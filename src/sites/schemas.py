from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints

from src.reuseble_types import Site, get_site_example_json, request_config_dict, response_config_dict


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


class SiteGenerationRequest(BaseModel):
    prompt: str
    """Промпт"""

    model_config = request_config_dict | ConfigDict(
        json_schema_extra={
            "example": {
                "prompt": "Сайт любителей играть в домино",
            },
        },
    )


class SiteResponse(Site):
    model_config = response_config_dict | ConfigDict(
        json_schema_extra={
            "example": get_site_example_json(),
        },
    )


class GeneratedSitesResponse(BaseModel):
    sites: list[Site]
    """Список сайтов пользователя"""

    model_config = response_config_dict | ConfigDict(
        json_schema_extra={
            "example": {
                "sites": [get_site_example_json()],
            },
        },
    )
