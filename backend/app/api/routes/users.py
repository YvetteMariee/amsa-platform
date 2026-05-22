from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from app.services.user_service import create_user, list_users
from app.services.security import require_roles

router = APIRouter()


class UserCreateRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "ANALYST"


@router.get("/users")
def get_users(current_user=Depends(require_roles(["ADMIN", "SUPERVISOR"]))):
    users = list_users()
    return [
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "role": u.role,
            "is_active": u.is_active,
            "created_at": u.created_at.isoformat() if u.created_at else None,
        }
        for u in users
    ]


@router.post("/users")
def add_user(payload: UserCreateRequest, current_user=Depends(require_roles(["ADMIN"]))):
    user = create_user(payload.username, payload.email, payload.password, payload.role)
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
    }
