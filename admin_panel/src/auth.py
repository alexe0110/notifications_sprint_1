from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AdminConfig, AdminUser, AuthProvider
from starlette_admin.exceptions import FormValidationError, LoginFailed

# Ужасный костыль, понимаю что надо бы хранитть данные о пользователе в БД и в зашифрованном виде
# Но этот спринт не про это, поэтому решил не тратить время на схему аутентификации, использовал просто вариант из доки
users = {
    'manager': {
        'name': 'manager',
        'avatar': 'avatar_manager.png',
        'company_logo_url': 'logo.svg',
        'roles': ['read', 'create', 'edit', 'delete', 'action_make_published'],
    },
    'viewer': {'name': 'Viewer', 'avatar': 'avatar_viewer.png', 'roles': ['read']},
}


class MyAuthProvider(AuthProvider):
    async def login(
        self,
        username: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response,
    ) -> Response:
        if len(username) < 3:
            raise FormValidationError({'username': 'Ensure username has at least 03 characters'})

        if username in users and password == 'password':
            request.session.update({'username': username})
            return response

        raise LoginFailed('Invalid username or password')

    async def is_authenticated(self, request) -> bool:
        if request.session.get('username', None) in users:
            request.state.user = users.get(request.session['username'])
            return True

        return False

    def get_admin_config(self, request: Request) -> AdminConfig:
        return AdminConfig(
            logo_url=str(request.url_for('static', path='logo.svg')),
        )

    def get_admin_user(self, request: Request) -> AdminUser:
        user = request.state.user
        photo_url = None
        if user['avatar'] is not None:
            photo_url = request.url_for('static', path=user['avatar'])
        return AdminUser(username=user['name'], photo_url=photo_url)

    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        return response
