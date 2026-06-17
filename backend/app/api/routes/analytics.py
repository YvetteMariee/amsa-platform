from fastapi import APIRouter, Depends, HTTPException
import pandas as pd
from sqlalchemy import text

from app.db.session import engine
from app.services.anomaly_detection import detect_anomalies
from app.services.security import require_roles

router = APIRouter()

ALLOWED_TABLES = {"market_data"}


@router.get("/analytics/{table_name}")
def get_analytics(
    table_name: str,
    current_user=Depends(require_roles(["ADMIN", "SUPERVISOR", "ANALYST"])),
):
    if table_name not in ALLOWED_TABLES:
        raise HTTPException(status_code=400, detail=f"Table '{table_name}' is not allowed")

    df = pd.read_sql(text(f"SELECT * FROM {table_name}"), engine)

    if df.empty:
        return {
            "table": table_name,
            "total_rows": 0,
            "average_price": 0,
            "max_price": 0,
            "min_price": 0,
            "total_volume": 0,
            "max_volume": 0,
            "price_variation": 0,
            "anomaly_count": 0,
            "risk_score": 0,
            "risk_level": "LOW",
            "ai_anomaly_count": 0,
            "ai_anomalies": [],
        }

    total_rows = len(df)
    avg_price = df["prix"].mean()
    max_price = df["prix"].max()
    min_price = df["prix"].min()
    total_volume = df["volume"].sum()
    max_volume = df["volume"].max()
    price_variation = df["prix"].iloc[-1] - df["prix"].iloc[0]

    anomaly_threshold = avg_price * 1.5
    anomalies = df[df["prix"] > anomaly_threshold]
    anomaly_count = len(anomalies)

    risk_score = 0
    if max_volume > 5000:
        risk_score += 30
    if anomaly_count > 0:
        risk_score += 40
    if price_variation > 50:
        risk_score += 30

    if risk_score >= 70:
        risk_level = "HIGH"
    elif risk_score >= 40:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    ai_detection = detect_anomalies(df)

    try:
        scores = ai_detection.get("scores")
        if scores is not None and "id" in df.columns:
            with engine.begin() as conn:
                for idx, score in scores.items():
                    row = df.loc[idx]
                    if "id" in row and row["id"] is not None:
                        stmt = text("UPDATE market_data SET anomaly_score = :score WHERE id = :id")
                        conn.execute(stmt, {"score": float(score), "id": int(row["id"])})
    except Exception:
        pass

    return {
        "table": table_name,
        "total_rows": total_rows,
        "average_price": round(avg_price, 2),
        "max_price": float(max_price),
        "min_price": float(min_price),
        "total_volume": int(total_volume),
        "max_volume": int(max_volume),
        "price_variation": float(price_variation),
        "anomaly_count": anomaly_count,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "ai_anomaly_count": ai_detection["anomaly_count"],
        "ai_anomalies": ai_detection["anomalies"],
    }
