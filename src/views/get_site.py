from datetime import datetime
from typing import Annotated

from fastapi import Request
from pydantic import AnyHttpUrl, BaseModel, ConfigDict, PastDatetime, StringConstraints

from reuseble_types import response_config_dict


class SiteResponse(BaseModel):
    id: int
    """Уникальный идентификатор сайта"""
    title: Annotated[
        str,
        StringConstraints(max_length=128),
    ]
    """Название сайта"""
    prompt: str
    """Промпт"""
    created_at: Annotated[datetime, PastDatetime]
    """Дата создания сайта"""
    updated_at: Annotated[datetime, PastDatetime]
    """Дата последнего обновления сайта"""
    html_code_download_url: AnyHttpUrl | None = None  # TODO заменить на AnyHttpUrl
    """URL для скачивания HTML-кода сайта """
    html_code_url: AnyHttpUrl | None = None  # TODO заменить на AnyHttUrlp
    """URL для просмотра HTML-кода сайта"""
    screenshot_url: AnyHttpUrl | None = None  # TODO заменить на AnyHttpUrl
    """URL превью сайта"""

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


async def mock_get_site(site_id: int, http_request: Request):
    """/frontend-api/{site_id}"""
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
    created_at = getattr(
        http_request.app.state,
        "created_at",
        "2025-01-01T00:00:00",
    )

    return {
        "created_at": created_at,
        "html_code_download_url": html_code_download_url,
        "html_code_url": html_code_url,
        "id": site_id,
        "prompt": prompt,
        "screenshot_url": screenshot_url,
        "title": title,
        "updated_at": created_at,
    }
