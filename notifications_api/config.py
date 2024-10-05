from pydantic_settings import BaseSettings, SettingsConfigDict


class KafkaSettings(BaseSettings):
    bootstrap_servers: list[str]
    topic_email_notification: str
    topic_websocket_notification: str

    model_config = SettingsConfigDict(env_prefix='KAFKA_')


class Settings(BaseSettings):
    kafka: KafkaSettings = KafkaSettings()


settings = Settings()
