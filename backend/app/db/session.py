from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./amsa.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # IMPORTANT pour FastAPI
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)