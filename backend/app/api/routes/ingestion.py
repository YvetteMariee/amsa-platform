from fastapi import APIRouter, UploadFile, File
import os

from app.services.csv_ingestion import ingest_dataframe

router = APIRouter()

UPLOAD_DIR = "app/data/uploads"

@router.post("/ingest")
async def ingest(file: UploadFile = File(...)):

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(file_path, "wb") as f:
        f.write(await file.read())

    table_name = file.filename.split(".")[0].lower()

    result = ingest_dataframe(
        file_path,
        table_name
    )

    return result