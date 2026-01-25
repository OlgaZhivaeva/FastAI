class SiteException(Exception):
    """Базовое исключение"""
    def __init__(self, message: str, site_id: int):
        self.message = message
        self.site_id = site_id
        super().__init__(self.message)


class ServiceUnavailableException(SiteException):
    """Внешний сервис не отвечает"""
    pass


class ScreenshotGenerationException(SiteException):
    """Не удалось создать скриншот"""
    pass
