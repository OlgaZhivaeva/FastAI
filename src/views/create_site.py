from datetime import datetime
from typing import Annotated

from pydantic import AnyHttpUrl, BaseModel, ConfigDict, StringConstraints

from reuseble_types import request_config_dict, response_config_dict


class CreateSiteResponse(BaseModel):
    id: int
    """Уникальный идентификатор сайта"""
    title: Annotated[
        str,
        StringConstraints(max_length=128),
    ]
    """Название сайта"""
    prompt: str
    """Промпт"""
    created_at: datetime
    """Дата создания сайта"""
    updated_at: datetime
    """Дата последнего обновления сайта"""
    html_code_download_url: AnyHttpUrl | None = None
    """URL для скачивания HTML-кода сайта """
    html_code_url: AnyHttpUrl | None = None
    """URL для просмотра HTML-кода сайта"""
    screenshot_url: AnyHttpUrl | None = None
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


class CreateSiteRequest(BaseModel):
    prompt: str
    """Промпт"""
    title: Annotated[
        str,
        StringConstraints(max_length=254),
    ] | None = "Название сайта"
    """Название сайта"""

    model_config = request_config_dict | ConfigDict(
        json_schema_extra={
            "example": {
                "prompt": "Сайт любителей космических путешествий",
                "title": "Космический сайт",
            },
        },
    )


def mock_create_site(site: CreateSiteRequest):
    """/frontend-api/create"""
    return {
        "created_at": "2025-01-01T12:00:00",
        "html_code_download_url": "http://example.com/media/index.html?response-content-disposition=attachment",
        "html_code_url": "http://example.com/media/index.html",
        "id": 1,
        "prompt": site.prompt,
        "screenshot_url": "http://example.com/media/index.png",
        "title": site.title,
        "updated_at": "2025-01-01T12:00:00",
    }
