from dataclasses import dataclass

from fastapi import WebSocket


@dataclass
class OnlineUser:
    websocket: WebSocket
    id: int
    data: dict
