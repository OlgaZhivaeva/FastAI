from typing import Annotated, Literal

from pydantic import AnyHttpUrl, BaseModel, PositiveInt, SecretStr, conint
from pydantic_settings import BaseSettings, SettingsConfigDict


class DeepSeek(BaseModel):
    api_key: SecretStr
    max_connections: PositiveInt | None = None
    base_url: AnyHttpUrl


class Unsplash(BaseModel):
    client_id: SecretStr
    max_connections: PositiveInt | None = None
    timeout: PositiveInt = 3


class S3(BaseModel):
    endpoint_url: AnyHttpUrl
    aws_access_key_id: str
    aws_secret_access_key: str
    bucket: str
    key: str
    max_pool_connections: PositiveInt = 50
    connect_timeout: PositiveInt = 10
    read_timeout: PositiveInt = 30


class Gotenberg(BaseModel):
    base_url: AnyHttpUrl
    timeout: PositiveInt = 15
    width: PositiveInt = 1000
    format: Literal["jpeg", "png", "webp"] = "png"
    wait_delay: PositiveInt = 5


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
