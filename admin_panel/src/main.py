from starlette.applications import Starlette
from starlette_admin.contrib.sqla import Admin, ModelView

from src.database import engine
from src.models import Todo

app = Starlette()

# Create an empty admin interface
admin = Admin(engine, title='Tutorials: Basic')

# Adding a view for the Todo model
admin.add_view(ModelView(Todo))

# Mount admin to my app
admin.mount_to(app)
