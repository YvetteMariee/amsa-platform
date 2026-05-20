from fastapi import APIRouter

from app.services.embedding_service import create_embedding
from app.db.chroma_client import collection

router = APIRouter()

@router.get("/search")
def search(query: str):

    query_embedding = create_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    return results