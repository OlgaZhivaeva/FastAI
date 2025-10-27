import logging

import anyio
import httpx
from fastapi import Request
from gotenberg_api import GotenbergServerError
from pydantic import BaseModel, ConfigDict
from starlette.responses import StreamingResponse

from src.reuseble_types import request_config_dict
from src.sites.service import generate_html_content

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


async def generate_html_stream(
    site_id: int,
    request: SiteGenerationRequest,
    http_request: Request,
) -> StreamingResponse:
    """post /frontend-api/sites/{site_id}/generate"""
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
