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

    return StreamingResponse(
        generate_html_content(
            site_id=site_id,
            user_prompt=request.prompt,
            app_state=http_request.app.state,
        ),
        media_type='text/html',
    )
