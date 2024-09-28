from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# class KafkaSettings(BaseSettings):
#     bootstrap_servers: list[str]
#     consumer_group: str
#     consumer_username: str | None = None
#     consumer_password: str | None = None
#     topic: str

#     producer_username: str | None = None
#     producer_password: str | None = None
#     destination_topic: str | None = None

#     model_config = SettingsConfigDict(env_prefix='KAFKA_')


class CommonSettings(BaseSettings):
    hold_transactions_file_path: str = Field(default='./data.csv', alias='HOLD_TRANSACTIONS_FILE_PATH')
    consume_batch_size: int = Field(default=100, alias='CONSUME_BATCH_SIZE')
    transaction_batch_size: int = Field(default=100, alias='TRANSACTION_BATCH_SIZE')
    default_job_interval: int = Field(default=25, alias='DEFAULT_JOB_INTERVAL')


class ELKSettings(BaseSettings):
    logstash_host: str
    logstash_port: int

    model_config = SettingsConfigDict(env_prefix='ELK_')


class NotificationSettings(BaseSettings):
    host: str
    send_url: str

    model_config = SettingsConfigDict(env_prefix='NOTIFICATION_')


class Settings(BaseSettings):
    common: CommonSettings = CommonSettings()
    notification: NotificationSettings = NotificationSettings()


settings = Settings()


# def kafka_producer() -> KafkaProducer:
#     return KafkaProducer(
#         bootstrap_servers=settings.kafka.bootstrap_servers,
#         topic=settings.kafka.destination_topic,
#     )


# def kafka_consumer() -> KafkaConsumer:
#     return KafkaConsumer(
#         bootstrap_servers=settings.kafka.bootstrap_servers,
#         topic=settings.kafka.topic,
#         group=settings.kafka.consumer_group,
#     )

# def notification_client() -> NotificationSettings:
#     return NotificationSettings()

# def clickhouse_connect() -> ClickhouseConnect:
#     return ClickhouseConnect(
#         host=settings.clickhouse.host,
#         port=settings.clickhouse.port,
#         user=settings.clickhouse.user,
#         password=settings.clickhouse.password,
#         database=settings.clickhouse.db,
#     )
