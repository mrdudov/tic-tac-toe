from typing import Annotated

from fastapi import (
    Depends,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi_jwt_auth import AuthJWT

from app.websocket.connect_manager import OnlineUsersConnectionManager
from app.websocket.functions import get_token
from app.websocket.classes import OnlineUser


manager = OnlineUsersConnectionManager()


html = """
    let ws = new WebSocket("ws://tic-tac-toe.mrdudov.ru/api/v1/ws")
    let ws = new WebSocket("ws://localhost:8080/ws")
    ws.onmessage = function(event) { console.log(event.data) }
    ws.send('get_online_users')
    ws.close()
"""


async def connections_handler(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")


async def online_users(
    *,
    websocket: WebSocket,
    token: Annotated[str, Depends(get_token)],
    Authorize: AuthJWT = Depends(),
):
    Authorize.jwt_required("websocket", token=token)
    decoded_token = Authorize.get_raw_jwt(token)
    online_user = OnlineUser(websocket, decoded_token["user_id"], decoded_token)
    await manager.connect(online_user)
    await manager.users_count_changed_broadcast()
    try:
        while True:
            data = await websocket.receive_text()
            if data == "get_online_users":
                await manager.send_online_users_list(online_user)
    except WebSocketDisconnect:
        manager.disconnect(online_user)
        await manager.users_count_changed_broadcast()
