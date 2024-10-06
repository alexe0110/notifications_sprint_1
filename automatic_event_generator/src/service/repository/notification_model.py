from datetime import datetime

from pydantic import BaseModel, Field


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
