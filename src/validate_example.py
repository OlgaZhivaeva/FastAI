from main import CreateSiteRequest, SiteGenerationRequest, SiteResponse, UserDetailsResponse


def validate_schema_exampl(model):
    """Проверка корректности примера для Pydantic модели"""
    example = model.model_config.get("json_schema_extra", {}).get("example")
    if example:
        try:
            model(**example)
        except ValueError as e:
            raise ValueError(f"Ошибки валидации: {e}")


def main():
    pydantic_models = [UserDetailsResponse, SiteResponse, CreateSiteRequest, SiteGenerationRequest]
    for model in pydantic_models:
        try:
            validate_schema_exampl(model=model)
            print(f"Пример в {model.__name__} соответствует схеме.")
        except ValueError as e:
            print(e)


if __name__ == "__main__":
    main()
