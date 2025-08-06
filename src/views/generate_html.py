import asyncio

import aiofiles
from pydantic import BaseModel, ConfigDict
from starlette.responses import StreamingResponse

from reuseble_types import request_config_dict


class SiteGenerationRequest(BaseModel):
    prompt: str
    """Промпт"""

    model_config = request_config_dict | ConfigDict(
        json_schema_extra={
            "example": {
                "prompt": "Сайт любителей морских свинок",
            },
        },
    )


async def mock_generate_html(site_id: int, request: SiteGenerationRequest):
    """/frontend-api/{site_id}/generate"""
    async def html_generator():
        async with aiofiles.open("src/index.html", "rb") as f:
            while True:
                chunk = await f.read(1024)
                if not chunk:
                    break
                yield chunk
                await asyncio.sleep(1)

    return StreamingResponse(html_generator(), media_type="text/html")
