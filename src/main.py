from pathlib import Path

from fastapi import APIRouter, FastAPI
from starlette.staticfiles import StaticFiles

FRONTEND_DIR = Path(__file__).parent / "frontend"

app = FastAPI()
api_router = APIRouter(prefix="/frontend-api")

from router import *

app.include_router(api_router)
app.mount(
    "/",
    StaticFiles(directory=FRONTEND_DIR, html=True),
    name="frontend",
)
