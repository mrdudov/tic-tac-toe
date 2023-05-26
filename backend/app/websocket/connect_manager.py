from fastapi import WebSocket
from app.settings import SETTINGS
from app.websocket.exceptions import OnlineLimitException


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[tuple[WebSocket, str]] = []

    async def connect(self, websocket: WebSocket, token: str):
        if len(self.active_connections) >= SETTINGS.max_online_users:
            raise OnlineLimitException
        await websocket.accept()
        self.active_connections.append((websocket, token))

    def disconnect(self, websocket: WebSocket, token: str):
        self.active_connections.remove((websocket, token))

    async def send_online_users_list(self, websocket: WebSocket):
        await websocket.send_text(self._get_users_list_str())

    def _get_users_list_str(self):
        online_users_list = str([item[1] for item in self.active_connections])
        return online_users_list 
