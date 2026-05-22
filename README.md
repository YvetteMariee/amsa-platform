# AMSA — African Market Surveillance AI

Plateforme de surveillance financière institutionnelle pour la COSUMAF.

## Architecture

- Backend: FastAPI + SQLAlchemy + PostgreSQL + Camelot + scikit-learn
- Frontend: React + Vite + TailwindCSS + Axios + Recharts
- DevOps: Docker + docker-compose

## Fonctionnalités principales

- Upload de fichiers PDF, CSV, XLSX
- Parsing Camelot pour extraction tableur PDF
- Normalisation et ingestion dans `market_data`
- Indicateurs métier et détection d'anomalies IA (IsolationForest)
- Génération d'alertes automatiques
- RBAC JWT avec rôles ADMIN, SUPERVISOR, ANALYST
- Endpoints : `/upload`, `/ingest-pdfs`, `/analytics/market_data`, `/alerts`, `/alerts/{id}/status`, `/auth/login`, `/users`, `/reports`, `/audit/logs`, `/supervision/health`

## Prérequis

- Docker
- Docker Compose
- Node.js 20+ (optionnel pour dev local frontend)
- Python 3.13 (optionnel pour dev local backend)

## Lancer avec Docker

```bash
cd c:\Users\23765\Desktop\amsa-platform
docker compose up --build
```

- Backend : http://localhost:8000
- Frontend : http://localhost:5173

## Lancer localement

### Backend

```bash
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0
```

## Comptes de démonstration

- admin / admin123 (SUPERVISOR)

## Notes

- Le script de seed est situé dans `scripts/seed_market_data.py`.
- Le backend crée automatiquement les tables SQLAlchemy au démarrage.
- Le frontend utilise `VITE_API_URL` pour appeler le backend.
