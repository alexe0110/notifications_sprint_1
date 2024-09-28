from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
from starlette_admin.contrib.sqla import Admin

from src.auth import MyAuthProvider
from src.database import engine
from src.models import Notification, Template
from src.views import NotificationView, TemplateView

app = Starlette(
    routes=[Mount('/static', app=StaticFiles(directory='static'), name='static')],
)

admin = Admin(
    engine,
    title='Notifications Admin',
    base_url='/admin',
    statics_dir='static',
    login_logo_url='/admin/statics/logo.svg',  # base_url + '/statics/' + path_to_the_file
    auth_provider=MyAuthProvider(),
    middlewares=[Middleware(SessionMiddleware, secret_key='my_super_secret_key')],
)

admin.add_view(TemplateView(Template, label='Шаблоны'))
admin.add_view(NotificationView(Notification, label='Уведомления'))

admin.mount_to(app)
