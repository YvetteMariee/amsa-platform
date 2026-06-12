from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from app.services.auth_service import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_user_by_email,
)
from app.services.audit_service import log_action
from app.services.security import get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class MeResponse(BaseModel):
    id: int
    email: str
    role: str
    is_active: bool


@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), request: Request = None):
    user = get_user_by_email(form_data.username)
    if user and not user.is_active:
        log_action(user.id, "login_blocked", ip_address=request.client.host if request else None,
                   detail="Compte bloqué après plusieurs tentatives")
        raise HTTPException(status_code=403, detail="Compte bloqué après plusieurs tentatives")

    authenticated_user = authenticate_user(form_data.username, form_data.password)
    if not authenticated_user:
        if user:
            log_action(user.id, "login_failed", ip_address=request.client.host if request else None,
                       detail="Tentative de connexion échouée")
            if not user.is_active or user.failed_attempts >= 5:
                raise HTTPException(status_code=403, detail="Compte bloqué après plusieurs tentatives")
        else:
            log_action(None, "login_failed", ip_address=request.client.host if request else None,
                       detail="Tentative de connexion échouée pour utilisateur inconnu")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": authenticated_user.email, "role": authenticated_user.role, "user_id": authenticated_user.id})
    refresh_token = create_refresh_token({"sub": authenticated_user.email})
    log_action(authenticated_user.id, "login_success", ip_address=request.client.host if request else None,
               detail="Connexion réussie")
    return {"access_token": token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get("/me", response_model=MeResponse)
def me(current_user=Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.role,
        "is_active": current_user.is_active,
    }


@router.post("/refresh")
def refresh(request_data: RefreshRequest, request: Request = None):
    payload = decode_token(request_data.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user = get_user_by_email(email)
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")

    token = create_access_token({"sub": user.email, "role": user.role, "user_id": user.id})
    log_action(user.id, "refresh_token", ip_address=request.client.host if request else None,
               detail="Renouvellement du token d'accès")
    return {"access_token": token, "token_type": "bearer"}


@router.post("/logout")
def logout(current_user=Depends(get_current_user), request: Request = None):
    log_action(current_user.id, "logout", ip_address=request.client.host if request else None,
               detail="Déconnexion utilisateur")
    return {"message": "Déconnexion réussie"}
