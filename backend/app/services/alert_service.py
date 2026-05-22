from datetime import datetime
from typing import Optional
from app.db.session import SessionLocal
from app.models.alerts import Alert


def create_alert(session, instrument: str, anomaly_score: float, risk_level: str = "MEDIUM", comment: Optional[str] = None):
    a = Alert(
        instrument=instrument,
        anomaly_score=anomaly_score,
        risk_level=risk_level,
        status="NEW",
        comments=comment,
        created_at=datetime.utcnow()
    )
    session.add(a)
    session.commit()
    session.refresh(a)
    return a


def get_alerts(session):
    return session.query(Alert).order_by(Alert.created_at.desc()).all()


def update_alert_status(session, alert_id: int, status: str, assigned_to: Optional[int] = None, comment: Optional[str] = None):
    a = session.query(Alert).filter(Alert.id == alert_id).first()
    if not a:
        return None
    a.status = status
    if assigned_to is not None:
        a.assigned_to = assigned_to
    if comment:
        a.comments = (a.comments or "") + "\n" + comment
    session.commit()
    session.refresh(a)
    return a
