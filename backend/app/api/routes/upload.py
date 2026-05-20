from fastapi import APIRouter, UploadFile, File
import os
import shutil

from app.services.pdf_service import extract_text_from_pdf
from app.services.embedding_service import create_embedding
from app.db.chroma_client import collection

router = APIRouter()

UPLOAD_DIR = "data/uploads"

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text_from_pdf(file_path)

    embedding = create_embedding(text)

    collection.add(
        documents=[text],
        embeddings=[embedding],
        ids=[file.filename]
    )

    return {
        "message": "upload réussi",
        "filename": file.filename
    }