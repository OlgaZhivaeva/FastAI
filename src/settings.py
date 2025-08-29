from typing import Annotated

from pydantic import BaseModel, SecretStr, conint
from pydantic_settings import BaseSettings, SettingsConfigDict


class DeepSeek(BaseModel):
    api_key: SecretStr
    max_connections: Annotated[conint(gt=0), "Максимальное количество подключений"] | None = None
    base_url: str


class Unsplash(BaseModel):
    client_id: SecretStr
    max_connections: Annotated[conint(gt=0), "Максимальное количество подключений"] | None = None


class Minio(BaseModel):
    endpoint_url: str
    aws_access_key_id: str
    aws_secret_access_key: str
    bucket: str
    key: str


class AppSettings(BaseSettings):
    """Главные настройки приложения. Загружаются из .env."""
    deep_seek: DeepSeek
    unsplash: Unsplash
    minio: Minio
    debug_mode: bool = False
    timeout: Annotated[conint(gt=0), "Таймаут"] | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter='__',
    )
