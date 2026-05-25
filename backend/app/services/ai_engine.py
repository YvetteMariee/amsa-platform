# backend/app/services/ai_engine.py

def extract_entities(text: str):
    keywords = ["BVMAC", "COSUMAF", "banque", "emetteur", "action", "obligation"]
    return [k for k in keywords if k.lower() in text.lower()]


def compute_risk_score(text: str):
    score = 0

    if "anomalie" in text.lower():
        score += 40
    if "volume suspect" in text.lower():
        score += 30
    if "chute" in text.lower():
        score += 20

    return min(score, 100)


def generate_alerts(text: str):
    alerts = []

    if "volume suspect" in text.lower():
        alerts.append("Volume anormal détecté")

    if "suspension" in text.lower():
        alerts.append("Suspension possible")

    if "anomalie" in text.lower():
        alerts.append("Anomalie détectée")

    return alerts


def analyze_document(text: str):
    return {
        "entities": extract_entities(text),
        "risk_score": compute_risk_score(text),
        "alerts": generate_alerts(text)
    }