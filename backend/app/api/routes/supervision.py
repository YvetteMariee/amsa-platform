from fastapi import APIRouter
from app.db.session import engine

router = APIRouter()


@router.get("/supervision/health")
def health_check():
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return {"status": "ok", "database": "connected"}
    except Exception as exc:
        return {"status": "error", "detail": str(exc)}
