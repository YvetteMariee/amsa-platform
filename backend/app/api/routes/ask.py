from fastapi import APIRouter
from app.services.embedding_service import create_embedding
from app.db.chroma_client import collection

router = APIRouter()

@router.get("/ask")
def ask(filename: str, question: str):

    # 1. embedding de la question
    query_embedding = create_embedding(question)

    # 2. recherche dans Chroma
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    # 3. extraction des chunks
    chunks = results["documents"][0] if results["documents"] else []

    # 4. réponse simple (sans LLM pour l'instant)
    answer = "\n".join(chunks)

    return {
        "question": question,
        "filename": filename,
        "answer": answer
    }