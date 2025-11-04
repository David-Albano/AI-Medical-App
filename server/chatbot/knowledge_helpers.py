import os
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
def split_text_into_chunks(text, max_chars=1000):
    """Splits long text into roughly token-sized chunks."""
    paragraphs = text.split("\n\n")
    chunks, current = [], ""

    for para in paragraphs:
        if len(current) + len(para) < max_chars:
            current += para + "\n\n"
        else:
            chunks.append(current.strip())
            current = para
    if current:
        chunks.append(current.strip())
    return chunks
