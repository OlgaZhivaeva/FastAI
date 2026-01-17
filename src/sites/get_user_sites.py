from fastapi import Request
from pydantic import BaseModel, ConfigDict

from src.reuseble_types import SITE_EXAMPLE, Site, get_site_example_json, response_config_dict
from src.sites.service import generate_s3_url


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


def mock_get_user_sites(http_request: Request):
    """get /frontend-api/sites/my"""
    s3_settings = http_request.app.state.settings.s3
    site_id = 1
    return {
        "sites":
        [
            {
                **SITE_EXAMPLE,
                "html_code_download_url": generate_s3_url(site_id, s3_settings, disposition="attachment"),
                "html_code_url": generate_s3_url(site_id, s3_settings, disposition="inline"),
                "screenshot_url": generate_s3_url(site_id, s3_settings, file_name="index.png"),
            },
        ],
    }
