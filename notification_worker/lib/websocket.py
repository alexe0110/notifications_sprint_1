from fastapi import WebSocket
from logging import Logger


class ConnectionManager:
    def __init__(self, logger: Logger):
        self.active_connections: dict[str, WebSocket] = {}
        self.logger = logger

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        self.logger.info(f"user_id={user_id} connected")

    def disconnect(self, user_id: str):
        del self.active_connections[user_id]
        self.logger.info(f"user_id={user_id} disconnected")

    async def send_messages_to(self, user_ids: list[str], message: str):
        for user_id in user_ids:
            if user_ws := self.active_connections[user_id]:
                await user_ws.send_text(message)
            self.logger.info(f"notification to user_id={user_id} was sent")
