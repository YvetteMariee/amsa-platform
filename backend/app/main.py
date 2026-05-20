from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import traceback

from app.api.routes.upload import router as upload_router
from app.api.routes.search import router as search_router
from app.api.routes.ask import router as ask_router

app = FastAPI()

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": str(exc), "detail": traceback.format_exc()}
    )

app.include_router(ask_router)
app.include_router(upload_router)
app.include_router(search_router)

@app.get("/")
def root():
    return {"status": "AMSA backend running"}