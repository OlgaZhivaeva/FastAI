import logging
from collections.abc import AsyncGenerator

import anyio
import httpx
from fastapi import Request
from furl import furl
from gotenberg_api import GotenbergServerError, ScreenshotHTMLRequest
from html_page_generator import AsyncPageGenerator

logger = logging.getLogger(__name__)


async def get_screenshot(html_content: str, http_request: Request) -> bytes:
    """Сгенерировать скриншот из HTML контента, используя Gotenberg."""
    gotenberg_client = http_request.app.state.gotenberg_client
    screenshot_bytes = await ScreenshotHTMLRequest(
        index_html=html_content,
        width=http_request.app.state.settings.gotenberg.width,
        format=http_request.app.state.settings.gotenberg.format,
        wait_delay=http_request.app.state.settings.gotenberg.wait_delay,
    ).asend(gotenberg_client)

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


async def generate_html_content(user_prompt: str, http_request: Request) -> AsyncGenerator[str]:
    """Сгенерировать HTML контент по промпту пользователя"""
    try:
        s3 = http_request.app.state.settings.s3

        generator = AsyncPageGenerator(debug_mode=http_request.app.state.settings.debug_mode)

        with anyio.CancelScope(shield=True):
            title_saved = False
            async for chunk in generator(user_prompt):
                yield chunk
                if title_saved:
                    continue
                if generator.html_page.title:
                    title_saved = True

            html_content = generator.html_page.html_code
            await upload_to_s3(
                body=html_content,
                bucket=s3.bucket,
                key=s3.key,
                content_type="text/html",
                content_disposition='attachment',
                http_request=http_request,
            )

            screenshot = await get_screenshot(html_content, http_request)
            await upload_to_s3(
                body=screenshot,
                bucket=s3.bucket,
                key='index.png',
                content_type='image/png',
                content_disposition='attachment',
                http_request=http_request,
            )
    except (httpx.ReadTimeout, httpx.ConnectTimeout, httpx.TimeoutException, httpx.HTTPStatusError) as err:
        logger.error(f"Ошибка при генерации HTML: {err}", exc_info=True)
    except GotenbergServerError as err:
        logger.error(f"Ошибка при генерации скриншота: {err}", exc_info=True)


def build_url(http_request: Request, file_name: str = None, disposition: str = None) -> str:
    s3 = http_request.app.state.settings.s3

    url = furl(s3.endpoint_url)
    key = file_name if file_name else s3.key
    url.path = f"/{s3.bucket}/{key}"

    if disposition:
        url.args['response-content-disposition'] = disposition

    return str(url)
