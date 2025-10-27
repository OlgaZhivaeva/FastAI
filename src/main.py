import logging
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from pathlib import Path

import aioboto3
from aiobotocore.config import AioConfig
from fastapi import FastAPI
from html_page_generator import AsyncDeepseekClient, AsyncUnsplashClient
from starlette.staticfiles import StaticFiles

from src.settings import AppSettings
from src.sites.router import sites_router
from src.users.router import users_router

FRONTEND_DIR = Path(__file__).parent / "frontend"

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

settings = AppSettings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AbstractAsyncContextManager[None]:
    app.state.settings = settings

    async with (
        aioboto3.Session().client(
            's3',
            config=AioConfig(
                max_pool_connections=settings.s3.max_pool_connections,
                connect_timeout=settings.s3.connect_timeout,
                read_timeout=settings.s3.read_timeout,
            ),
            region_name='us-east-1',
            endpoint_url=settings.s3.endpoint_url,
            aws_access_key_id=settings.s3.aws_access_key_id,
            aws_secret_access_key=settings.s3.aws_secret_access_key,
        ) as s3_client,
        AsyncUnsplashClient.setup(
            settings.unsplash.client_id,
            timeout=settings.unsplash.timeout,
        ),
        AsyncDeepseekClient.setup(
            settings.deep_seek.api_key,
            settings.deep_seek.base_url,
        ),
    ):
        app.state.s3_client = s3_client
        yield


app = FastAPI(lifespan=lifespan)

app.include_router(users_router)
app.include_router(sites_router)

app.mount(
    "/",
    StaticFiles(directory=FRONTEND_DIR, html=True),
    name="frontend",
)
