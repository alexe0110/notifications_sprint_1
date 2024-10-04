from .abstract import AbstractTransport
from lib.websocket import ConnectionManager


class WebsocketTransport(AbstractTransport):
    def __init__(self, cm: ConnectionManager) -> None:
        self.client = cm

    async def send(self, user_ids: list[str], message: str):
        await self.client.send_messages_to(user_ids, message)
