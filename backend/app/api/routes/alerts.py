from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional

from app.db.session import SessionLocal
from app.services.alert_service import get_alerts, update_alert_status
from app.services.security import require_roles

router = APIRouter()


class AlertStatusUpdate(BaseModel):
    status: str
    assigned_to: Optional[int] = None
    comment: Optional[str] = None


@router.get("/alerts")
def list_alerts(current_user=Depends(require_roles(["ADMIN", "SUPERVISOR", "ANALYST"]))):
    session = SessionLocal()
    try:
        alerts = get_alerts(session)
        return [
            {
                "id": a.id,
                "instrument": a.instrument,
                "anomaly_score": a.anomaly_score,
                "risk_level": a.risk_level,
                "status": a.status,
                "assigned_to": a.assigned_to,
                "comments": a.comments,
                "created_at": a.created_at.isoformat() if a.created_at else None,
            }
            for a in alerts
        ]
    finally:
        session.close()


@router.post("/alerts/{alert_id}/status")
def change_status(
    alert_id: int,
    payload: AlertStatusUpdate,
    current_user=Depends(require_roles(["ADMIN", "SUPERVISOR"])),
):
    session = SessionLocal()
    try:
        a = update_alert_status(session, alert_id, payload.status, payload.assigned_to, payload.comment)
        if not a:
            raise HTTPException(status_code=404, detail="Alert not found")
        return {"message": "ok", "alert_id": a.id, "status": a.status}
    finally:
        session.close()
