from typing import Annotated, Union

from fastapi import Query, WebSocket, WebSocketException, status


async def get_token(
    websocket: WebSocket,
    token: Annotated[Union[str, None], Query()] = None,
):
    if token is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return token
