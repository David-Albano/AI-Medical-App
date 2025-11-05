import os, json, tiktoken
from django.shortcuts import render
from django.db import transaction
from chatbot.knowledge_helpers import extract_text_from_file, split_text_into_chunks
from chatbot.rag_utils import retrieve_relevant_chunks
from chatbot.serializers import MedicalCategorySerializer
from medical_ai.openai_client import get_openai_client
from .models import ChatMessage, ChatSession, KnowledgeChunk, MedicalCategory
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

client = get_openai_client()

class GetMedicalCategories(APIView):

    def get(self, request):
        try:
            medical_categories = MedicalCategory.objects.all()
            medical_categories_serialized = MedicalCategorySerializer(medical_categories, many=True)

            response = {
                'medical_categories': medical_categories_serialized.data
            }

            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            return Exception(str(e))
            

# --- MAIN ENDPOINT ---
@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def upload_knowledge_files(request):
    """
    Upload multiple files -> extract text -> create KnowledgeChunk embeddings.
    """
    files = request.FILES.getlist("files")
    medical_category_pk = request.data.get("medical_category_pk", None)

    if not files:
        return Response({"error": "No files provided."}, status=status.HTTP_400_BAD_REQUEST)

    if not medical_category_pk:
        raise Exception('Please select medical category')
    
    try:
        medical_category_pk = int(medical_category_pk)
    except (TypeError, ValueError):
        medical_category_pk = None

    related_category = MedicalCategory.objects.get(pk=medical_category_pk)

    created_chunks = 0
    results = []

    try:
        with transaction.atomic():
            for f in files:
                text = extract_text_from_file(f)
                if not text:
                    results.append({"file": f.name, "status": "no_text_found"})
                    continue

                chunks = split_text_into_chunks(text)

                for chunk in chunks:
                    tokens = tiktoken.encoding_for_model("text-embedding-3-small").encode(chunk)

                    if len(tokens) > 8192:
                        # truncate safely
                        chunk = tiktoken.encoding_for_model("text-embedding-3-small").decode(tokens[:8192])

                    embedding = client.embeddings.create(
                        model="text-embedding-3-small",
                        input=chunk
                    ).data[0].embedding

                    KnowledgeChunk.objects.create(
                        title=f.name,
                        content=chunk,
                        category=related_category,
                        embedding=embedding,
                        source=f.name,
                    )
                    created_chunks += 1

                results.append({"file": f.name, "chunks_created": len(chunks)})

        return Response({
            "status": "success",
            "total_chunks": created_chunks,
            "details": results
        })

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChatbotAPIView(APIView):
    def post(self, request, session_id=None):
        answer = 'Default answer text'

        user_message = request.data.get("message")
        knowledge_categories = request.data.get("knowledge_categories", [])

        if not user_message:
            return Response({"error": "Message required"}, status=400)

        if not knowledge_categories:
            return Response({"error": "Select at least one category"}, status=400)

        session, _ = ChatSession.objects.get_or_create(session_id=session_id or "default")
        ChatMessage.objects.create(session=session, role="user", content=user_message)

        # === RAG retrieval ===
        context_chunks = retrieve_relevant_chunks(user_message, knowledge_categories)
        context_text = "\n\n".join(context_chunks) or "No relevant data found."

        # === LLM Response ===
        prompt = f"""You are a helpful health assistant.
        Use this context to answer accurately and clearly:
        {context_text}

        User question: {user_message}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You explain health info simply and accurately."},
                {"role": "user", "content": prompt}
            ],
        )
        
        answer = response.choices[0].message.content.strip()

        ChatMessage.objects.create(session=session, role="assistant", content=answer)
        
        return Response({"answer": answer})
    
    