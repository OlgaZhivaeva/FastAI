from datetime import datetime

import anyio
import httpx
from fastapi import Request
from html_page_generator import AsyncDeepseekClient, AsyncPageGenerator, AsyncUnsplashClient
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


async def get_presigned_url(content_type, content_disposition, http_request: Request):
    params = {
        'Bucket': http_request.app.state.settings.s3.bucket,
        'Key': http_request.app.state.settings.s3.key,
        'ResponseContentDisposition': content_disposition,
        'ResponseContentType': content_type,
    }

    url = await http_request.app.state.s3_client.generate_presigned_url(
        'get_object',
        Params=params,
        ExpiresIn=60 * 60,
    )
    return url


async def upload_html_page(html_content, http_request: Request):
    upload_params = {
        'Bucket': http_request.app.state.settings.s3.bucket,
        'Key': http_request.app.state.settings.s3.key,
        'Body': html_content,
        'ContentType': 'text/html',
        'ContentDisposition': 'attachment',
    }
    await http_request.app.state.s3_client.put_object(**upload_params)


async def mock_generate_html(
    site_id: int,
    request: SiteGenerationRequest,
    http_request: Request,
):
    """/frontend-api/{site_id}/generate"""
    async def html_generator(user_prompt: str):
        try:
            async with (
                AsyncUnsplashClient.setup(
                    http_request.app.state.settings.unsplash.client_id,
                    timeout=3,
                ),
                AsyncDeepseekClient.setup(
                    http_request.app.state.settings.deep_seek.api_key,
                    http_request.app.state.settings.deep_seek.base_url,
                ),
            ):
                with anyio.CancelScope(shield=True):
                    generator = AsyncPageGenerator(debug_mode=http_request.app.state.settings.debug_mode)
                    http_request.app.state.user_prompt = user_prompt
                    title_saved = False
                    async for chunk in generator(user_prompt):
                        yield chunk
                        print(chunk, end="", flush=True)
                        if title_saved:
                            continue
                        if title := generator.html_page.title:
                            print(title)
                            http_request.app.state.title = title
                            title_saved = True

                html_content = generator.html_page.html_code
                await upload_html_page(html_content, http_request)

                http_request.app.state.html_code_download_url = await get_presigned_url(
                    "text/html",
                    'attachment; filename="index.html"',
                    http_request,
                )
                http_request.app.state.html_code_url = await get_presigned_url(
                    "text/html",
                    'inline',
                    http_request,
                )
                http_request.app.state.screenshot_url = await get_presigned_url(
                    "image/png",
                    'inline',
                    http_request,
                )
                http_request.app.state.created_at = datetime.now()

        except (httpx.ReadTimeout, httpx.ConnectTimeout, httpx.TimeoutException, httpx.HTTPStatusError) as err:
            print(f"Ошибка при генерации HTML: {err}")

    return StreamingResponse(html_generator(request.prompt), media_type="text/html")
