from datetime import datetime

from pydantic import BaseModel, Field


class NotificationModel(BaseModel):
    event_id: str = Field(description='Идентификатор события')
    event_type: str = Field(description='Тип события (email)')
    created_at: datetime = Field(description='Время создания события')
    event_at: datetime = Field(description='Время срабатывания события')
    template_id: str = Field(description='Идентификатор шаблона')
    payload_for_template: dict = Field(description='Данные для шаблона')
    user_id: str = Field(description='Идентификатор пользователя')
