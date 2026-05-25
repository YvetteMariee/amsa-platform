from app.api.routes.ws import broadcast


def detect_and_broadcast(ai_result, filename):

    alerts = ai_result.get("alerts", [])
    risk = ai_result.get("risk_score", 0)

    event = {
        "file": filename,
        "risk_score": risk,
        "alerts": alerts,
        "level": "HIGH" if risk > 70 else "MEDIUM" if risk > 30 else "LOW"
    }

    # push temps réel
    import asyncio
    asyncio.create_task(broadcast(event))

    return event