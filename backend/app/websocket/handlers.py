from json import JSONDecodeError
import logging

from fastapi import (
    WebSocket,
    WebSocketDisconnect,
)
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import JWTDecodeError
from jwt.exceptions import ExpiredSignatureError

from app.websocket.connect_manager import OnlineUsersConnectionManager
from app.websocket.classes import OnlineUser
from app.websocket.exceptions import NoTokenException


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

manager = OnlineUsersConnectionManager()


async def connections_handler(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()

            if not data.get("access_token"):
                raise NoTokenException
            try:
                Authorize = AuthJWT()
                decoded_token = Authorize.get_raw_jwt(data["access_token"])

            except JWTDecodeError as e:
                await websocket.send_json({"error": "JWTDecodeError"})
                logger.exception("JWTDecodeError")
                continue

            except ExpiredSignatureError as e:
                await websocket.send_json({"error": "ExpiredSignatureError"})
                logger.exception("ExpiredSignatureError")
                continue

            if data["end_point"] == "online_users":
                online_user = OnlineUser(
                    websocket, decoded_token["user_id"], decoded_token
                )

                if data["query"] == "online":
                    manager.add(online_user)
                    await manager.users_count_changed_broadcast()

                if data["query"] == "offline":
                    manager.remove(online_user)
                    await manager.users_count_changed_broadcast()

                if data["query"] == "get_list":
                    await manager.send_online_users_list(online_user)

    except WebSocketDisconnect as e:
        logger.exception("WebSocketDisconnect")

    except JSONDecodeError as e:
        logger.exception("JSONDecodeError")

    except NoTokenException as e:
        logger.exception("NoTokenException")

    except Exception as e:
        logger.exception("exc")
        
    finally:
        manager.disconnect(websocket)
        await manager.users_count_changed_broadcast()
