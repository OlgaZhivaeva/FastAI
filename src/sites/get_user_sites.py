from urllib.parse import urlparse

from fastapi import Request
from furl import furl
from pydantic import BaseModel, ConfigDict

from src.reuseble_types import Site, response_config_dict


class GeneratedSitesResponse(BaseModel):
    sites: list[Site]
    """Список сайтов пользователя"""

    model_config = response_config_dict | ConfigDict(
        json_schema_extra={
            "example": {
                "sites": [
                    {
                        "createdAt": "2025-06-15T18:29:56",
                        "htmlCodeDownloadUrl": "http://example.com/media/index.html?response-content-disposition=attachment",
                        "htmlCodeUrl": "http://example.com/media/index.html",
                        "id": 1,
                        "prompt": "Сайт любителей играть в домино",
                        "screenshotUrl": "http://example.com/media/index.png",
                        "title": "Фан клуб Домино",
                        "updatedAt": "2025-06-15T18:29:56",
                    },
                ],
            },
        },
    )


def mock_get_user_sites(http_request: Request):
    """get /frontend-api/sites/my"""
    title = getattr(
        http_request.app.state,
        'title',
        "Заголовок не задан")
    prompt = getattr(
        http_request.app.state,
        'user_prompt',
        "Промпт не задан",
    )
    created_at = getattr(
        http_request.app.state,
        'created_at',
        "2025-01-01T00:00:00",
    )
    parsed_url = urlparse(http_request.app.state.settings.s3.endpoint_url)
    scheme = parsed_url.scheme
    host = parsed_url.hostname
    port = parsed_url.port

    url_builder = furl(
        scheme=scheme,
        host=host,
        port=port,
        path=f"{http_request.app.state.settings.s3.bucket}/{http_request.app.state.settings.s3.key}",
        query_params={"response-content-disposition": "attachment"},
    )
    html_code_download_url = str(url_builder)

    url_builder = furl(
        scheme=scheme,
        host=host,
        port=port,
        path=f"{http_request.app.state.settings.s3.bucket}/{http_request.app.state.settings.s3.key}",
        query_params={"response-content-disposition": "inline"},
    )
    html_code_url = str(url_builder)

    file_name = "index.png"
    url_builder = furl(
        scheme=scheme,
        host=host,
        port=port,
        path=f"{http_request.app.state.settings.s3.bucket}/{file_name}",
    )
    screenshot_url = str(url_builder)

    return {
        "sites":
        [
            {
                "created_at": created_at,
                "html_code_download_url": html_code_download_url,
                "html_code_url": html_code_url,
                "id": 1,
                "prompt": prompt,
                "screenshot_url": screenshot_url,
                "title": title,
                "updated_at": created_at,
            },
        ],
    }
