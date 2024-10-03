from pydantic_settings import BaseSettings, SettingsConfigDict


class KafkaSettings(BaseSettings):
    bootstrap_servers: list[str]
    topic: str

    model_config = SettingsConfigDict(env_prefix='KAFKA_')


class Settings(BaseSettings):
    kafka: KafkaSettings = KafkaSettings()


settings = Settings()
