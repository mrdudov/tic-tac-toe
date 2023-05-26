from typing import Annotated

from fastapi import (
    Depends,
    WebSocket,
    APIRouter,
    WebSocketDisconnect,
)
from fastapi.responses import HTMLResponse
from fastapi_jwt_auth import AuthJWT

from app.websocket.connect_manager import ConnectionManager
from app.websocket.functions import get_token
from app.websocket.exceptions import NoTokenException


manager = ConnectionManager()
router = APIRouter(prefix="/ws", tags=["ws"])


html = """
    var url = "ws://localhost:8080/ws"
    var token = "some_token"
    ws = new WebSocket(`${url}/online_users?token=${token}`)
    ws.onmessage = function(event) {
        console.log(event.data)
    }

    ws.send('get_online_users')
"""


@router.get("/")
async def get():
    return HTMLResponse(html)


@router.websocket("/online_users")
async def websocket_endpoint(
    *,
    websocket: WebSocket,
    token: Annotated[str, Depends(get_token)],
):
    if token == "":
        raise NoTokenException

    print(f"{token=}")
    await manager.connect(websocket, token)
    try:
        while True:
            data = await websocket.receive_text()
            if data == "get_online_users":
                await manager.send_online_users_list(websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket, token)
