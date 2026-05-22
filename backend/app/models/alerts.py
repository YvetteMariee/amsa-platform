from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    instrument = Column(String(255), nullable=True)
    anomaly_score = Column(Float, nullable=True)
    risk_level = Column(String(32), nullable=True)
    status = Column(String(32), nullable=False, default="NEW")
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    comments = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    assignee = relationship("User", backref="alerts")
