from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    user: str
    password: str
    host: str
    port: int
    db: str
    url: str | None = None

    model_config = SettingsConfigDict(env_prefix='POSTGRES_')

    def get_dsn(self) -> str:
        return PostgresDsn.build(
            scheme='postgresql+psycopg2',
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            path=self.db,
        ).unicode_string()


class JwtSettings(BaseSettings):
    public_key: str

    model_config = SettingsConfigDict(env_prefix='JWT_')


class Settings(BaseSettings):
    jwt: JwtSettings = JwtSettings()
    pg: PostgresSettings = PostgresSettings()


settings = Settings()
