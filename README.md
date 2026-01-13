# FastAI

FastAI — это веб-сервис для создания HTML-страниц с помощью нейросетей. Он умеет создавать яркие сайты-визитки,
лендинги и продающие страницы в полностью автоматическом режиме.

## Настройки переменных окружения

Для запуска проекта необходимо настроить переменные окружения.

Скопируйте файл `example.env` в `.env`
```commandline
cp example.env .env
```
Отредактируйте файл `.env`.
```.env
DEBUG_MODE="Значение True для разработки и отладки или False для production"
TIMEOUT="Таймаут в секундах для API запросов"
DEEP_SEEK__API_KEY="Ваш API ключ DeepSeek"
DEEP_SEEK__MAX_CONNECTIONS="Максимальное количество подключений к DeepSeek API"
DEEPSEEK__BASE_URL="Если вы используете альтернативную инсталляцию DeepSeek"
UNSPLASH__CLIENT_ID="Ваш Client ID Unsplash APIo"
UNSPLASH__MAX_CONNECTIONS="Максимальное количество подключений к Unsplash API"
UNSPLASH__TIMEOUT="Значение по умолчанию 3"
S3__ENDPOINT_URL="URL-адрес MinIO S3 хранилища"
S3__AWS_ACCESS_KEY_ID="Идентификатор ключа доступа AWS для аутентификации в MinIO"
S3__AWS_SECRET_ACCESS_KEY="Секретный ключ доступа AWS для аутентификации в MinIO"
S3__BUCKET="Имя бакета в MinIO"
S3__KEY="Ключ (имя файла) в бакете"
S3__MAX_POOL_CONNECTIONS="Значение по умолчанию 50"
S3__CONNECT_TIMEOUT="Значение по умолчанию 10"
S3__READ_TIMEOUT="Значение по умолчанию 30"
GOTENBERG__BASE_URL="Базовый адрес Gotenberg API"
GOTENBERG__TIMEOUT="Значение по умолчанию 15"
GOTENBERG__WIDTH="Значение по умолчанию 1000"
GOTENBERG__FORMAT="Значение по умолчанию png"
GOTENBERG__WAIT_DELAY="Значение по умолчанию 5"
```
Заполните значения переменных окружения, необходимые для работы приложения.

DEBUG_MODE: Включает или выключает режим отладки. Установите в True для разработки и отладки, False для production (рабочего режима).

TIMEOUT: Таймаут в секундах для API запросов. Это значение определяет, как долго приложение будет ждать ответа от API,<br>
прежде чем произойдет таймаут. Увеличьте это значение, если вы часто сталкиваетесь с ошибками таймаута.

### Настройки Deep Seek

