from datetime import datetime
from logging import Logger
from typing import Any
import requests


from src.lib.csv_handler import CSVHandler
from automatic_event_generator.src.service.repository.notification_repository import (
    NotificationModel,
    NotificationRepository,
)


class ServiceProcessor:
    def __init__(
        self,
        repository: NotificationRepository,
        hold_transactions_file_path: str,
        notification_service_url: str,
        logger: Logger,
    ) -> None:
        self._logger = logger
        self._repository = repository

        self._columns = list(NotificationModel.__fields__.keys())

        self._csv_handler = CSVHandler(
            columns=self._columns,
            file_path=hold_transactions_file_path,
        )

        self.notification_service_url = notification_service_url  # URL для сервиса уведомлений

    # функция, которая будет вызываться по расписанию.
    def run(self) -> None:
        # Пишем в лог, что джоб был запущен.
        self._logger.info(f'{datetime.utcnow()}: START')

        self.__remove_expired_events()

        current_time = datetime.utcnow()

        last_rows_count = 1
        while last_rows_count > 0:
            ids_worked = {row['id']: row for row in self._csv_handler.read_all_rows()}

            count_rows = len(ids_worked.keys())
            rows = self._repository.select_notifications(
                target_timestamp=current_time,
                offset=count_rows,
            )

            last_rows_count = len(rows)

            prepared_rows = []

            for row in rows:
                if row['id'] in ids_worked:
                    continue
                try:
                    self.__send_to_notification_service(row)
                    prepared_rows.append(row)
                except Exception as e:
                    self._logger.error(f'{datetime.utcnow()}: {e}')
                    continue

            self._csv_handler.write_row(prepared_rows)

        self._logger.info(f'{datetime.utcnow()}: FINISH')

    def __remove_expired_events(self) -> None:
        """Удаляет события, которые уже прошли."""

        current_time = datetime.now()

        def is_expired(row: dict[str, Any]) -> bool:
            event_time = datetime.fromisoformat(row['event_at'])
            return event_time < current_time  # Возвращает True, если событие истекло

        self._csv_handler.delete_rows(is_expired)

    def __send_to_notification_service(self, row: dict[str, Any]) -> None:
        """Отправляет событие в сервис уведомлений."""

        try:
            response = requests.post(
                self.notification_service_url,
                json=row,  # Используем JSON для отправки данных
                timeout=10,  # Устанавливаем таймаут на запрос
            )
            response.raise_for_status()  # Вызываем ошибку, если статус-код не является 2xx
            self._logger.info(f'Уведомление успешно отправлено: {response.json()}')
        except requests.exceptions.RequestException as e:
            self._logger.error(f'Ошибка при отправке уведомления: {e}')
