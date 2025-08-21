from typing import Annotated

import anyio
import httpx
from html_page_generator import AsyncDeepseekClient, AsyncPageGenerator, AsyncUnsplashClient
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

    async def html_generator(user_prompt: str):
        try:
            async with (
                AsyncUnsplashClient.setup(settings.unsplash_client_id, timeout=3),
                AsyncDeepseekClient.setup(settings.deep_seek_api_key, settings.deepseek_base_url),

            ):
                with anyio.CancelScope(shield=True):
                    generator = AsyncPageGenerator(debug_mode=settings.debug_mode)
                    title_saved = False
                    async for chunk in generator(user_prompt):
                        yield chunk
                        print(chunk, end="", flush=True)
                        if title_saved:
                            continue
                        if title := generator.html_page.title:
                            print(title)
                            title_saved = True

                with open("site_title_1" + '.html', 'w', encoding='utf-8') as f:
                    f.write(generator.html_page.html_code)
        except (httpx.ReadTimeout, httpx.ConnectTimeout, httpx.TimeoutException, httpx.HTTPStatusError) as err:
            print(f"Oшибка при генерации HTML: {err}")

    return StreamingResponse(html_generator(request.prompt), media_type="text/html")
