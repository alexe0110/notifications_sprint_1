from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

from src.logger import logger
from automatic_event_generator.src.service.repository.notification_repository import MetricsRepository
from src.service.service_processor_job import ServiceProcessor

from .app_config import clickhouse_connect, kafka_consumer, settings

app = Flask(__name__)


@app.get('/health')
def health() -> str:
    return 'healthy'


proc = ServiceProcessor(
    consumer=kafka_consumer(),
    consumer_batch_size=settings.common.consume_batch_size,
    transaction_batch_size=settings.common.transaction_batch_size,
    repository=MetricsRepository(clickhouse_connect()),
    hold_transactions_file_path=settings.common.hold_transactions_file_path,
    logger=logger,
)

scheduler = BackgroundScheduler()
scheduler.add_job(func=proc.run, trigger='interval', seconds=settings.common.default_job_interval)
scheduler.start()
