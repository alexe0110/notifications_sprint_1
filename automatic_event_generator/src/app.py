from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

from src.logger import logger
from automatic_event_generator.src.service.repository.notification_repository import NotificationRepository
from src.service.service_processor_job import ServiceProcessor

from src.app_config import settings, pg_connect

app = Flask(__name__)


@app.get('/health')
def health() -> str:
    return 'healthy'


proc = ServiceProcessor(
    repository=NotificationRepository(
        pg=pg_connect(),
        limit=settings.limit.select_transaction,
    ),
    notification_service_url=settings.notification.notification_service_url,
    hold_transactions_file_path=settings.common.hold_transactions_file_path,
    logger=logger,
)

scheduler = BackgroundScheduler()
scheduler.add_job(func=proc.run, trigger='interval', seconds=settings.common.default_job_interval)
scheduler.start()
