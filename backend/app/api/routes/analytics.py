from fastapi import APIRouter
import pandas as pd
from sqlalchemy import text

from app.db.session import engine
from app.services.anomaly_detection import detect_anomalies

router = APIRouter()


@router.get("/analytics/{table_name}")
def get_analytics(table_name: str):

    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, engine)

    # =====================
    # INDICATEURS METIER
    # =====================
    total_rows = len(df)

    avg_price = df["prix"].mean()
    max_price = df["prix"].max()
    min_price = df["prix"].min()

    total_volume = df["volume"].sum()
    max_volume = df["volume"].max()

    price_variation = df["prix"].iloc[-1] - df["prix"].iloc[0]

    # =====================
    # ANOMALIE SIMPLE (RULE-BASED)
    # =====================
    anomaly_threshold = avg_price * 1.5
    anomalies = df[df["prix"] > anomaly_threshold]
    anomaly_count = len(anomalies)

    # =====================
    # SCORING RISQUE
    # =====================
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

    # =====================
    # IA ANOMALY DETECTION
    # =====================
    ai_detection = detect_anomalies(df)

    # persist anomaly scores back to DB when possible
    try:
        scores = ai_detection.get("scores")
        if scores is not None and "id" in df.columns:
            conn = engine.connect()
            for idx, score in scores.items():
                row = df.loc[idx]
                if "id" in row and row["id"] is not None:
                    stmt = text("UPDATE market_data SET anomaly_score = :score WHERE id = :id")
                    conn.execute(stmt, {"score": float(score), "id": int(row["id"])})
            conn.close()
    except Exception:
        pass

    # =====================
    # RETURN FINAL PIPELINE
    # =====================
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
        "ai_anomalies": ai_detection["anomalies"]
    }