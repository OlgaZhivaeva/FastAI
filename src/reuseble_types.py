from datetime import datetime
from typing import Annotated

from pydantic import AnyHttpUrl, BaseModel, ConfigDict, PastDatetime, StringConstraints
from pydantic.alias_generators import to_camel

SITE_EXAMPLE = {
    "created_at": "2025-01-01T00:00:00",
    "html_code_download_url": "http://example.com/media/index.html?response-content-disposition=attachment",
    "html_code_url": "http://example.com/media/index.html",
    "id": 1,
    "prompt": "Промпт пользователя",
    "screenshot_url": "http://example.com/media/index.png",
    "title": "Название сайта",
    "updated_at": "2025-01-01T00:00:00",
}

response_config_dict = ConfigDict(
    extra="forbid",
    use_attribute_docstrings=True,
    alias_generator=to_camel,
    populate_by_name=True,
)
request_config_dict = ConfigDict(
    use_attribute_docstrings=True,
    alias_generator=to_camel,
    populate_by_name=True,
)


class Site(BaseModel):
    id: int
    """Уникальный идентификатор сайта"""
    title: Annotated[
        str,
        StringConstraints(max_length=25400),
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

    model_config = ConfigDict(
        use_attribute_docstrings=True,
        alias_generator=to_camel,
        populate_by_name=True,
    )


def get_site_example_json():
    return Site(**SITE_EXAMPLE).model_dump(by_alias=True, mode="json")
