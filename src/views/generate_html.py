from datetime import datetime

import anyio
import httpx
from fastapi import Request
from gotenberg_api import GotenbergServerError, ScreenshotHTMLRequest
from html_page_generator import AsyncDeepseekClient, AsyncPageGenerator, AsyncUnsplashClient
from pydantic import BaseModel, ConfigDict
from starlette.responses import StreamingResponse

from reuseble_types import request_config_dict


class SiteGenerationRequest(BaseModel):
    prompt: str
    """Промпт"""

    model_config = request_config_dict | ConfigDict(
        json_schema_extra={
            "example": {
                "prompt": "Сайт любителей играть в домино",
            },
        },
    )


async def get_screenshot(html_content: str, http_request: Request) -> bytes | None:
    """Сгенерировать скриншот из HTML контента, используя Gotenberg."""
    try:
        async with httpx.AsyncClient(
            base_url=str(http_request.app.state.settings.gotenberg.base_url),
            timeout=http_request.app.state.settings.gotenberg.timeout,
        ) as client:
            screenshot_bytes = await ScreenshotHTMLRequest(
                index_html=html_content,
                width=http_request.app.state.settings.gotenberg.width,
                format=http_request.app.state.settings.gotenberg.format,
                wait_delay=http_request.app.state.settings.gotenberg.wait_delay,
            ).asend(client)

    except GotenbergServerError as err:
        print(f"Ошибка при генерации скриншота: {err}")
        screenshot_bytes = None
    return screenshot_bytes


async def upload_screenshot(screenshot: bytes, http_request: Request) -> None:
    """Загрузить скриншот в MinIO S3 хранилище."""
    upload_params = {
        'Bucket': http_request.app.state.settings.s3.bucket,
        'Key': "index.png",
        'Body': screenshot,
        'ContentType': 'image/png',
        'ContentDisposition': 'attachment',
    }
    await http_request.app.state.s3_client.put_object(**upload_params)


async def upload_html_page(html_content: str, http_request: Request) -> None:
    """Загрузить HTML контент в MinIO S3 хранилище."""
    upload_params = {
        'Bucket': http_request.app.state.settings.s3.bucket,
        'Key': http_request.app.state.settings.s3.key,
        'Body': html_content,
        'ContentType': 'text/html',
        'ContentDisposition': 'attachment',
    }
    await http_request.app.state.s3_client.put_object(**upload_params)


async def mock_generate_html(
    site_id: int,
    request: SiteGenerationRequest,
    http_request: Request,
) -> StreamingResponse:
    """post /frontend-api/{site_id}/generate"""
    async def html_generator(user_prompt: str):
        try:
            with anyio.CancelScope(shield=True):
                async with (
                    AsyncUnsplashClient.setup(
                        http_request.app.state.settings.unsplash.client_id,
                        timeout=3,
                    ),
                    AsyncDeepseekClient.setup(
                        http_request.app.state.settings.deep_seek.api_key,
                        http_request.app.state.settings.deep_seek.base_url,
                    ),
                ):
                    generator = AsyncPageGenerator(debug_mode=http_request.app.state.settings.debug_mode)
                    title_saved = False
                    async for chunk in generator(user_prompt):
                        yield chunk
                        print(chunk, end="", flush=True)
                        if title_saved:
                            continue
                        if title := generator.html_page.title:
                            print(title)
                            http_request.app.state.title = title
                            title_saved = True

                html_content = generator.html_page.html_code
                await upload_html_page(html_content, http_request)

                screenshot = await get_screenshot(html_content, http_request)
                if screenshot:
                    await upload_screenshot(screenshot, http_request)

                http_request.app.state.user_prompt = user_prompt
                http_request.app.state.created_at = datetime.now()

        except (httpx.ReadTimeout, httpx.ConnectTimeout, httpx.TimeoutException, httpx.HTTPStatusError) as err:
            print(f"Ошибка при генерации HTML: {err}")

    return StreamingResponse(html_generator(request.prompt), media_type="text/html")
