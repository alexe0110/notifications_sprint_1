from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv('.env')


class KafkaSettings(BaseSettings):
    bootstrap_servers: list[str]
    topic_email_notification: str
    topic_websocket_notification: str

    model_config = SettingsConfigDict(env_prefix='KAFKA_')


class JwtSettings(BaseSettings):
    public_key: str

    model_config = SettingsConfigDict(env_prefix='JWT_')


class NotificationSettings(BaseSettings):
    email_server_host: str
    email_server_port: str
    email_user: str
    email_password: str
    email_from_addr: str
    mock_user_id: str
    mock_email_to: str

    model_config = SettingsConfigDict(env_prefix='WORKER_')


class Settings(BaseSettings):
    jwt: JwtSettings = JwtSettings()
    notification: NotificationSettings = NotificationSettings()
    kafka: KafkaSettings = KafkaSettings()


settings = Settings()
