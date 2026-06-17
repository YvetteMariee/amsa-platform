from fastapi import APIRouter, Depends
from sqlalchemy import text
from app.db.session import engine
from app.services.security import require_roles
import pandas as pd

router = APIRouter()


@router.get("/reports")
def get_reports(current_user=Depends(require_roles(["ADMIN", "SUPERVISOR", "ANALYST"]))):
    query = text("SELECT date, instrument, prix, volume, compartiment FROM market_data ORDER BY date DESC LIMIT 200")
    df = pd.read_sql(query, engine)
    if df.empty:
        return {"reports": []}

    summary = df.groupby("compartiment").agg({"prix": ["mean", "max"], "volume": ["sum"]})
    summary.columns = ["avg_price", "max_price", "total_volume"]
    summary = summary.reset_index().to_dict(orient="records")

    return {
        "reports": [
            {
                "title": "Surveillance mensuelle de marché",
                "period": "Derniers 200 enregistrements",
                "summary_by_compartiment": summary,
            }
        ]
    }
