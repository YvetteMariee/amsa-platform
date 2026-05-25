from app.db.session import engine
from sqlalchemy import text

def seed():
    with engine.connect() as conn:
        conn.execute(text("""
        INSERT INTO market_data (date, instrument, prix, volume, compartiment)
        VALUES
        ('2026-05-01', 'BVMAC ACTION A', 1200.50, 100000, 'Actions'),
        ('2026-05-02', 'BVMAC ACTION B', 1500.00, 200000, 'Actions'),
        ('2026-05-03', 'BVMAC OBLIG 1', 980.00, 50000, 'Obligations')
        """))
        conn.commit()

if __name__ == "__main__":
    seed()
    print("Données insérées")