DEEP_SEEK__API_KEY: Ваш API ключ для доступа к DeepSeek API. Вы можете получить этот ключ, создав аккаунт и зарегистрировав<br>
ваше приложение на Портале разработчиков [DeepSeek API](https://api-docs.deepseek.com/quick_start/pricing). Этот ключ необходим для аутентификации в сервисе DeepSeek.<br>
Если нет возможности оплатить официальный DeepSeek (с большинства карт РФ), рекомендуем воспользоваться одной из альтернативных инсталляций:<br>
- [BotHub](https://bothub.chat/deepseek-chat-v3-0324/api)
- [VseGPT](https://vsegpt.ru/Docs/Models#h46-6)
    - [Регистрация и настройка](https://gist.github.com/Eugene-Fed/9f86603a1279cfdc690ecc70b392f5cf)

DEEP_SEEK__MAX_CONNECTIONS: Максимальное количество одновременных подключений к DeepSeek API.

DEEPSEEK__BASE_URL: Если вы используете альтернативную инсталляцию DeepSeek, укажите данные для вашей инсталляции.

### Настройки Unsplash

UNSPLASH__CLIENT_ID: Ваш Client ID для доступа к Unsplash API. Зарегистрируйте ваше приложение на Портале разработчиков
[Unsplash API](https://unsplash.com/documentation#creating-a-developer-account),<br> чтобы получить этот ID.

UNSPLASH__MAX_CONNECTIONS: Максимальное количество одновременных подключений к Unsplash API.

UNSPLASH__TIMEOUT: Максимальное время в секундах, которое приложение будет ждать ответа от Unsplash API. По умолчанию 30

### Настройки для MinIO S3 хранилища

S3__ENDPOINT_URL: URL-адрес MinIO S3 хранилища. Например, "http://127.0.0.1:9000".

S3__AWS_ACCESS_KEY_ID: Идентификатор ключа доступа AWS для аутентификации в MinIO. Например, "minioadmin".

S3__AWS_SECRET_ACCESS_KEY: Секретный ключ доступа AWS для аутентификации в MinIO. Например, "minioadmin".

S3__BUCKET: Имя бакета в MinIO, который будет использоваться. Например, "html-bucket".

S3__KEY: Ключ (имя файла) в бакете, который будет использоваться. Например, "index.html".

S3__MAX_POOL_CONNECTIONS: Максимальное количество подключений в пуле соединений. Определяет максимальное количество параллельных запросов к MinIO. По умолчанию 50.

S3__CONNECT_TIMEOUT: Таймаут подключения в секундах. Определяет, как долго клиент будет ждать установления соединения с MinIO. По умолчанию 10.

S3__READ_TIMEOUT: Таймаут чтения в секундах. Определяет, как долго клиент будет ждать получения данных от MinIO. По умолчанию 30.

Пример S3 настроек:

```
S3__ENDPOINT_URL="http://127.0.0.1:9000"
S3__AWS_ACCESS_KEY_ID="minioadmin"
S3__AWS_SECRET_ACCESS_KEY="minioadmin"
S3__BUCKET="html-bucket"
S3__KEY="index.html"
S3__MAX_POOL_CONNECTIONS=50
S3__CONNECT_TIMEOUT=10
S3__READ_TIMEOUT=30
```

### Настройки для Gotenberg API

GOTENBERG__BASE_URL: Базовый адрес Gotenberg API, обычно "http://localhost:3000"

GOTENBERG__TIMEOUT: Таймаут асинхронного клиента ддля библиотеки httpx. Значение по умолчанию 15.

GOTENBERG__WIDTH: Ширина скриншота в пикселях. Значение по умолчанию 1000.

GOTENBERG__FORMAT: Формат скриншота (может принимать значения jpeg, png, webp). Значение по умолчанию png.

GOTENBERG__WAIT_DELAY: Время ожидания завершения анимаций на html-странице. Значение по умолчанию 5.

Важно: время ожидания завершения анимаций должно быть меньше таймаута асинхронного клиента, иначе библиотека всегда будет возвращать TimeoutError.
Рекомендуемая разница между временем ожидания и таймаутом составляет от 2 до 5 секунд.


Пример настроек для Gotenberg API:

```
GOTENBERG__BASE_URL="http://localhost:3000"
GOTENBERG__TIMEOUT=15
GOTENBERG__WIDTH=1000
GOTENBERG__FORMAT="png"
GOTENBERG__WAIT_DELAY=5
```


### Обновите файл .gitignore

Чтобы предотвратить попадание файла `.env` в ваш репозиторий, добавьте следующую строку в файл .gitignore:
```.gitignore
.env
```

## Как установить и запустить MinIO

Скачать MinIO можно на [официальном сайте MinIO](https://www.min.io/download?platform=windows)

### Инструкция для Windows

Откройте PowerShell от имени администратора. Создайте папку для MinIO:
```powershell
New-Item -ItemType Directory -Path "C:\minio"
```

Загрузите MinIO:
```powershell
Invoke-WebRequest -Uri "https://dl.min.io/server/minio/release/windows-amd64/minio.exe" -OutFile "C:\minio\minio.exe"
```
Создайте папку для данных:
```powershell
New-Item -ItemType Directory -Path "C:\minio\data"
```

Скачайте утилиту mc (MinIO Client):
```powershell
Invoke-WebRequest -Uri "https://dl.min.io/client/mc/release/windows-amd64/mc.exe" -OutFile "C:\mc.exe"
```

Запустите MinIO:
```powershell
& "C:\minio\minio.exe" server C:\minio\data
```
Зайдите на сайт MinIO по адресу http://127.0.0.1:9000. <br>Используйте для входа учетные данные:
-   RootUser: minioadmin
-   RootPass: minioadmin

На сайте создайте свой бакет, например `html-bucket`

Установите алиас для mc (MinIO Client), например `myminio`
```powershell
mc alias set 'myminio' 'http://127.0.0.1:9000' 'myadmin' 'myadmin'
```

Сделайте бакет публичным используя команду
```powershell
mc anonymous set public myminio/html-bucket
```
Вручную загрузите в бакет файлы `index.html` и `index.png`.
Это позволяет использовать ссылки на файлы в бакете при реализации эндпоинтов


## Как запустить Gotenberg

Чтобы запустить стандартный Docker-контейнер Gotenberg, выполните команду:
```commandline
docker run --rm -p "127.0.0.1:3000:3000" gotenberg/gotenberg:8
```


## Как развернуть фронтенд локально

В папке `src` создайте папку `frontend`.
Скачайте и распакуйте в нее [архив с фронтендом](https://dvmn.org/filer/canonical/1750917110/1035/)

В папке `frontend` создайте файл `frontend-settings.json` и добавьте в него настройки
```
{
    "backendBaseUrl": "/frontend-api"
}
```


## Репозиторий для бэкенд-разработчиков.

Инструкции и справочная информация по разворачиванию проекта собраны
в документе [CONTRIBUTING.md](./CONTRIBUTING.md).
