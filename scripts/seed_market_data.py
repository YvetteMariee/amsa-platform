import random
from datetime import date, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.market_data import MarketData

DATABASE_URL = "postgresql://amsa:amsa@localhost:5432/amsa_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def seed(n=100):
    session = SessionLocal()
    base_date = date.today() - timedelta(days=n)
    for i in range(n):
        d = base_date + timedelta(days=i)
        prix = round(100 + random.gauss(0, 5) + (i % 10) * 0.5, 2)
        volume = int(abs(random.gauss(1000, 300)) + (i % 5) * 100)
        m = MarketData(
            instrument=f"TITRE_{(i%10)+1}",
            prix=prix,
            volume=volume,
            date=d,
            import random
            from datetime import date, timedelta
            from sqlalchemy import create_engine
            from sqlalchemy.orm import sessionmaker
            from app.models.market_data import MarketData
            from app.models.users import User
            from app.services.auth_service import get_password_hash

            DATABASE_URL = "postgresql://amsa:amsa@localhost:5432/amsa_db"

            engine = create_engine(DATABASE_URL)
            SessionLocal = sessionmaker(bind=engine)


            def seed(n=100):
                session = SessionLocal()

                # create admin user if not exists
                admin = session.query(User).filter(User.username == 'admin').first()
                if not admin:
                    u = User(
                        username='admin',
                        email='admin@cosumaf.local',
                        hashed_password=get_password_hash('admin123'),
                        role='SUPERVISOR'
                    )
                    session.add(u)
                    session.commit()

                base_date = date.today() - timedelta(days=n)
                for i in range(n):
                    d = base_date + timedelta(days=i)
                    prix = round(100 + random.gauss(0, 5) + (i % 10) * 0.5, 2)
                    volume = int(abs(random.gauss(1000, 300)) + (i % 5) * 100)
                    m = MarketData(
                        instrument=f"TITRE_{(i%10)+1}",
                        prix=prix,
                        volume=volume,
                        date=d,
                        compartiment="A",
                        source_file="seed",
                    )
                    session.add(m)
                session.commit()
                session.close()


            if __name__ == "__main__":
                seed(200)
                print("Seeded market_data and admin user")
