from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from notifications import router as notifications_router

app = FastAPI(
    title='Notifications API',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


app.include_router(notifications_router, prefix='/api/v1/notifications', tags=['notifications'])
