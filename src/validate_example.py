from pydantic import ValidationError

from views.create_site import CreateSiteRequest, CreateSiteResponse
from views.generate_html import SiteGenerationRequest
from views.get_site import SiteResponse
from views.get_user import UserDetailsResponse


def validate_schema_example(model):
    """Проверка корректности примера для Pydantic модели"""
    example = model.model_config.get("json_schema_extra", {}).get("example")
    if example:
        try:
            model.model_validate(example)
        except ValidationError as e:
            raise ValueError(f"Ошибки валидации: {e}")


def main():
    pydantic_models = [UserDetailsResponse, SiteResponse, CreateSiteRequest, CreateSiteResponse, SiteGenerationRequest]
    for model in pydantic_models:
        try:
            validate_schema_example(model=model)
            print(f"Пример в {model.__name__} соответствует схеме.")
        except ValueError as e:
            print(e)


if __name__ == "__main__":
    main()
