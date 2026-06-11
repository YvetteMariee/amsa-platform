from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import traceback

from app.api.routes.upload import router as upload_router
from app.api.routes.search import router as search_router
from app.api.routes.ask import router as ask_router
from app.api.routes.ingestion import router as ingestion_router
from app.api.routes.analytics import router as analytics_router
from app.api.routes.alerts import router as alerts_router
from app.api.routes.auth import router as auth_router
from app.api.routes.users import router as users_router
from app.api.routes.audit import router as audit_router
from app.api.routes.reports import router as reports_router
from app.api.routes.supervision import router as supervision_router

from app.db.session import engine
from app.db.base import Base

app = FastAPI(title="AMSA - African Market Surveillance AI")

# CORS — autorise le frontend React à appeler le backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": str(exc),
            "detail": traceback.format_exc()
        }
    )

# ROUTES
app.include_router(upload_router)
app.include_router(search_router)
app.include_router(ask_router)
app.include_router(ingestion_router)
app.include_router(analytics_router)
app.include_router(alerts_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(audit_router)
app.include_router(reports_router)
app.include_router(supervision_router)

@app.get("/")
def root():
    return {"status": "AMSA backend running"}