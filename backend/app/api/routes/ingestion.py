from fastapi import APIRouter, Depends
from app.services.pdf_ingestion import process_all_pdfs
from app.services.security import require_roles

router = APIRouter()


@router.get("/ingest-pdfs")
def ingest_pdfs(current_user=Depends(require_roles(["ADMIN", "SUPERVISOR", "ANALYST"]))):
    df = process_all_pdfs()
    return {
        "rows": len(df),
        "loaded_files": df["source_file"].unique().tolist() if not df.empty else [],
        "sample": df.head(5).to_dict(orient="records")
    }