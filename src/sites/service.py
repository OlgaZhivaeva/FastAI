import logging
from collections.abc import AsyncGenerator

import anyio
import httpx
from furl import furl
from gotenberg_api import GotenbergServerError, ScreenshotHTMLRequest
from html_page_generator import AsyncPageGenerator

from src.settings import S3, Gotenberg

logger = logging.getLogger(__name__)


async def get_screenshot(
    html_content: str,
    gotenberg_client: httpx.AsyncClient,
    gotenberg_settings: Gotenberg,
) -> bytes:
    """Сгенерировать скриншот из HTML контента, используя Gotenberg."""
    screenshot_bytes = await ScreenshotHTMLRequest(
        index_html=html_content,
        width=gotenberg_settings.width,
        format=gotenberg_settings.format,
        wait_delay=gotenberg_settings.wait_delay,
    ).asend(gotenberg_client)

    return screenshot_bytes


async def upload_to_s3(
    body: bytes | str,
    key: str,
    content_type: str,
    content_disposition: str,
    s3_client: any,
    s3_settings: S3,
) -> None:
    """Загрузить данные в MinIO S3 хранилище."""
    upload_params = {
        'Bucket': s3_settings.bucket,
        'Key': key,
        'Body': body,
        'ContentType': content_type,
        'ContentDisposition': content_disposition,
    }
    await s3_client.put_object(**upload_params)


async def generate_html_content(
    user_prompt: str,
    s3_client: any,
    s3_settings: S3,
    gotenberg_client: httpx.AsyncClient,
    gotenberg_settings: Gotenberg,
    debug_mode: bool,
) -> AsyncGenerator[str]:
    """Сгенерировать HTML контент по промпту пользователя"""
    try:
        generator = AsyncPageGenerator(debug_mode=debug_mode)

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
                key=s3_settings.key,
                content_type="text/html",
                content_disposition='attachment',
                s3_client=s3_client,
                s3_settings=s3_settings,
            )

            screenshot = await get_screenshot(html_content, gotenberg_client, gotenberg_settings)
            await upload_to_s3(
                body=screenshot,
                key='index.png',
                content_type='image/png',
                content_disposition='attachment',
                s3_client=s3_client,
                s3_settings=s3_settings,
            )
    except (httpx.ReadTimeout, httpx.ConnectTimeout, httpx.TimeoutException, httpx.HTTPStatusError) as err:
        logger.error(f"Ошибка при генерации HTML: {err}", exc_info=True)
    except GotenbergServerError as err:
        logger.error(f"Ошибка при генерации скриншота: {err}", exc_info=True)


def generate_s3_url(settings_s3: S3, file_name: str = None, disposition: str = None) -> str:
    url = furl(settings_s3.endpoint_url)
    key = file_name if file_name else settings_s3.key
    url.path = f"/{settings_s3.bucket}/{key}"

    if disposition:
        url.args['response-content-disposition'] = disposition

    return str(url)
