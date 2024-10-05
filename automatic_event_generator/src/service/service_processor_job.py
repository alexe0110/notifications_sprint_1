from datetime import datetime
from logging import Logger
from typing import Any
import requests
from croniter import croniter
from pydantic import BaseModel, Field


from src.lib.csv_handler import CSVHandler
from src.service.repository.notification_repository import (
    NotificationModel,
    NotificationRepository,
)


class RequestNotification(BaseModel):
    event_id: str = Field(description='Идентификатор события')
    event_type: str = Field(description='Тип события (email)')
    event_at: datetime | None = Field(description='Время отправки события')
    template_id: str = Field(description='Идентификатор шаблона')
    template_name: str = Field(description='Название шаблона')
    template_content: str = Field(description='Содержимое шаблона')
    payload_for_template: dict = Field(description='Данные для шаблона')
    user_ids: list = Field(description='Идентификатор пользователя')
    created_at: datetime = Field(description='Время создания события')
    updated_at: datetime = Field(description='Время обновления события')

    def dict(self, *args, **kwargs) -> dict[str, Any]:
        # Получаем стандартное словарь от BaseModel
        original_dict = super().dict(*args, **kwargs)

        # Проходим по всем ключам и преобразуем datetime в строку
        for key, value in original_dict.items():
            if isinstance(value, datetime):
                original_dict[key] = value.isoformat()

        return original_dict


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
        self._logger.info('RUN JOB')
        self.send_events_by_at()
        self.send_events_by_cron()

    def send_events_by_at(self) -> None:
        # Пишем в лог, что джоб был запущен.
        self._logger.info(f'{datetime.utcnow()}: START')

        self.__remove_expired_events()

        current_time = datetime.utcnow()

        prepared_rows_count = 0
        last_rows_count = 1
        while last_rows_count > 0:
            try:
                ids_worked = {row['event_id']: True for row in self._csv_handler.read_all_rows()}
                self._logger.info(f'ids_worked{datetime.utcnow()}: {ids_worked}')

                rows = self._repository.select_notifications(
                    target_timestamp=current_time, offset=prepared_rows_count, is_cron=False
                )

                last_rows_count = len(rows)
                prepared_rows_count += last_rows_count

                for row in rows:
                    if row.event_id in ids_worked:
                        continue
                    try:
                        self.__send_to_notification_service(row)
                        self._csv_handler.write_row(row.__dict__)
                    except Exception as e:
                        self._logger.error(f'Ошибка при обработки строки {datetime.utcnow()}: {e}')
                        continue

            except Exception as e:
                last_rows_count = 0
                self._logger.error(f'{datetime.utcnow()}: {e}')
                continue

        self._logger.info(f'{datetime.utcnow()}: FINISH')

    # функция, которая будет вызываться по расписанию для отправки сообщений CRON.
    def send_events_by_cron(self) -> None:
        # Пишем в лог, что джоб был запущен.
        self._logger.info(f'{datetime.utcnow()}: START CRON')

        current_time = datetime.utcnow()

        prepared_rows_count = 0
        last_rows_count = 1
        while last_rows_count > 0:
            try:
                rows = self._repository.select_notifications(
                    target_timestamp=current_time, offset=prepared_rows_count, is_cron=True
                )

                last_rows_count = len(rows)
                prepared_rows_count += last_rows_count

                for row in rows:
                    try:
                        if row.cron is None or row.cron == '':
                            continue

                        is_run, event_at = self.__is_time_to_run(row.cron, current_time)

                        if is_run:
                            row.event_at = event_at
                            del row.cron

                            self.__send_to_notification_service(row)
                    except Exception as e:
                        self._logger.error(f'{datetime.utcnow()}: {e}')
                        continue
            except Exception as e:
                last_rows_count = 0
                self._logger.error(f'{datetime.utcnow()}: {e}')
                continue

        self._logger.info(f'{datetime.utcnow()}: FINISH CRON')

    def __remove_expired_events(self) -> None:
        """Удаляет события, которые уже прошли."""

        current_time = datetime.now()

        def is_expired(row: dict[str, Any]) -> bool:
            event_time = datetime.fromisoformat(row['event_at'])
            return event_time < current_time  # Возвращает True, если событие истекло

        self._csv_handler.delete_rows(is_expired)

    def __send_to_notification_service(self, row: dict[str, Any]) -> None:
        """Отправляет событие в сервис уведомлений."""

        notification_request = RequestNotification(**row.dict())

        try:
            response = requests.post(
                self.notification_service_url,
                json=notification_request.dict(),  # Используем JSON для отправки данных
                timeout=10,  # Устанавливаем таймаут на запрос
            )
            response.raise_for_status()  # Вызываем ошибку, если статус-код не является 2xx
            self._logger.info(f'Уведомление успешно отправлено: {response.json()}')
        except requests.exceptions.RequestException as e:
            self._logger.error(f'Ошибка Request при отправке уведомления: {e} {e.response.text}')
            raise e
        except Exception as e:
            self._logger.error(f'Общая ошибка при отправке уведомления: {e}')
            raise e

    def __is_time_to_run(self, cron_expression, current_time):
        """Проверяет, совпадает ли текущее время с cron выражением."""
        cron = croniter(cron_expression, current_time)

        # Получаем следующее время выполнения
        next_run = cron.get_next(datetime)

        # Проверяем, попадает ли текущее время в диапазон от следующего выполнения
        # до следующего выполнения + 15 секунд
        is_time = next_run - datetime.timedelta(seconds=15) <= current_time < next_run + datetime.timedelta(seconds=15)
        return is_time, next_run
