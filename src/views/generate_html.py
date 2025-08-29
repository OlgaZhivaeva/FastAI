import aioboto3
import anyio
import httpx
from aiobotocore.config import AioConfig
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


async def upload_html_page(html_content, http_request: Request):
    config = AioConfig(
        max_pool_connections=http_request.app.state.settings.minio.max_pool_connections,
        connect_timeout=http_request.app.state.settings.minio.connect_timeout,
        read_timeout=http_request.app.state.settings.minio.read_timeout,
    )
    async with aioboto3.Session().client(
            's3',
            config=config,
            region_name='us-east-1',
            endpoint_url=http_request.app.state.settings.minio.endpoint_url,
            aws_access_key_id=http_request.app.state.settings.minio.aws_access_key_id,
            aws_secret_access_key=http_request.app.state.settings.minio.aws_secret_access_key,
    ) as client:
        upload_params = {
            'Bucket': http_request.app.state.settings.minio.bucket,
            'Key': http_request.app.state.settings.minio.key,
            'Body': html_content,
            'ContentType': 'text/html',
            'ContentDisposition': 'attachment',
        }
        await client.put_object(**upload_params)


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
                    title_saved = False
                    async for chunk in generator(user_prompt):
                        yield chunk
                        print(chunk, end="", flush=True)
                        if title_saved:
                            continue
                        if title := generator.html_page.title:
                            print(title)
                            title_saved = True

                html_content = generator.html_page.html_code
                await upload_html_page(html_content, http_request)

        except (httpx.ReadTimeout, httpx.ConnectTimeout, httpx.TimeoutException, httpx.HTTPStatusError) as err:
            print(f"Oшибка при генерации HTML: {err}")

    return StreamingResponse(html_generator(request.prompt), media_type="text/html")
