from datetime import datetime
from typing import Annotated

from pydantic import AnyHttpUrl, BaseModel, ConfigDict, PastDatetime, StringConstraints

from src.reuseble_types import request_config_dict, response_config_dict


class CreateSiteResponse(BaseModel):
    id: int
    """Уникальный идентификатор сайта"""
    title: Annotated[
        str,
        StringConstraints(max_length=12800),
    ]
    """Название сайта"""
    prompt: str
    """Промпт"""
    created_at: Annotated[datetime, PastDatetime]
    """Дата создания сайта"""
    updated_at: Annotated[datetime, PastDatetime]
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
                "createdAt": "2025-06-15T18:29:56+00:00",
                "htmlCodeDownloadUrl": "http://example.com/media/index.html?response-content-disposition=attachment",
                "htmlCodeUrl": "http://example.com/media/index.html",
                "id": 1,
                "prompt": "Сайт любителей играть в домино",
                "screenshotUrl": "http://example.com/media/index.png",
                "title": "Фан клуб Домино",
                "updatedAt": "2025-06-15T18:29:56+00:00",
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


def mock_create_site(request: CreateSiteRequest):
    """post /frontend-api/sites/create"""
    return {
        "created_at": "2025-01-01T12:00:00",
        "html_code_download_url": "http://example.com/media/index.html?response-content-disposition=attachment",
        "html_code_url": "http://example.com/media/index.html",
        "id": 1,
        "prompt": request.prompt,
        "screenshot_url": "http://example.com/media/index.png",
        "title": request.title,
        "updated_at": "2025-01-01T12:00:00",
    }
