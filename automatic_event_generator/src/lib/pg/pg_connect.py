from pydantic import BaseModel, PostgresDsn
from contextlib import contextmanager
from typing import Generator

import psycopg2
from psycopg2 import connect


class PgConnect(BaseModel):
    dsn: PostgresDsn

    @contextmanager
    def connection(self) -> Generator[connect, None, None]:
        """Управляет подключением к базе данных."""
        conn = psycopg2.connect(str(self.dsn))
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
