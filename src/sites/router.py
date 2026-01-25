from typing import Annotated

import boto3
import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from starlette.responses import HTMLResponse, StreamingResponse

from src.dependencies import get_gotenberg_client, get_s3_client, get_settings
from src.settings import AppSettings

from .exceptions import ScreenshotGenerationException, ServiceUnavailableException
from .schemas import CreateSiteRequest, GeneratedSitesResponse, SiteGenerationRequest, SiteResponse
from .service import generate_html_stream, mock_create_site, mock_get_site, mock_get_user_sites

sites_router = APIRouter(prefix="/frontend-api/sites", tags=["Sites"])


@sites_router.get(
    "/my",
    summary="Получить список сайтов пользователя",
    response_description="Сайты пользователя",
    response_model=GeneratedSitesResponse,
)
async def get_user_sites(settings: Annotated[AppSettings, Depends(get_settings)]):
    return mock_get_user_sites(settings)


@sites_router.get(
    "/{site_id}",
    summary="Получить сайт",
    response_description="Данные сайта",
    response_model=SiteResponse,
)
async def get_site(
    site_id: int,
    settings: Annotated[AppSettings, Depends(get_settings)],
):
    return mock_get_site(site_id, settings)


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
async def generate_html(
    site_id: int,
    request: SiteGenerationRequest,
    s3_client: Annotated[boto3.client, Depends(get_s3_client)],
    gotenberg_client: Annotated[httpx.AsyncClient, Depends(get_gotenberg_client)],
    settings: Annotated[AppSettings, Depends(get_settings)],
) -> StreamingResponse:
    try:
        return await generate_html_stream(
            site_id,
            request,
            s3_client,
            gotenberg_client,
            settings,
        )
    except ServiceUnavailableException as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        )
    except ScreenshotGenerationException as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )
