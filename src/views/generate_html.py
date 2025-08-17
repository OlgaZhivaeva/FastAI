import asyncio
from typing import Annotated

import aiofiles
from pydantic import BaseModel, ConfigDict, SecretStr, conint
from pydantic_settings import BaseSettings, SettingsConfigDict
from starlette.responses import StreamingResponse

from reuseble_types import request_config_dict


class SiteGenerationRequest(BaseModel):
    prompt: str
    """Промпт"""

    model_config = request_config_dict | ConfigDict(
        json_schema_extra={
            "example": {
                "prompt": "Сайт любителей морских свинок",
            },
        },
    )


class AppSettings(BaseSettings):
    """Главные настройки приложения. Загружаются из .env."""
    debug_mode: bool = False
    deep_seek_api_key: SecretStr
    unsplash_client_id: SecretStr
    deep_seek_max_connections: Annotated[conint(gt=0), "Максимальное количество подключений"] | None = None
    unsplash_max_connections: Annotated[conint(gt=0), "Максимальное количество подключений"] | None = None
    timeout: Annotated[conint(gt=0), "Таймаут"] | None = None
    deepseek_base_url: str
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


class HtmlPage(BaseModel):
    html_code: str = ""
    title: str = ""


async def mock_generate_html(site_id: int, request: SiteGenerationRequest):
    """/frontend-api/{site_id}/generate"""
    settings = AppSettings()

    settings_json_format = settings.model_dump_json(indent=4)
    print(settings_json_format)

    async def html_generator():
        async with aiofiles.open("src/index.html", "rb") as f:
            while True:
                chunk = await f.read(1024)
                if not chunk:
                    break
                yield chunk
                await asyncio.sleep(1)

    return StreamingResponse(html_generator(), media_type="text/html")
