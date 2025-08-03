from datetime import datetime

from pydantic import AnyHttpUrl, BaseModel


class Site(BaseModel):
    id: int
    """Уникальный идентификатор сайта"""
    title: str
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
