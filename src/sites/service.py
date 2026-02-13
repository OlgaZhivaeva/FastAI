import logging
from collections.abc import AsyncGenerator

import anyio
import boto3
import httpx
from gotenberg_api import GotenbergServerError
from html_page_generator import AsyncPageGenerator

from src.clients.gotenberg import get_screenshot
from src.clients.s3 import generate_s3_url, upload_to_s3
from src.reuseble_types import SITE_EXAMPLE
from src.settings import AppSettings

from .exceptions import ScreenshotGenerationException, ServiceUnavailableException
from .schemas import CreateSiteRequest

logger = logging.getLogger(__name__)


async def generate_html_content(
    site_id: int,
    user_prompt: str,
    s3_client: boto3.client,
    gotenberg_client: httpx.AsyncClient,
    settings: AppSettings,
) -> AsyncGenerator[str]:
    """Сгенерировать HTML контент по промпту пользователя."""
    try:
        generator = AsyncPageGenerator(debug_mode=settings.debug_mode)

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
                key=f"{site_id}/{settings.s3.key}",
                content_type="text/html",
                content_disposition="attachment",
                s3_client=s3_client,
                s3_settings=settings.s3,
            )

            screenshot = await get_screenshot(html_content, gotenberg_client, settings.gotenberg)
            await upload_to_s3(
                body=screenshot,
                key=f"/{site_id}/index.png",
                content_type="image/png",
                content_disposition="attachment",
                s3_client=s3_client,
                s3_settings=settings.s3,
            )
    except (httpx.ReadTimeout, httpx.ConnectTimeout, httpx.TimeoutException, httpx.HTTPStatusError) as err:
        logger.error(f"Ошибка при генерации HTML для сайта {site_id}: {err}", exc_info=True)
        raise ServiceUnavailableException(
            message="Сервис временно недоступен. Попробуйте позже.",
            site_id=site_id,
        )
    except GotenbergServerError as err:
        logger.error(f"Ошибка при генерации скриншота для сайта {site_id}: {err}", exc_info=True)
        raise ScreenshotGenerationException(
            message="Не удалось сгенерировать скриншот",
            site_id=site_id,
        )


def mock_create_site(request: CreateSiteRequest):
    """Создать мок сайта."""
    return {
        **SITE_EXAMPLE,
        "prompt": request.prompt,
        "title": request.title,
    }


def mock_get_site(
    site_id: int,
    settings: AppSettings,
):
    """Получить мок сайта."""

    return {
        **SITE_EXAMPLE,
        "html_code_download_url": generate_s3_url(site_id, settings.s3, disposition="attachment"),
        "html_code_url": generate_s3_url(site_id, settings.s3),
        "id": site_id,
        "screenshot_url": generate_s3_url(site_id, settings.s3, file_name="index.png", disposition="inline"),
    }


def mock_get_user_sites(settings: AppSettings):
    """Получить мок сайтов пользователя."""
    site_id = 1
    return {
        "sites":
        [
            {
                **SITE_EXAMPLE,
                "html_code_download_url": generate_s3_url(site_id, settings.s3, disposition="attachment"),
                "html_code_url": generate_s3_url(site_id, settings.s3, disposition="inline"),
                "screenshot_url": generate_s3_url(site_id, settings.s3, file_name="index.png"),
            },
        ],
    }
