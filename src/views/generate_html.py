from typing import Annotated

import aioboto3
import anyio
import httpx
from aiobotocore.config import AioConfig
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


config = AioConfig(
    max_pool_connections=50,  # 50 параллельных операций
    connect_timeout=10,  # 10 сек на подключение
    read_timeout=30,  # 30 сек на чтение данных
)


async def upload_html_page(html_content):
    async with aioboto3.Session().client(
            's3',
            config=config,
            region_name='us-east-1',
            endpoint_url='http://127.0.0.1:9000',
            aws_access_key_id='minioadmin',
            aws_secret_access_key='minioadmin',
    ) as client:
        upload_params = {
            'Bucket': 'html-bucket',
            'Key': 'index.html',  # Путь в S3
            'Body': html_content,  # Данные
            'ContentType': 'text/html',  # MIME-тип
            'ContentDisposition': 'attachment',
        }
        await client.put_object(**upload_params)


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

                html_content = generator.html_page.html_code
                await upload_html_page(html_content)

        except (httpx.ReadTimeout, httpx.ConnectTimeout, httpx.TimeoutException, httpx.HTTPStatusError) as err:
            print(f"Oшибка при генерации HTML: {err}")

    return StreamingResponse(html_generator(request.prompt), media_type="text/html")
