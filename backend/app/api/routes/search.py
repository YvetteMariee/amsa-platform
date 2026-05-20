from fastapi import APIRouter
from services.pdf_service import search_in_all_pdfs

router = APIRouter()

@router.get("/search")
def search(keyword: str):
    return search_in_all_pdfs(keyword)