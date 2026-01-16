from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints

from src.reuseble_types import Site, get_site_example_json, request_config_dict, response_config_dict


class CreateSiteResponse(Site):
    model_config = response_config_dict | ConfigDict(
        json_schema_extra={
            "example": get_site_example_json(),
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
