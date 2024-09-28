from pydantic import Field, PostgresDsn, RedisDsn, field_validator
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    USER: str
    PASSWORD: str
    HOST: str
    PORT: int
    DB: str
    URL: str | None = None

    model_config = SettingsConfigDict(env_prefix='POSTGRES_')

    @field_validator("URL", mode="before")
    @classmethod
    def assemble_connection_url(cls, v: str | None, info: FieldValidationInfo) -> str:
        if isinstance(v, str):
            return v

        return PostgresDsn.build(  # type: ignore
            scheme="postgresql+asyncpg",
            username=info.data.get("USER"),
            password=info.data.get("PASSWORD"),
            host=info.data.get("HOST"),
            port=info.data.get("PORT"),
            path=info.data.get("DB"),
        ).unicode_string()


class JwtSettings(BaseSettings):
    public_key: str

    model_config = SettingsConfigDict(env_prefix='JWT_')


class Settings(BaseSettings):
    jwt: JwtSettings = JwtSettings()
    pg: PostgresSettings = PostgresSettings()


settings = Settings()
