from fastapi import Request
from pydantic import BaseModel, ConfigDict
from starlette.responses import StreamingResponse

from src.reuseble_types import request_config_dict
from src.sites.service import generate_html_content


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
    state = http_request.app.state

    return StreamingResponse(
        generate_html_content(
            user_prompt=request.prompt,
            s3_client=state.s3_client,
            s3_settings=state.settings.s3,
            gotenberg_client=state.gotenberg_client,
            gotenberg_settings=state.settings.gotenberg,
            debug_mode=state.settings.debug_mode,
        ),
        media_type='text/html',
    )
