from starlette.requests import Request
from starlette_admin.contrib.sqla import ModelView


class MyModelView(ModelView):
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
