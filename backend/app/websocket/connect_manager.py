from fastapi import WebSocket

from app.settings import SETTINGS
from app.websocket.exceptions import OnlineLimitException
from app.websocket.classes import OnlineUser


class OnlineUsersConnectionManager:
    def __init__(self):
        self.online_users: list[OnlineUser] = []

    def add(self, online_user: OnlineUser):
        if len(self.online_users) >= SETTINGS.max_online_users:
            raise OnlineLimitException
        self.online_users.append(online_user)

    def remove(self, online_user: OnlineUser):
        self.online_users.remove(online_user)

    def disconnect(self, websocket: WebSocket):
        for online_user in self.online_users:
            if online_user.websocket == websocket:
                self.online_users.remove(online_user)
                break

    async def send_online_users_list(self, online_user: OnlineUser):
        await online_user.websocket.send_json(self._get_users_list())

    def _get_users_list(self):
        return [
            {
                "email": online_user.data["user_email"],
                "user_id": online_user.data["user_id"],
            }
            for online_user in self.online_users
        ]

    async def users_count_changed_broadcast(self):
        for online_user in self.online_users:
            await self.send_online_users_list(online_user)
