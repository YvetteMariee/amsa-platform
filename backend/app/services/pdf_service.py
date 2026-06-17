import os
from pypdf import PdfReader

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "data", "uploads")


def get_all_pdfs():
    pdf_files = []
    for root, dirs, files in os.walk(UPLOAD_DIR):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_files.append(os.path.join(root, file))
    return pdf_files


def search_in_all_pdfs(query: str):
    results = []
    for pdf_path in get_all_pdfs():
        try:
            reader = PdfReader(pdf_path)
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                if query.lower() in text.lower():
                    results.append({
                        "file": pdf_path,
                        "page": page_num + 1,
                        "snippet": text[:200],
                    })
                    break
        except Exception:
            pass
    return results


def extract_text_from_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text
