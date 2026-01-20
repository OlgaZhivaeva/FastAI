import logging
from collections.abc import AsyncGenerator

import anyio
import httpx
from fastapi import HTTPException, Request, status
from furl import furl
from gotenberg_api import GotenbergServerError, ScreenshotHTMLRequest
from html_page_generator import AsyncPageGenerator
from starlette.responses import StreamingResponse

from src.reuseble_types import SITE_EXAMPLE
from src.settings import S3, Gotenberg

from .schemas import CreateSiteRequest, SiteGenerationRequest

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
    site_id: int,
    user_prompt: str,
    app_state: any,
) -> AsyncGenerator[str]:
    """Сгенерировать HTML контент по промпту пользователя"""
    s3_client = app_state.s3_client
    s3_settings = app_state.settings.s3
    gotenberg_client = app_state.gotenberg_client
    gotenberg_settings = app_state.settings.gotenberg
    debug_mode = app_state.settings.debug_mode
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
                key=f"{site_id}/{s3_settings.key}",
                content_type="text/html",
                content_disposition="attachment",
                s3_client=s3_client,
                s3_settings=s3_settings,
            )

            screenshot = await get_screenshot(html_content, gotenberg_client, gotenberg_settings)
            await upload_to_s3(
                body=screenshot,
                key=f"/{site_id}/index.png",
                content_type="image/png",
                content_disposition="attachment",
                s3_client=s3_client,
                s3_settings=s3_settings,
            )
    except (httpx.ReadTimeout, httpx.ConnectTimeout, httpx.TimeoutException, httpx.HTTPStatusError) as err:
        logger.error(f"Ошибка при генерации HTML: {err}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Сервис временно недоступен. Попробуйте позже.",
        )
    except GotenbergServerError as err:
        logger.error(f"Ошибка при генерации скриншота: {err}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при генерации скриншота.",
        )


def generate_s3_url(site_id: int, s3_settings: S3, file_name: str = None, disposition: str = None) -> str:
    url = furl(s3_settings.endpoint_url)
    key = f"{site_id}/{file_name}" if file_name else f"{site_id}/{s3_settings.key}"
    url.path = f"/{s3_settings.bucket}/{key}"

    if disposition:
        url.args['response-content-disposition'] = disposition

    return str(url)


def mock_create_site(request: CreateSiteRequest):
    """post /frontend-api/sites/create"""
    return {
        **SITE_EXAMPLE,
        "prompt": request.prompt,
        "title": request.title,
    }


def mock_get_site(site_id: int, http_request: Request):
    """get /frontend-api/sites/{site_id}"""
    s3_settings = http_request.app.state.settings.s3

    return {
        **SITE_EXAMPLE,
        "html_code_download_url": generate_s3_url(site_id, s3_settings, disposition="attachment"),
        "html_code_url": generate_s3_url(site_id, s3_settings),
        "id": site_id,
        "screenshot_url": generate_s3_url(site_id, s3_settings, file_name="index.png", disposition="inline"),
    }


def mock_get_user_sites(http_request: Request):
    """get /frontend-api/sites/my"""
    s3_settings = http_request.app.state.settings.s3
    site_id = 1
    return {
        "sites":
        [
            {
                **SITE_EXAMPLE,
                "html_code_download_url": generate_s3_url(site_id, s3_settings, disposition="attachment"),
                "html_code_url": generate_s3_url(site_id, s3_settings, disposition="inline"),
                "screenshot_url": generate_s3_url(site_id, s3_settings, file_name="index.png"),
            },
        ],
    }


async def generate_html_stream(
    site_id: int,
    request: SiteGenerationRequest,
    http_request: Request,
) -> StreamingResponse:
    """post /frontend-api/sites/{site_id}/generate"""

    return StreamingResponse(
        generate_html_content(
            site_id=site_id,
            user_prompt=request.prompt,
            app_state=http_request.app.state,
        ),
        media_type='text/html',
    )
