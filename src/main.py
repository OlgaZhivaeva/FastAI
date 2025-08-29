from contextlib import asynccontextmanager
from pathlib import Path

import aioboto3
from aiobotocore.config import AioConfig
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from router import api_router
from settings import AppSettings

FRONTEND_DIR = Path(__file__).parent / "frontend"

settings = AppSettings()

print("Настройки приложения:", settings.model_dump_json(indent=4))


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.settings = settings

    app.include_router(api_router)

    app.mount(
        "/",
        StaticFiles(directory=FRONTEND_DIR, html=True),
        name="frontend",
    )

    async with aioboto3.Session().client(
            's3',
            config=AioConfig(
                max_pool_connections=settings.minio.max_pool_connections,
                connect_timeout=settings.minio.connect_timeout,
                read_timeout=settings.minio.read_timeout,
            ),
            region_name='us-east-1',
            endpoint_url=settings.minio.endpoint_url,
            aws_access_key_id=settings.minio.aws_access_key_id,
            aws_secret_access_key=settings.minio.aws_secret_access_key,
    ) as s3_client:
        app.state.s3_client = s3_client
        yield


app = FastAPI(lifespan=lifespan)
