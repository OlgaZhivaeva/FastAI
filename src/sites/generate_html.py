import logging
from collections.abc import AsyncIterator
from datetime import datetime

import anyio
import httpx
from fastapi import Request
from gotenberg_api import GotenbergServerError, ScreenshotHTMLRequest
from html_page_generator import AsyncPageGenerator
from pydantic import BaseModel, ConfigDict
from starlette.responses import StreamingResponse

from src.reuseble_types import request_config_dict

logger = logging.getLogger(__name__)


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


async def get_screenshot(html_content: str, http_request: Request) -> bytes:
    """Сгенерировать скриншот из HTML контента, используя Gotenberg."""
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

    return screenshot_bytes


async def upload_to_s3(
    body: bytes | str,
    bucket: str,
    key: str,
    content_type: str,
    content_disposition: str,
    http_request: Request,
) -> None:
    """Загрузить данные в MinIO S3 хранилище."""
    upload_params = {
        'Bucket': bucket,
        'Key': key,
        'Body': body,
        'ContentType': content_type,
        'ContentDisposition': content_disposition,
    }
    await http_request.app.state.s3_client.put_object(**upload_params)


async def generate_html_content(user_prompt: str, http_request: Request) -> AsyncIterator[None]:
    generator = AsyncPageGenerator(debug_mode=http_request.app.state.settings.debug_mode)
    title_saved = False
    async for chunk in generator(user_prompt):
        yield chunk
        if title_saved:
            continue
        if title := generator.html_page.title:
            http_request.app.state.title = title
            title_saved = True

    html_content = generator.html_page.html_code
    await upload_to_s3(
        body=html_content,
        bucket=http_request.app.state.settings.s3.bucket,
        key=http_request.app.state.settings.s3.key,
        content_type="text/html",
        content_disposition='attachment',
        http_request=http_request,
    )

    http_request.app.state.user_prompt = user_prompt
    http_request.app.state.created_at = datetime.now()
    screenshot = await get_screenshot(html_content, http_request)
    await upload_to_s3(
        body=screenshot,
        bucket=http_request.app.state.settings.s3.bucket,
        key='index.png',
        content_type='image/png',
        content_disposition='attachment',
        http_request=http_request,
    )


async def generate_html_stream(
    site_id: int,
    request: SiteGenerationRequest,
    http_request: Request,
) -> StreamingResponse:
    """post /frontend-api/{site_id}/generate"""
    try:
        with anyio.CancelScope(shield=True):
            generate_html_content(user_prompt=request.prompt, http_request=http_request)
    except (httpx.ReadTimeout, httpx.ConnectTimeout, httpx.TimeoutException, httpx.HTTPStatusError) as err:
        logger.error(f"Ошибка при генерации HTML: {err}", exc_info=True)
    except GotenbergServerError as err:
        logger.error(f"Ошибка при генерации скриншота: {err}", exc_info=True)

    return StreamingResponse(
        generate_html_content(user_prompt=request.prompt, http_request=http_request),
        media_type='text/html',
    )
