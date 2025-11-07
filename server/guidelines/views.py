# guidelines/views.py
import os
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import transaction
import tiktoken

from medical_ai.helpers import extract_text_from_file, split_text_into_chunks, handle_file_deletion
from medical_ai.settings import TEXT_EMBEDDING_MODEL
from .models import GuidelineDocument, GuidelineChunk, ComparisonQuery
from .serializers import GuidelineDocumentSerializer, ComparisonQuerySerializer
from .utils import embed_texts_openai, similarity_search, build_prompt_for_verdict, call_llm_for_verdict


class GuidelineUploadAPIView(APIView):

    def post(self, request):
        try:
            files = request.FILES.getlist("files")
            
            if not files:
                return Response({"detail": "File required."}, status=400)
            
            created_chunks = 0
            files_processed = []
            
            with transaction.atomic():
                for f in files:
                    try:
                        content = extract_text_from_file(f)

                        if not content:
                            files_processed.append({"file": f.name, "status": "No text found"})
                            continue

                        doc = GuidelineDocument.objects.create(title=f.name, file=f)
                        
                        try:
                            doc.content = content
                            doc.save()

                            n_chunks = self.process_guideline(doc)
                            created_chunks += n_chunks

                            file_process_result = {
                                "file": doc.title,
                                "chunks_created": n_chunks,
                            }

                            files_processed.append(file_process_result)

                        except Exception as e:
                            handle_file_deletion(doc.pk, GuidelineDocument)
                            return Response({"detail": "Uploaded but failed to process guidelines: " + str(e)}, status=201)

                    except Exception as e:
                        return Response({"detail": "Uploaded but failed to extract text: " + str(e)}, status=201)

            return Response({
                "status": "Success",
                "total_chunks": created_chunks,
                "details": files_processed
            }, status=201)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def process_guideline(self, guideline_doc):
        try:
            """
            Synchronously process a document into chunks+embeddings.
            For scale, move to background (Celery) - example commented below.
            """
            
            if guideline_doc.processed:
                return Response({"detail":"Already processed"}, status=400)
            
            text = guideline_doc.content or ""
            
            if not text:
                return Response({"detail":"No extracted text available."}, status=400)
            
            # chunk
            chunks = split_text_into_chunks(text)
            
            # Save chunks (order) and embed in batches
            chunk_objs = []

            for idx, chunk in enumerate(chunks):
                tokens = tiktoken.encoding_for_model(TEXT_EMBEDDING_MODEL).encode(chunk)

                if len(tokens) > 8192:
                    # truncate safely
                    chunk = tiktoken.encoding_for_model(TEXT_EMBEDDING_MODEL).decode(tokens[:8192])

                c = GuidelineChunk.objects.create(guideline=guideline_doc, content=chunk, order=idx)
                chunk_objs.append(c)

            # create embeddings in batches
            texts = [c.content for c in chunk_objs]
            embeddings = embed_texts_openai(texts)

            for c, emb in zip(chunk_objs, embeddings):
                c.embedding = emb
                c.save()

            guideline_doc.processed = True
            guideline_doc.save()
            
            return len(chunk_objs)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        

class CompareQueryAPIView(APIView):
    
    def post(self, request, pk):
        try:
            """
            pk = guideline id to compare against (or could accept global search in future).
            Request body: { "query_text": "...", "top_k": 5 }
            """
            doc = get_object_or_404(GuidelineDocument, pk=pk)

            if not doc.processed:
                return Response({"detail":"Document not processed. Run processing first."}, status=400)
            query_text = request.data.get("query_text")

            if not query_text:
                return Response({"detail":"query_text required."}, status=400)
            
            top_k = int(request.data.get("top_k", 5))

            # embed query
            query_emb = embed_texts_openai([query_text])[0]

            # load chunks and their embeddings from DB
            chunks_qs = GuidelineChunk.objects.filter(guideline=doc).order_by("order")
            chunk_rows = []

            for c in chunks_qs:
                if not c.embedding:
                    continue
                chunk_rows.append((c.id, c.content, c.embedding))

            # convert to expected tuple for similarity_search (cid, content, emb)
            prepared = [(cid, content, emb) for (cid, content, emb) in chunk_rows]
            
            # similarity_search expects (chunk_id, content, embedding)
            # adapt:
            top = similarity_search(query_emb, [(cid, content, emb) for cid, content, emb in prepared], top_k=top_k)
            
            # top is list of (score, cid, content, emb)
            prompt = build_prompt_for_verdict(query_text, top)
            raw_llm_response = call_llm_for_verdict(prompt)

            # parse JSON from LLM response (best effort)
            try:
                parsed = json.loads(raw_llm_response)
                verdict = parsed.get("verdict")
                rationale = parsed.get("rationale")
                confidence = float(parsed.get("confidence", 0.0))

            except Exception:
                # fallback: save raw text and attempt to extract verdict via simple heuristics
                verdict = None
                rationale = raw_llm_response
                confidence = None

            # compute a similarity-derived confidence too (average of top scores)
            avg_sim = sum([s for s, *_ in top]) / len(top) if top else 0.0

            # combine confidences (if LLM gave one)
            if confidence is None:
                combined_confidence = float(avg_sim)
            else:
                combined_confidence = float(0.6*confidence + 0.4*avg_sim)
            
            # Save ComparisonQuery
            cq = ComparisonQuery.objects.create(
                query_text=query_text,
                guideline=doc,
                ai_response=raw_llm_response,
                verdict=verdict or "Undetermined",
                confidence=combined_confidence
            )

            serializer = ComparisonQuerySerializer(cq)

            return Response({
                "id": cq.id,
                "verdict": cq.verdict,
                "confidence": combined_confidence,
                "rationale": rationale,
                "llm_raw": raw_llm_response,
                "supporting_chunks": [{"chunk_id": cid, "score": score, "content": content[:300]} for score, cid, content, emb in top]
            }, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)