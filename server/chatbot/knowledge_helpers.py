import os, tiktoken
import tempfile
from PyPDF2 import PdfReader
from docx import Document
import pytesseract
from PIL import Image


# --- Utility: extract text from file depending on type ---
def extract_text_from_file(uploaded_file):
    """Extracts text from txt, pdf, docx, or image."""
    name = uploaded_file.name.lower()

    # Save temporarily to disk
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        for chunk in uploaded_file.chunks():
            tmp.write(chunk)
        tmp_path = tmp.name

    text = ""
    try:
        if name.endswith(".txt"):
            with open(tmp_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()

        elif name.endswith(".pdf"):
            reader = PdfReader(tmp_path)
            text = "\n".join([page.extract_text() or "" for page in reader.pages])

        elif name.endswith(".docx"):
            doc = Document(tmp_path)
            text = "\n".join([para.text for para in doc.paragraphs])

        elif name.endswith((".jpg", ".jpeg", ".png")):
            img = Image.open(tmp_path)
            text = pytesseract.image_to_string(img)

        else:
            text = f"[Unsupported file type: {name}]"

    finally:
        os.remove(tmp_path)

    return text.strip()

# --- Utility: split into smaller chunks for embeddings ---
def split_text_into_chunks(text, max_tokens=7500, model="text-embedding-3-small"):
    """Splits text into chunks that safely fit within token limits."""
    enc = tiktoken.encoding_for_model(model)
    paragraphs = text.split("\n\n")
    chunks = []
    current_tokens = []
    current_length = 0

    for para in paragraphs:
        tokens = enc.encode(para)
        paragraph_len = len(tokens)

        # If adding this paragraph would exceed the limit, start a new chunk
        if current_length + paragraph_len > max_tokens:
            if current_tokens:
                chunks.append(enc.decode(current_tokens))

            current_tokens = tokens
            current_length = paragraph_len
            
        else:
            current_tokens.extend(tokens)
            current_length += paragraph_len

    if current_tokens:
        chunks.append(enc.decode(current_tokens))

    return chunks
