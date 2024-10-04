import asyncio
from aiokafka import AIOKafkaConsumer
from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import Depends, FastAPI, WebSocket, WebSocketDisconnect

from dependencies.jwt import get_current_user
from services.notification import NotificationService
from transport.email import EmailTransport
from lib.logger import logger
from lib.websocket import ConnectionManager
from transport.websocket import WebsocketTransport
from config import settings


async def consume_email_notifications(consumer: AIOKafkaConsumer):
    service = NotificationService(
        transport=EmailTransport(
            server_conf={
                'host': settings.notification.email_server_host,
                'port': settings.notification.email_server_port
            },
            credentials={
                'user': settings.notification.email_user,
                'password': settings.notification.email_password
            },
            from_addr=settings.notification.email_from_addr
        ),
        logger=logger
    )

    try:
        async for msg in consumer:
            await service.notify(msg.value)
    except Exception as e:
        logger.error(str(e))


@asynccontextmanager
async def lifespan(_: FastAPI):
    loop = asyncio.get_event_loop()
    email_notification_consumer = AIOKafkaConsumer(
        settings.kafka.topic_email_notification,
        bootstrap_servers=','.join(settings.kafka.bootstrap_servers),
        group_id="email_notification_group",
        client_id="email_notification_client",
        loop=loop
    )
    ws_notification_consumer = AIOKafkaConsumer(
        settings.kafka.topic_websocket_notification,
        bootstrap_servers=','.join(settings.kafka.bootstrap_servers),
        group_id="websocket_notification_group",
        client_id="websocket_notification_client",
        loop=loop
    )
    await ws_notification_consumer.start()
    await email_notification_consumer.start()
    asyncio.ensure_future(consume_email_notifications(email_notification_consumer))
    yield {
        'ws_notification_consumer': ws_notification_consumer,
        'ws_connection_manager': ConnectionManager(logger=logger)
    }
    await email_notification_consumer.stop()
    await ws_notification_consumer.stop()


app = FastAPI(
    debug=True,
    lifespan=lifespan,
)


@app.get('/healthz')
async def health():
    return {"message": "ok"}


@app.websocket("/ws_notification")
async def ws_notification(websocket: WebSocket, user: Annotated[dict, Depends(get_current_user)]):
    consumer: AIOKafkaConsumer = websocket.state.ws_notification_consumer
    connection_manager: ConnectionManager = websocket.state.ws_connection_manager
    service = NotificationService(
        transport=WebsocketTransport(connection_manager),
        logger=logger
    )
    await connection_manager.connect(user['id'], websocket)

    try:
        async for msg in consumer:
            await service.notify(msg.value)
    except WebSocketDisconnect:
        connection_manager.disconnect(user['id'])
    except Exception as e:
        logger.error(str(e))
