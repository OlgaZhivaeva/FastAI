from fastapi import Request
from pydantic import BaseModel, ConfigDict

from reuseble_types import Site, response_config_dict


class GeneratedSitesResponse(BaseModel):
    sites: list[Site]
    """Список сайтов пользователя"""

    model_config = response_config_dict | ConfigDict(
        json_schema_extra={
            "example": {
                "created_at": "2025-06-15T18:29:56",
                "html_code_download_url": "http://example.com/media/index.html?response-content-disposition=attachment",
                "html_code_url": "http://example.com/media/index.html",
                "id": 1,
                "prompt": "Сайт любителей играть в домино",
                "screenshot_url": "http://example.com/media/index.png",
                "title": "Фан клуб Домино",
                "updated_at": "2025-06-15T18:29:56",
            },
        },
    )


async def mock_get_user_sites(http_request: Request):
    """/frontend-api/users/my"""
    html_code_download_url = getattr(
        http_request.app.state,
        'html_code_download_url',
        "http://example.com/media/index.html?response-content-disposition=attachment",
    )
    html_code_url = getattr(
        http_request.app.state,
        'html_code_url',
        "http://example.com/media/index.html",
    )
    screenshot_url = getattr(
        http_request.app.state,
        'screenshot_url',
        "http://example.com/media/index.png",
    )
    title = getattr(
        http_request.app.state,
        'title',
        "Заголовок не задан")
    prompt = getattr(
        http_request.app.state,
        'user_prompt',
        "Промпт не задан",
    )

    return {
        "sites":
        [
            {
            "created_at": "2025-01-01T00:00:00",
            "html_code_download_url": html_code_download_url,
            "html_code_url": html_code_url,
            "id": 1,
            "prompt": prompt,
            "screenshot_url": screenshot_url,
            "title": title,
            "updated_at": "2025-01-01T00:00:00",
            },
        ],
    }
