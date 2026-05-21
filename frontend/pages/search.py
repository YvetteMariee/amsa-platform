from fastapi import APIRouter
from app.services.pdf_service import search_in_all_pdfs

router = APIRouter()

@router.get("/search")
def search(query: str):
    results = search_in_all_pdfs(query)
    return {
        "query": query,
        "results": results
    }