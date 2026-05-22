from datetime import datetime
from typing import Optional
from app.models.audit_logs import AuditLog
from app.db.session import SessionLocal


def log_action(user_id: Optional[int], action: str, entity: Optional[str] = None, detail: Optional[str] = None, ip_address: Optional[str] = None):
    session = SessionLocal()
    try:
        audit = AuditLog(
            user_id=user_id,
            action=action,
            entity=entity,
            detail=detail,
            ip_address=ip_address,
            created_at=datetime.utcnow()
        )
        session.add(audit)
        session.commit()
        session.refresh(audit)
        return audit
    finally:
        session.close()


def list_audit_logs():
    session = SessionLocal()
    try:
        return session.query(AuditLog).order_by(AuditLog.created_at.desc()).all()
    finally:
        session.close()
