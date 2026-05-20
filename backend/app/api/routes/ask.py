from fastapi import APIRouter

router = APIRouter(prefix="/ask")

@router.get("")
def ask(filename: str, question: str):
    return {
        "step": "endpoint_ok",
        "filename": filename,
        "question": question
    }