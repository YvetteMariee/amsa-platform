"""
Script d'initialisation AMSA
Lance depuis : amsa-platform/backend/
Commande     : python init_admin.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db.session import engine, SessionLocal
from app.db.base import Base
from app.models.users import User
from app.services.auth_service import get_password_hash

# ── 1. Créer toutes les tables ──────────────────────────────────────────────
print("Création des tables...")
Base.metadata.create_all(bind=engine)
print("✅ Tables créées")

# ── 2. Créer l'utilisateur admin ────────────────────────────────────────────
db = SessionLocal()

USERNAME = "admin"
EMAIL    = "admin@amsa.cemac"
PASSWORD = "Admin1234!"
ROLE     = "ADMIN"

existing = db.query(User).filter(User.username == USERNAME).first()

if existing:
    existing.hashed_password = get_password_hash(PASSWORD)
    existing.is_active = True
    existing.role = ROLE
    db.commit()
    print(f"✅ Mot de passe réinitialisé pour : {USERNAME}")
else:
    admin = User(
        username=USERNAME,
        email=EMAIL,
        hashed_password=get_password_hash(PASSWORD),
        role=ROLE,
        is_active=True
    )
    db.add(admin)
    db.commit()
    print(f"✅ Utilisateur admin créé")

db.close()

print("")
print("═══════════════════════════════════════")
print("  AMSA — Credentials admin")
print("═══════════════════════════════════════")
print(f"  Username : {USERNAME}")
print(f"  Password : {PASSWORD}")
print(f"  Role     : {ROLE}")
print("═══════════════════════════════════════")
print("")
print("Connecte-toi sur http://localhost:5173")