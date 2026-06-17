import os
from fastapi import APIRouter, Depends
from app.db.chroma_client import collection
from app.services.security import require_roles

router = APIRouter(prefix="/ask")


@router.get("")
def ask(
    question: str,
    filename: str = "",
    current_user=Depends(require_roles(["ADMIN", "SUPERVISOR", "ANALYST"])),
):
    where_filter = {"source": filename} if filename else None

    try:
        results = collection.query(
            query_texts=[question],
            n_results=5,
            where=where_filter,
        )
    except Exception:
        results = collection.query(query_texts=[question], n_results=5)

    documents = results.get("documents", [[]])[0]
    context = "\n---\n".join(documents) if documents else ""

    if not context:
        return {"answer": "Aucun document pertinent trouvé.", "sources": []}

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {
            "answer": "Le service IA n'est pas configuré (clé API manquante). Voici les extraits pertinents :",
            "sources": documents,
        }

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Tu es AMSA, un assistant expert en surveillance des marchés financiers de la CEMAC/BVMAC. "
                        "Réponds en français en te basant uniquement sur le contexte fourni."
                    ),
                },
                {"role": "user", "content": f"Contexte:\n{context}\n\nQuestion: {question}"},
            ],
            max_tokens=1024,
        )
        answer = response.choices[0].message.content
    except Exception as e:
        return {"answer": f"Erreur IA: {e}", "sources": documents}

    return {"answer": answer, "sources": documents}
