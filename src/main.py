import asyncio
from datetime import datetime
from pathlib import Path
from typing import Annotated

import aiofiles
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import AnyHttpUrl, BaseModel, ConfigDict, EmailStr, PastDatetime, StringConstraints

from reuseble_types import Site

FRONTEND_DIR = Path(__file__).parent / "frontend"

app = FastAPI()

response_config_dict = ConfigDict(
    extra="forbid",
    use_attribute_docstrings=True,
)
request_config_dict = ConfigDict(
    use_attribute_docstrings=True,
)


class UserDetailsResponse(BaseModel):
    profile_id: int
    """Уникальный идентификатор профиля пользователя"""
    email: EmailStr
    """Электронный адрес пользователя для связи и уведомлений"""
    username: Annotated[str, StringConstraints(max_length=254)]
    """Имя пользователя для входа в систему и идентификации"""
    registered_at: Annotated[datetime, PastDatetime]
    """Дата регистрации пользователя в системе"""
    updated_at: Annotated[datetime, PastDatetime]
    """Дата последнего обновления профиля пользователя"""
    is_active: bool
    """Флаг, указывающий, активен ли профиль пользователя"""

    model_config = response_config_dict | ConfigDict(
        json_schema_extra={
            "example": {
                "profile_id": 123,
                "email": "IIvanov@mail.ru",
                "username": "Иван",
                "registered_at": "2024-01-01T00:00:00",
                "updated_at": "2025-01-08T00:00:00",
                "is_active": False,
            },
        },
    )


def mock_get_user():
    """/frontend-api/users/me"""
    return {
        "profile_id": 1,
        "email": "IIvanov@mail.ru",
        "username": "Иван",
        "registered_at": "2025-01-01T12:00:00",
        "updated_at": "2025-01-01T00:00:00",
        "is_active": True,
    }


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


def mock_get_user_sits():
    """/frontend-api/users/my"""
    return {
        "sites":
        [
            {
            "created_at": "2025-01-01T00:00:00",
            "html_code_download_url": "http://example.com/media/index.html?response-content-disposition=attachment",
            "html_code_url": "http://example.com/media/index.html",
            "id": 1,
            "prompt": "Сайт садоводов любителей",
            "screenshot_url": "http://example.com/media/index.png",
            "title": "Садоводы любители",
            "updated_at": "2025-01-01T00:00:00",
            },
        ],
    }


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


def mock_get_site(site_id: int):
    """/frontend-api/{site_id}"""
    return {
        "created_at": "2025-06-15T18:29:56",
        "html_code_download_url": "http://example.com/media/index.html?response-content-disposition=attachment",
        "html_code_url": "http://example.com/media/index.html",
        "id": site_id,
        "prompt": "Сайт любителей",
        "screenshot_url": "http://example.com/media/index.png",
        "title": "Фан клуб",
        "updated_at": "2025-06-15T18:29:56",
    }


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


from router import *
