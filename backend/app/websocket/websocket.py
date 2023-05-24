from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.websocket.connect_manager import ConnectionManager


manager = ConnectionManager()
router = APIRouter(prefix="/ws", tags=["ws"])


client_js_example = """
var ws = new WebSocket("ws://localhost:8080/ws/test/1")
ws.onmessage = function(event) {
    console.log(event.data)
}
ws.send("input.value")
"""


@router.websocket("/test/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
