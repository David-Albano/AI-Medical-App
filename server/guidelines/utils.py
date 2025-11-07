# guidelines/utils.py
import numpy as np

from medical_ai.openai_client import get_openai_client
from medical_ai.settings import TEXT_EMBEDDING_MODEL

client = get_openai_client()


def embed_texts_openai(texts, model=None):
    """Return list of embedding vectors (lists) for each text using OpenAI embeddings API"""
    model = model or TEXT_EMBEDDING_MODEL

    # batching
    results = []
    BATCH = 16

    for i in range(0, len(texts), BATCH):

        batch = texts[i:i+BATCH]
        resp = client.embeddings.create(model=model, input=batch)

        # resp['data'] is list of {'embedding': [...]}
        for item in resp.data:
            results.append(item.embedding)

    return results

def cosine_sim(a, b):
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)

    if np.linalg.norm(a)==0 or np.linalg.norm(b)==0:
        return 0.0
    
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def similarity_search(query_embedding, chunk_rows, top_k=5):
    """
    chunk_rows: list of tuples (chunk_id, content, embedding)
    returns top_k rows sorted by similarity
    """
    scores = []

    for cid, content, emb in chunk_rows:
        score = cosine_sim(query_embedding, emb)
        scores.append((score, cid, content, emb))

    scores.sort(reverse=True, key=lambda x: x[0])

    return scores[:top_k]

def build_prompt_for_verdict(case_text, retrieved_chunks):
    """
    retrieved_chunks: list of (score, chunk_id, content)
    We'll instruct the LLM to answer in JSON: {verdict, rationale, supporting_chunk_ids}
    """
    header = (
        "You are an expert medical policy adjudicator. "
        "You will be given (1) a user's patient case or question, and (2) supporting excerpts from a medical guideline or an insurance policy. "
        "Your output MUST be valid JSON with the following keys: "
        "verdict (one of: \"Covered\", \"Partially covered\", \"Not covered\"), "
        "rationale (concise explanation, cite which chunk ids or sections you relied on), "
        "supporting_chunks (list of chunk ids), "
        "confidence (0.0-1.0). "
        "Do NOT output any extra text outside JSON."
    )

    snippets = []

    for idx, (score, cid, content, emb) in enumerate(retrieved_chunks):
        snippets.append(f"CHUNK_{cid} (score={score:.3f}):\n{content}\n---")
    
    prompt = (
        header + "\n\n"
        f"CASE:\n{case_text}\n\n"
        "EXCERPTS:\n" + "\n".join(snippets) + "\n\n"
        "Answer now in JSON exactly as required."
    )

    return prompt

def call_llm_for_verdict(prompt, model=None, temperature=0.0):
    model = model or TEXT_EMBEDDING_MODEL

    resp = client.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=500
    )

    text = resp["choices"][0]["message"]["content"]

    return text
