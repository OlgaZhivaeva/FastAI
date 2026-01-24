import boto3
import httpx
from fastapi import Request

from src.settings import AppSettings


def get_settings(request: Request) -> AppSettings:
    return request.app.state.settings


def get_s3_client(request: Request) -> boto3.client:
    return request.app.state.s3_client


def get_gotenberg_client(request: Request) -> httpx.AsyncClient:
    return request.app.state.gotenberg_client
