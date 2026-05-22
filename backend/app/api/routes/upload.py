from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
import os
import shutil
from typing import Dict

from ...services.pdf_parser import parse_pdf
from ...services.csv_ingestion import ingest_dataframe
from ...services.security import require_roles
from ...db.session import engine

router = APIRouter()

BASE_APP_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UPLOAD_DIR = os.path.join(BASE_APP_DIR, "data", "uploads")

ALLOWED_EXT = {".pdf", ".csv", ".xlsx", ".xls"}


def _ensure_upload_dir():
    os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...), current_user=Depends(require_roles(["ADMIN", "SUPERVISOR", "ANALYST"]))):
    """Save an uploaded file, validate type, then route to ingestion.

    PDF -> parse tables and attempt to append to `market_data` table
    CSV/XLSX -> load and write to `market_data` via ingest_dataframe
    """
    _ensure_upload_dir()

    filename = file.filename
    if not filename:
        raise HTTPException(status_code=400, detail="Missing filename")

    _, ext = os.path.splitext(filename)
    ext = ext.lower()

    if ext not in ALLOWED_EXT:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")

    file_path = os.path.join(UPLOAD_DIR, filename)

    # Save uploaded file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

    # Route ingestion based on type
    try:
        if ext == ".pdf":
            df = parse_pdf(file_path)
            # attempt to persist to PostgreSQL market_data table
            try:
                df.to_sql("market_data", engine, if_exists="append", index=False)
                rows = len(df)
            except Exception:
                rows = len(df)

            return {"message": "pdf_ingested", "file": filename, "rows": rows}

        else:
            # csv / xlsx
            res = ingest_dataframe(file_path, table_name="market_data")
            return {"message": "table_ingested", "file": filename, **res}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
