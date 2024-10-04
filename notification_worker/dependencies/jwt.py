from typing import Annotated
from fastapi import Cookie, WebSocket, WebSocketException, status
import jwt
import time
from config import settings


def decode_token(token: str, secret_key: str):
    try:
        decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except jwt.PyJWTError:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)


async def get_current_user(
    websocket: WebSocket,
    access_token: Annotated[str | None, Cookie()] = None,
):

    return {'id': settings.notification.mock_user_id}
    # if not access_token:
    #     raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)

    # decoded_token = decode_token(access_token, settings.jwt.secret_key)
    # return decoded_token
