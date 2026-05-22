from fastapi import APIRouter
from app.services.pdf_ingestion import process_all_pdfs

router = APIRouter()


@router.get("/ingest-pdfs")
def ingest_pdfs():

    df = process_all_pdfs()

    return {
        "rows": len(df),
        "data": df.head().to_dict()
    }