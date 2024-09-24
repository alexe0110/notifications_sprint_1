from sqlalchemy import create_engine
from starlette.applications import Starlette
from starlette_admin.contrib.sqla import Admin, ModelView

from models import Todo

app = Starlette()

engine = create_engine('sqlite:///kekdb', connect_args={'check_same_thread': False})

# Create an empty admin interface
admin = Admin(engine, title='Tutorials: Basic')

# Adding a view for the Todo model
admin.add_view(ModelView(Todo))

# Mount admin to my app
admin.mount_to(app)
