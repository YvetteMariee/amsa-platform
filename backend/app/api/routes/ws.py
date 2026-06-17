import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from app.services.auth_service import SECRET_KEY, ALGORITHM
import jwt

router = APIRouter()
logger = logging.getLogger(__name__)

clients: list[WebSocket] = []


@router.websocket("/ws/alerts")
async def websocket_alerts(websocket: WebSocket, token: str = Query(default="")):
    if token:
        try:
            jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.PyJWTError:
            await websocket.close(code=4001)
            return

    await websocket.accept()
    clients.append(websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        if websocket in clients:
            clients.remove(websocket)
    except Exception:
        if websocket in clients:
            clients.remove(websocket)


async def broadcast(message: dict):
    disconnected = []
    for client in clients:
        try:
            await client.send_json(message)
        except Exception:
            disconnected.append(client)
    for client in disconnected:
        if client in clients:
            clients.remove(client)
