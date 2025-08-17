from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, PastDatetime, StringConstraints

response_config_dict = ConfigDict(
    extra="forbid",
    use_attribute_docstrings=True,
)
request_config_dict = ConfigDict(
    use_attribute_docstrings=True,
)


class Site(BaseModel):
    id: int
    """Уникальный идентификатор сайта"""
    title: Annotated[
        str,
        StringConstraints(max_length=254),
    ]
    """Название сайта"""
    prompt: str
    """Промпт"""
    created_at: Annotated[datetime, PastDatetime]
    """Дата создания сайта"""
    updated_at: Annotated[datetime, PastDatetime]
    """Дата последнего обновления сайта"""
    html_code_download_url: str | None = None  # TODO заменить на AnyHttpUrl
    """URL для скачивания HTML-кода сайта """
    html_code_url: str | None = None  # TODO заменить на AnyHttpUrl
    """URL для просмотра HTML-кода сайта"""
    screenshot_url: str | None = None  # TODO заменить на AnyHttpUrl
    """URL превью сайта"""
