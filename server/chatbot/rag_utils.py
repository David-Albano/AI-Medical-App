# chatbot/rag_utils.py
import numpy as np
from medical_ai.openai_client import get_openai_client
from medical_ai.settings import TEXT_EMBEDDING_MODEL
from .models import KnowledgeChunk

client = get_openai_client()

def get_embedding(text, model=TEXT_EMBEDDING_MODEL):
    """Get OpenAI embedding vector for a given text."""
    res = client.embeddings.create(input=text, model=model)
    return res.data[0].embedding


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def retrieve_relevant_chunks(query, knowledge_category, top_k=3):
    """Return top_k most relevant KnowledgeChunk texts."""
    query_emb = get_embedding(query)
    chunks = KnowledgeChunk.objects.exclude(embedding__isnull=True, category__isnull=True).filter(category__pk__in=knowledge_category)
    
    scored = []
    for chunk in chunks:
        if not chunk.embedding:
            continue
        sim = cosine_similarity(query_emb, chunk.embedding)
        scored.append((sim, chunk.content))
    
    scored.sort(reverse=True, key=lambda x: x[0])
    top_chunks = [text for _, text in scored[:top_k]]

    return top_chunks
