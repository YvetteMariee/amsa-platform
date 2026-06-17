from fastapi import APIRouter, Depends
from app.db.chroma_client import collection
from app.services.security import require_roles

router = APIRouter()


@router.get("/search")
def search(
    keyword: str,
    current_user=Depends(require_roles(["ADMIN", "SUPERVISOR", "ANALYST"])),
):
    try:
        results = collection.query(
            query_texts=[keyword],
            n_results=10,
        )
        documents = results.get("documents", [[]])[0]
        ids = results.get("ids", [[]])[0]
        distances = results.get("distances", [[]])[0] if results.get("distances") else []

        return {
            "keyword": keyword,
            "total_results": len(documents),
            "results": [
                {"id": ids[i], "document": documents[i], "score": distances[i] if i < len(distances) else None}
                for i in range(len(documents))
            ],
        }
    except Exception as e:
        return {"error": str(e)}
