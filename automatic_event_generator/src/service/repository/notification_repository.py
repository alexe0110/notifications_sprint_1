from datetime import datetime
import backoff

from src.lib.pg import PgConnect
from automatic_event_generator.src.service.repository.notification_model import NotificationModel


class NotificationRepository:
    TABLE_NAME = 'notifications'
    FILTER_FIELD = 'event_at'
    SORT_BY = 'ASC'
    SORT_FIELD = 'event_at'

    def __init__(self, db: PgConnect, limit: int) -> None:
        self._db = db
        self.limit = limit

    @backoff.on_exception(backoff.expo, Exception, max_tries=5)
    def select_notifications(
        self,
        target_timestamp: datetime,
        offset: int,
    ) -> list[NotificationModel]:
        columns = list(NotificationModel.__fields__.keys())

        with self._db.connection() as conn, conn.cursor() as cur:
            cur.execute(
                f"""
                    SELECT
                        {', '.join(columns)}
                    FROM {self.TABLE_NAME}
                    WHERE {self.FILTER_FIELD}::timestamp BETWEEN %(target_timestamp)s AND %(target_timestamp)s + INTERVAL '1 hour'
                    ORDER BY {self.SORT_FIELD} {self.SORT_BY}
                    LIMIT %(limit)s --Обрабатываем только одну пачку объектов.
                    OFFSET %(offset)s
                """, {
                    'target_timestamp': target_timestamp,
                    'limit': self.limit,
                    'offset': offset
                }
            )
            objs = cur.fetchall()
        return objs
