from datetime import datetime
import backoff
import psycopg2.extras

from src.lib.pg import PgConnect
from src.service.repository.notification_model import NotificationModel


class NotificationRepository:
    TABLE_NAME = 'notification'
    FILTER_FIELD = 'n.event_at'
    SORT_BY = 'DESC'
    SORT_FIELD = 'n.updated_at'

    def __init__(self, db: PgConnect, limit: int) -> None:
        self._db = db
        self.limit = limit

    @backoff.on_exception(backoff.expo, Exception, max_tries=5)
    def select_notifications(
        self,
        target_timestamp: datetime,
        offset: int,
        is_cron: bool = False,
    ) -> list[NotificationModel]:
        where_sql = (
            "n.cron is not null AND n.cron != ''"
            if is_cron
            else (
                f"{self.FILTER_FIELD} is not null and {self.FILTER_FIELD} "
                "BETWEEN %(target_timestamp)s AND %(target_timestamp)s + INTERVAL '30 minutes'"
            )
        )
        order_by_sql = f'ORDER BY {self.SORT_FIELD} {self.SORT_BY}' if not is_cron else ''

        with self._db.connection() as conn, conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(
                f"""
                    SELECT
                        n.id as event_id,
                        n.type as event_type,
                        n.event_at as event_at,
                        n.cron as cron,
                        n.template_id as template_id,
                        t.name as template_name,
                        t.content as template_content,
                        n.payload as payload_for_template,
                        n.users as user_ids,
                        n.created_at as created_at,
                        n.updated_at as updated_at
                    FROM {self.TABLE_NAME} as n
                    INNER JOIN template as t ON t.id = n.template_id
                    WHERE {where_sql}
                    {order_by_sql}
                    LIMIT %(limit)s --Обрабатываем только одну пачку объектов.
                    OFFSET %(offset)s
                """,
                {'target_timestamp': target_timestamp, 'limit': self.limit, 'offset': offset},
            )
            objs = cur.fetchall()

            objs = [NotificationModel(**dict(row)) for row in objs]

        return objs
