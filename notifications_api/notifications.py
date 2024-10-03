import logging
import pickle
from datetime import datetime
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from kafka import KafkaProducer
from kafka.errors import KafkaError
from pydantic import BaseModel, Field
from config import settings
import backoff
from kafka.errors import NoBrokersAvailable

router = APIRouter()
logger = logging.getLogger(__name__)
access_token_header = HTTPBearer()


@backoff.on_exception(backoff.expo, exception=NoBrokersAvailable)
def get_kafka_producer() -> KafkaProducer:
    return KafkaProducer(bootstrap_servers=settings.kafka.bootstrap_servers)


producer = get_kafka_producer()


class NotificationModel(BaseModel):
    event_id: str = Field(description='Идентификатор события')
    event_type: str = Field(description='Тип события (email)')
    event_at: datetime | None = Field(description='Время отправки события')
    template_id: str = Field(description='Идентификатор шаблона')
    template_name: str = Field(description='Название шаблона')
    template_content: str = Field(description='Содержимое шаблона')
    payload_for_template: dict = Field(description='Данные для шаблона')
    user_ids: list = Field(description='Идентификатор пользователя')
    cron: str | None = Field(description='Запуск расписания')
    created_at: datetime = Field(description='Время создания события')
    updated_at: datetime = Field(description='Время обновления события')


@router.post('/', description='Send notification to Kafka')
async def record_notification(
        notification: NotificationModel,
        token: HTTPAuthorizationCredentials = Depends(access_token_header),
):
    try:
        result = producer.send(
            settings.kafka.topic,
            key=pickle.dumps(notification.event_type),
            value=pickle.dumps(notification.model_dump_json()),
        )
        producer.flush()
        logger.info('Сообщение доставлено в %s [partition %s]', result.get().topic, result.get().partition)
        return {'status': 'success', 'message': 'Event recorded and sent to Kafka.'}
    except KafkaError as e:
        logger.error('Ошибка доставки сообщения: %s', e)
        return HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
