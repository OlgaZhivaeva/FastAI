from fastapi import APIRouter
from starlette.responses import HTMLResponse

from src.sites.create_site import mock_create_site
from src.sites.generate_html import generate_html_stream
from src.sites.get_site import SiteResponse, mock_get_site
from src.sites.get_user_sites import GeneratedSitesResponse, mock_get_user_sites

sites_router = APIRouter(prefix="/frontend-api/sites", tags=["Sites"])

sites_router.get(
    "/my",
    summary="Получить список сайтов пользователя",
    response_description="Сайты пользователя",
    response_model=GeneratedSitesResponse,
)(mock_get_user_sites)


sites_router.get(
    "/{site_id}",
    summary="Получить сайт",
    response_description="Данные сайта",
    response_model=SiteResponse,
)(mock_get_site)


sites_router.post(
    "/create",
    summary="Создать сайт",
    response_description="Данные для генерации сайта",
    response_model=SiteResponse,
)(mock_create_site)


sites_router.post(
    "/{site_id}/generate",
    summary="Сгенерировать HTML код сайта",
    response_description="HTML код сайта",
    response_class=HTMLResponse,
)(generate_html_stream)
