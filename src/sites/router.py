from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse

from src.sites.create_site import CreateSiteRequest, mock_create_site
from src.sites.generate_html import SiteGenerationRequest, generate_html_stream
from src.sites.get_site import SiteResponse, mock_get_site
from src.sites.get_user_sites import GeneratedSitesResponse, mock_get_user_sites

sites_router = APIRouter(prefix="/frontend-api/sites", tags=["Sites"])


@sites_router.get(
    "/my",
    summary="Получить список сайтов пользователя",
    response_description="Сайты пользователя",
    response_model=GeneratedSitesResponse,
)
async def get_user_sites(http_request: Request):
    return mock_get_user_sites(http_request)


@sites_router.get(
    "/{site_id}",
    summary="Получить сайт",
    response_description="Данные сайта",
    response_model=SiteResponse,
)
async def get_site(site_id: int, http_request: Request):
    return mock_get_site(site_id, http_request)


@sites_router.post(
    "/create",
    summary="Создать сайт",
    response_description="Данные для генерации сайта",
    response_model=SiteResponse,
)
async def create_site(request: CreateSiteRequest):
    return mock_create_site(request)


@sites_router.post(
    "/{site_id}/generate",
    summary="Сгенерировать HTML код сайта",
    response_description="HTML код сайта",
    response_class=HTMLResponse,
)
async def generate_html(site_id: int, request: SiteGenerationRequest, http_request: Request):
    return await generate_html_stream(site_id, request, http_request)
