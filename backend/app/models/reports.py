from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from app.db.base import Base


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    report_type = Column(String(64), nullable=True)
    period = Column(String(64), nullable=True)
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
