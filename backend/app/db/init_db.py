from app.db.base import Base
from app.db.session import engine

# importe tes modèles pour qu’ils soient enregistrés
from app.models import market_data  # si ton model existe

def init():
    Base.metadata.create_all(bind=engine)
    print("DB initialisée")

if __name__ == "__main__":
    init()