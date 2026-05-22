from sklearn.ensemble import IsolationForest
import pandas as pd


def detect_anomalies(df):

    features = df[["prix", "volume"]]

    model = IsolationForest(
        contamination=0.1,
        random_state=42
    )

    df["anomaly"] = model.fit_predict(features)

    anomalies = df[df["anomaly"] == -1]

    return {
        "anomaly_count": len(anomalies),
        "anomalies": anomalies.to_dict(orient="records")
    }