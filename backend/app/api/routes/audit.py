from fastapi import APIRouter, Depends
from app.services.audit_service import list_audit_logs
from app.services.security import require_roles

router = APIRouter()


@router.get("/audit/logs")
def audit_logs(current_user=Depends(require_roles(["ADMIN", "SUPERVISOR"]))):
    logs = list_audit_logs()
    return [
        {
            "id": log.id,
            "user_id": log.user_id,
            "action": log.action,
            "entity": log.entity,
            "detail": log.detail,
            "ip_address": log.ip_address,
            "created_at": log.created_at.isoformat() if log.created_at else None,
        }
        for log in logs
    ]
