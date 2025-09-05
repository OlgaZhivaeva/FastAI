from typing import Annotated, Literal

from pydantic import AnyHttpUrl, BaseModel, SecretStr, conint
from pydantic_settings import BaseSettings, SettingsConfigDict


class DeepSeek(BaseModel):
    api_key: SecretStr
    max_connections: Annotated[conint(gt=0), "Максимальное количество подключений"] | None = None
    base_url: str


class Unsplash(BaseModel):
    client_id: SecretStr
    max_connections: Annotated[conint(gt=0), "Максимальное количество подключений"] | None = None


class S3(BaseModel):
    endpoint_url: str
    aws_access_key_id: str
    aws_secret_access_key: str
    bucket: str
    key: str
    max_pool_connections: Annotated[conint(gt=0), "Максимальное количество подключений"] = 50
    connect_timeout: Annotated[conint(gt=0), "Таймаут подключения"] = 10
    read_timeout: Annotated[conint(gt=0), "Таймаут чтения"] = 30


class Gotenberg(BaseModel):
    base_url: AnyHttpUrl
    timeout: Annotated[conint(gt=0), "Таймаут"] = 15
    width: Annotated[conint(gt=0), "Ширина скриншота"] = 1000
    format: Literal["jpeg", "png", "webp"] = "png"
    wait_delay: Annotated[conint(gt=0), "Время ожидания"] = 5


class AppSettings(BaseSettings):
    """Главные настройки приложения. Загружаются из .env."""
    deep_seek: DeepSeek
    unsplash: Unsplash
    s3: S3
    gotenberg: Gotenberg
    debug_mode: bool = False
    timeout: Annotated[conint(gt=0), "Таймаут"] | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter='__',
    )
