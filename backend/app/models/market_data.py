from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Date
from app.db.base import Base


class MarketData(Base):
    __tablename__ = "market_data"

    id = Column(Integer, primary_key=True, index=True)
    instrument = Column(String(255), index=True, nullable=True)
    prix = Column(Float, nullable=True)
    volume = Column(Float, nullable=True)
    date = Column(Date, nullable=True)
    compartiment = Column(String(50), nullable=True)
    source_file = Column(String(255), nullable=True)
    anomaly_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
