from app.db.base import Base
from app.db.session import engine

from app.models import market_data, alerts, annotations, audit_logs, users, reports  # noqa: F401


def init():
    Base.metadata.create_all(bind=engine)
    print("DB initialisée")


if __name__ == "__main__":
    init()
