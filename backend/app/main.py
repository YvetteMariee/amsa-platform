from fastapi import FastAPI

from app.api.routes.upload import router as upload_router
from app.api.routes.search import router as search_router

app = FastAPI()

app.include_router(upload_router)
app.include_router(search_router)

@app.get("/")
def root():
    return {
        "status": "AMSA backend running"
    }