from fastapi import APIRouter
from ...db.chroma_client import collection

router = APIRouter()

@router.get("/search")
def search(keyword: str):

    try:
        all_data = collection.get()

        return {
            "total_ids": len(all_data.get("ids", [])),
            "sample_documents": all_data.get("documents", [])[:2]
        }

    except Exception as e:
        return {
            "error": str(e)
        }