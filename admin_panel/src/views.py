from typing import Any

from starlette.requests import Request
from starlette_admin.contrib.sqla import ModelView
from starlette_admin.exceptions import FormValidationError


class MyModelView(ModelView):
    exclude_fields_from_edit = ['created_at', 'updated_at']
    exclude_fields_from_create = ['created_at', 'updated_at']

    def can_view_details(self, request: Request) -> bool:
        return 'read' in request.state.user['roles']

    def can_create(self, request: Request) -> bool:
        return 'create' in request.state.user['roles']

    def can_edit(self, request: Request) -> bool:
        return 'edit' in request.state.user['roles']

    def can_delete(self, request: Request) -> bool:
        return 'delete' in request.state.user['roles']


class TemplateView(MyModelView):
    fields = ['id', 'name', 'content']


class NotificationView(MyModelView):
    exclude_fields_from_list = ['payload', 'created_at', 'users']

    async def validate(self, request: Request, data: dict[str, Any]) -> None:
        errors: dict[str, str] = {}

        if data.get('cron') == '' and data.get('event_at') is None:
            errors.update(dict.fromkeys(['cron', 'event_at'], 'Нужно указать event_at или cron'))
        if data.get('cron') and data.get('event_at'):
            errors.update(dict.fromkeys(['cron', 'event_at'], 'Нужно указать только одно: event_at или cron'))
        if data.get('template') is None:
            errors['template'] = 'Нужно выбрать шаблон'

        if len(errors) > 0:
            raise FormValidationError(errors)
        return await super().validate(request, data)
