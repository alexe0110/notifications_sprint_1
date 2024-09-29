from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.lib.pg import PgConnect


class CommonSettings(BaseSettings):
    hold_transactions_file_path: str = Field(default='./data.csv', alias='HOLD_TRANSACTIONS_FILE_PATH')
    default_job_interval: int = Field(default=25, alias='DEFAULT_JOB_INTERVAL')


class ELKSettings(BaseSettings):
    logstash_host: str
    logstash_port: int

    model_config = SettingsConfigDict(env_prefix='ELK_')


class PgSettings(BaseSettings):
    dbname: str
    user: str
    password: str
    host: str
    port: int

    model_config = SettingsConfigDict(env_prefix='PG_')


class LimitSettings(BaseSettings):
    select_transaction: int = Field(default=100)

    model_config = SettingsConfigDict(env_prefix='LIMIT_')


class NotificationSettings(BaseSettings):
    host: str
    port: int
    send_url: str

    @property
    def notification_service_url(self) -> str:
        return f'http://{self.host}:{self.port}/{self.send_url}'

    model_config = SettingsConfigDict(env_prefix='NOTIFICATION_')


class Settings(BaseSettings):
    common: CommonSettings = CommonSettings()
    limit: LimitSettings = LimitSettings()
    notification: NotificationSettings = NotificationSettings()
    pg: PgSettings = PgSettings()


settings = Settings()


def pg_connect() -> PgConnect:
    return PgConnect(
        dbname=settings.pg.dbname,
        user=settings.pg.user,
        password=settings.pg.password,
        host=settings.pg.host,
        port=settings.pg.port,
    )
