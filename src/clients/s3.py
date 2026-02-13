from furl import furl

from src.settings import S3


async def upload_to_s3(
    body: bytes | str,
    key: str,
    content_type: str,
    content_disposition: str,
    s3_client: any,
    s3_settings: S3,
) -> None:
    """Загрузить данные в MinIO S3 хранилище."""
    upload_params = {
        'Bucket': s3_settings.bucket,
        'Key': key,
        'Body': body,
        'ContentType': content_type,
        'ContentDisposition': content_disposition,
    }
    await s3_client.put_object(**upload_params)


def generate_s3_url(
    site_id: int,
    s3_settings: S3,
    file_name: str = None,
    disposition: str = None,
) -> str:
    """Сгенерировать URL-адрес для доступа к файлу в S3-хранилище"""
    url = furl(s3_settings.endpoint_url)
    key = f"{site_id}/{file_name}" if file_name else f"{site_id}/{s3_settings.key}"
    url.path = f"/{s3_settings.bucket}/{key}"

    if disposition:
        url.args['response-content-disposition'] = disposition

    return str(url)
