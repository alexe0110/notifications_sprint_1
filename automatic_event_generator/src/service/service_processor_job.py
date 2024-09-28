from datetime import datetime
from logging import Logger
from typing import Any

from src.lib.csv_handler import CSVHandler
from src.lib.kafka_connect import KafkaConsumer
from automatic_event_generator.src.service.repository.notification_repository import NotificationModel, NotificationRepository

from lib.pg import PgConnect


class ServiceProcessor:
    def __init__(
        self,
        repository: NotificationRepository,
        consumer_batch_size: int,
        transaction_batch_size: int,
        hold_transactions_file_path: str,
        logger: Logger,
    ) -> None:
        self._logger = logger
        self._repository = repository
        self._consumer_batch_size = consumer_batch_size
        self._transaction_batch_size = transaction_batch_size

        self._columns = list(NotificationModel.__fields__.keys())

        self._csv_handler = CSVHandler(
            columns=self._columns,
            file_path=hold_transactions_file_path,
        )

    # функция, которая будет вызываться по расписанию.
    def run(self) -> None:
        # Пишем в лог, что джоб был запущен.
        self._logger.info(f'{datetime.utcnow()}: START')
        self._csv_handler.clear_file()



        last_rows = 1
        while last_rows > 0:
            count_rows = self._csv_handler.count_rows()
            rows = self._repository.select_notifications(
                target_timestamp=datetime.utcnow(),
                offset=count_rows,
            )
            self._csv_handler.write_row(rows)


            last_rows = len(rows)

            # дописать

        self._logger.info(f'{datetime.utcnow()}: FINISH')
