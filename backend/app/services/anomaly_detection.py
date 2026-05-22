import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest


def _prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    cols = [c for c in ["prix", "volume"] if c in df.columns]
    features = df[cols].copy()
    # log transform to reduce skew
    for c in cols:
        features[c] = pd.to_numeric(features[c], errors="coerce").fillna(0)
        features[f"log_{c}"] = np.log1p(features[c])
    features = features.fillna(0)
    return features


def detect_anomalies(df: pd.DataFrame, contamination: float = 0.05):
    if df is None or df.empty:
        return {"anomaly_count": 0, "anomalies": [], "scores": pd.Series(dtype=float)}

    features = _prepare_features(df)

    if len(features) < 5:
        return {"anomaly_count": 0, "anomalies": [], "scores": pd.Series(dtype=float)}

    model = IsolationForest(contamination=contamination, random_state=42)
    model.fit(features)

    dec = model.decision_function(features)
    dec_min, dec_max = dec.min(), dec.max()
    if dec_max - dec_min == 0:
        norm = np.zeros_like(dec)
    else:
        norm = (dec - dec_min) / (dec_max - dec_min)
    anomaly_score = 1.0 - norm

    scores = pd.Series(anomaly_score, index=df.index)
    anomalies_idx = scores[scores > 0.75].index
    anomalies = df.loc[anomalies_idx].to_dict(orient="records")

    return {"anomaly_count": len(anomalies), "anomalies": anomalies, "scores": scores}