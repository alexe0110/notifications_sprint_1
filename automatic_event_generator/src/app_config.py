from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.lib.pg import PgConnect


class CommonSettings(BaseSettings):
    hold_transactions_file_path: str = Field(default='/etc/hold_data.csv', alias='HOLD_TRANSACTIONS_FILE_PATH')
    default_job_interval: int = Field(default=25, alias='DEFAULT_JOB_INTERVAL')


class ELKSettings(BaseSettings):
    logstash_host: str
    logstash_port: int

    model_config = SettingsConfigDict(env_prefix='ELK_')


class PgSettings(BaseSettings):
    db: str
    user: str
    password: str
    host: str
    port: int

    model_config = SettingsConfigDict(env_prefix='POSTGRES_')

    @property
    def get_dsn(self) -> str:
        return PostgresDsn.build(
            scheme='postgresql',
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            path=self.db,
        ).unicode_string()


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
        dsn=settings.pg.get_dsn,
    )
