from fastapi import APIRouter, HTTPException
from typing import Dict
from app.db.session import SessionLocal
from app.services.alert_service import get_alerts, update_alert_status

router = APIRouter()


@router.get("/alerts")
def list_alerts():
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
                "created_at": a.created_at.isoformat() if a.created_at else None
            }
            for a in alerts
        ]
    finally:
        session.close()


@router.post("/alerts/{alert_id}/status")
def change_status(alert_id: int, payload: Dict):
    status = payload.get("status")
    assigned_to = payload.get("assigned_to")
    comment = payload.get("comment")

    if not status:
        raise HTTPException(status_code=400, detail="status is required")

    session = SessionLocal()
    try:
        a = update_alert_status(session, alert_id, status, assigned_to, comment)
        if not a:
            raise HTTPException(status_code=404, detail="Alert not found")
        return {"message": "ok", "alert_id": a.id, "status": a.status}
    finally:
        session.close()
