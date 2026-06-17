import asyncio
import logging
from app.api.routes.ws import broadcast

logger = logging.getLogger(__name__)


def detect_and_broadcast(ai_result, filename):
    alerts = ai_result.get("alerts", [])
    risk = ai_result.get("risk_score", 0)

    event = {
        "file": filename,
        "risk_score": risk,
        "alerts": alerts,
        "level": "HIGH" if risk > 70 else "MEDIUM" if risk > 30 else "LOW",
    }

    try:
        loop = asyncio.get_running_loop()
        loop.create_task(broadcast(event))
    except RuntimeError:
        logger.warning("No running event loop, skipping broadcast")

    return event
