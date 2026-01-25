import httpx
from gotenberg_api import ScreenshotHTMLRequest

from src.settings import Gotenberg


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
