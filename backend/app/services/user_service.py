from typing import Optional
from app.models.users import User
from app.db.session import SessionLocal
from app.services.auth_service import get_password_hash


def create_user(username: str, email: str, password: str, role: str = "ANALYST") -> User:
    session = SessionLocal()
    try:
        user = User(
            username=username,
            email=email,
            hashed_password=get_password_hash(password),
            role=role,
            is_active=True
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    finally:
        session.close()


def list_users():
    session = SessionLocal()
    try:
        return session.query(User).order_by(User.created_at.desc()).all()
    finally:
        session.close()
