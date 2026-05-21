from fastapi import APIRouter, UploadFile, File
import os
import shutil

from ...services.pdf_service import extract_text_from_pdf
from ...services.embedding_service import create_embedding
from ...db.chroma_client import collection

router = APIRouter()

UPLOAD_DIR = "data/uploads"


def chunk_text(text, chunk_size=500):
    return [
        text[i:i + chunk_size]
        for i in range(0, len(text), chunk_size)
    ]


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    # 1. save file
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2. extract text
    text = extract_text_from_pdf(file_path)

    # 3. chunk text
    chunks = chunk_text(text)

    # 4. embeddings par chunk
    embeddings = [
        create_embedding(chunk)
        for chunk in chunks
    ]

    # 5. store in Chroma
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=[f"{file.filename}_{i}" for i in range(len(chunks))]
    )

    return {
        "message": "upload + indexing OK",
        "chunks": len(chunks)
    }