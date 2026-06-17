import os
import random
from datetime import date, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.models.market_data import MarketData
from app.models.users import User
from app.services.auth_service import get_password_hash
from app.db.base import Base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./backend/amsa.db")

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine)


def seed(n=200):
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()

    admin = session.query(User).filter(User.username == "admin").first()
    if not admin:
        u = User(
            username="admin",
            email="admin@cosumaf.local",
            hashed_password=get_password_hash("admin123"),
            role="ADMIN",
        )
        session.add(u)
        session.commit()

    supervisor = session.query(User).filter(User.username == "supervisor").first()
    if not supervisor:
        u = User(
            username="supervisor",
            email="supervisor@cosumaf.local",
            hashed_password=get_password_hash("supervisor123"),
            role="SUPERVISOR",
        )
        session.add(u)
        session.commit()

    analyst = session.query(User).filter(User.username == "analyst").first()
    if not analyst:
        u = User(
            username="analyst",
            email="analyst@cosumaf.local",
            hashed_password=get_password_hash("analyst123"),
            role="ANALYST",
        )
        session.add(u)
        session.commit()

    instruments = [
        "SEMC", "SAFACAM", "SOCAPALM", "SIC CACAOS", "BICEC",
        "AFRILAND", "SCB-CA", "CHOCOCAM", "SCDP", "SOCATRAL",
    ]
    compartiments = ["Actions", "Obligations", "TCN"]

    base_date = date.today() - timedelta(days=n)
    for i in range(n):
        d = base_date + timedelta(days=i)
        prix = round(100 + random.gauss(0, 5) + (i % 10) * 0.5, 2)
        volume = int(abs(random.gauss(1000, 300)) + (i % 5) * 100)
        m = MarketData(
            instrument=instruments[i % len(instruments)],
            prix=prix,
            volume=volume,
            date=d,
            compartiment=compartiments[i % len(compartiments)],
            source_file="seed",
        )
        session.add(m)

    session.commit()
    session.close()


if __name__ == "__main__":
    seed(200)
    print("Seeded market_data + users (admin/supervisor/analyst)")
