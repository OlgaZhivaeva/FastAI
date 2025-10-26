from pydantic import ValidationError

from src.sites.create_site import CreateSiteRequest, CreateSiteResponse
from src.sites.generate_html import SiteGenerationRequest
from src.sites.get_site import SiteResponse
from src.sites.get_user_sites import GeneratedSitesResponse
from src.users.get_user import UserDetailsResponse


def validate_schema_example(model):
    """Проверить корректность примеров для Pydantic моделей"""
    example = model.model_config.get("json_schema_extra", {}).get("example")
    if example:
        try:
            model.model_validate(example)
        except ValidationError as e:
            raise ValueError(f"Ошибки валидации: {e}")


def main():
    pydantic_models = [
        UserDetailsResponse,
        GeneratedSitesResponse,
        SiteResponse, CreateSiteRequest,
        CreateSiteResponse,
        SiteGenerationRequest,
    ]
    for model in pydantic_models:
        try:
            validate_schema_example(model=model)
            print(f"Пример в {model.__name__} соответствует схеме.")
        except ValueError as e:
            print(e)


if __name__ == "__main__":
    main()
