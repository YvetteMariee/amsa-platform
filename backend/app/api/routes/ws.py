from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

clients = []


@router.websocket("/ws/alerts")
async def websocket_alerts(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)

    try:
        while True:
            await websocket.receive_text()  # keep alive
    except WebSocketDisconnect:
        clients.remove(websocket)


async def broadcast(message: dict):
    for client in clients:
        try:
            await client.send_json(message)
        except:
            clients.remove(client)