from pydantic import BaseModel, PostgresDsn
from contextlib import contextmanager
from typing import Generator

import psycopg
from psycopg import Connection


class PgConnect(BaseModel):
    host: str
    port: int
    db_name: str
    user: str
    password: str
    sslmode: str | None = 'disable'

    @property
    def dsn(self) -> PostgresDsn:
        """Создает строку подключения DSN для PostgreSQL."""
        return PostgresDsn.build(
            scheme='postgresql',
            user=self.user,
            password=self.password,
            host=self.host,
            port=str(self.port),
            path=f'/{self.db_name}',
            query={'sslmode': self.sslmode}
        )

    @contextmanager
    def connection(self) -> Generator[Connection, None, None]:
        """Управляет подключением к базе данных."""
        conn = psycopg.connect(str(self.dsn))
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()