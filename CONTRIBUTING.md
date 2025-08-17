# Разработчикам бэкенда


## Как развернуть local-окружение

### Необходимое ПО

Для запуска ПО вам понадобятся консольный Git и Make. Инструкции по их установке ищите на
официальных сайтах:

- [Git SCM](https://git-scm.com/)
- [GNU Make](https://www.gnu.org/software/make/)

Вы можете проверить, установлены ли эти программы с помощью команд:
```shell
$ git --help
usage: git [-v | --version] [-h | --help] [-C <path>] [-c <name>=<value>]
           [--exec-path[=<path>]] [--html-path] [--man-path] [--info-path]
           [-p | --paginate | -P | --no-pager] [--no-replace-objects] [--bare]
           [--git-dir=<path>] [--work-tree=<path>] [--namespace=<name>]
           [--config-env=<name>=<envvar>] <command> [<args>]
<...>

$ make --help
Usage: make [options] [target] ...
Options:
<...>
```

Для тех, кто использует Windows необходимы также программы **git** и **git bash**. В git bash надо добавить ещё команду
make:

- Go to [ezwinports](https://sourceforge.net/projects/ezwinports/files/)
- Download make-4.4.1-without-guile-w32-bin.zip (get the version without guile)
- Extract zip
- Copy the contents to C:\ProgramFiles\Git\mingw64\ merging the folders, but do NOT overwrite/replace any exisiting
  files.

Все дальнейшие команды запускать из-под **git bash**.

### Настройка pre-commit хуков

В репозитории используются хуки pre-commit, чтобы автоматически запускать линтеры и автотесты. Перед началом разработки
установите [pre-commit package manager](https://pre-commit.com/).

В корне репозитория запустите команду для настройки хуков:

```shell
$ pre-commit install
pre-commit installed at .git/hooks/pre-commit
```

В последующем при коммите автоматически будут запускаться линтеры и автотесты. Есть линтеры будет недовольны, то коммит прервётся с ошибкой.

### Создание виртуального окружения для работы с IDE

IDE для корректной работы подсказок необходимо развернуть виртуальное окружение со всеми установленными зависимостями.

В качестве пакетного менеджера на проекта используется [uv](https://docs.astral.sh/uv/).

Установите [uv](https://docs.astral.sh/uv/) и в корне репозитория выполните команду

```shell
$ uv sync
```

[uv](https://docs.astral.sh/uv/) создаст виртуальное окружение, установит необходимую версию Python и все необходимые зависимости.

После этого активируйте виртуальное окружение в текущей сессии терминала:

```shell
$ source .venv/bin/activate  # для Linux
$ .\.venv\Scripts\activate  # Для Windows
```

### Настройки переменных окружения

Для запуска проекта необходимо настроить переменные окружения.

Скопируйте файл `example.env` в `.env`
```commandline
cp example.env .env
```
Отредактируйте файл `.env`.
```.env
DEBUG_MODE="Значение True для разработки и отладки или False для production"
DEEP_SEEK_API_KEY="Ваш API ключ DeepSeek"
DEEP_SEEK_MAX_CONNECTIONS="Максимальное количество подключений к DeepSeek API"
UNSPLASH_CLIENT_ID="Ваш Client ID Unsplash APIo"
UNSPLASH_MAX_CONNECTIONS="Максимальное количество подключений к Unsplash API"
TIMEOUT="Таймаут в секундах для API запросов"
DEEPSEEK_BASE_URL="Если вы используете альтернативную инсталляцию DeepSeek"
```
Заполните значения переменных окружения, необходимые для работы приложения.

DEBUG_MODE: Включает или выключает режим отладки. Установите в True для разработки и отладки, False для production (рабочего режима).

DEEP_SEEK_API_KEY: Ваш API ключ для доступа к DeepSeek API. Вы можете получить этот ключ, создав аккаунт и зарегистрировав<br>
ваше приложение на Портале разработчиков [DeepSeek API](https://api-docs.deepseek.com/quick_start/pricing). Этот ключ необходим для аутентификации в сервисе DeepSeek.<br>
Если нет возможности оплатить официальный DeepSeek (с большинства карт РФ), рекомендуем воспользоваться одной из альтернативных инсталляций:<br>
- [BotHub](https://bothub.chat/deepseek-chat-v3-0324/api)
- [VseGPT](https://vsegpt.ru/Docs/Models#h46-6)
    - [Регистрация и настройка](https://gist.github.com/Eugene-Fed/9f86603a1279cfdc690ecc70b392f5cf)

DEEP_SEEK_MAX_CONNECTIONS: Максимальное количество одновременных подключений к DeepSeek API.

UNSPLASH_CLIENT_ID: Ваш Client ID для доступа к Unsplash API. Зарегистрируйте ваше приложение на Портале разработчиков
[Unsplash API](https://unsplash.com/documentation#creating-a-developer-account),<br> чтобы получить этот ID.

UNSPLASH_MAX_CONNECTIONS: Максимальное количество одновременных подключений к Unsplash API.

TIMEOUT: Таймаут в секундах для API запросов. Это значение определяет, как долго приложение будет ждать ответа от API,<br>
прежде чем произойдет таймаут. Увеличьте это значение, если вы часто сталкиваетесь с ошибками таймаута.

DEEPSEEK_BASE_URL: Если вы используете альтернативную инсталляцию DeepSeek, укажите данные для вашей инсталляции.


Чтобы предотвратить попадание файла .env в ваш репозиторий, добавьте следующую строку в файл .gitignore:
```.gitignore
.env
```


## Как вести разработку

Код проекта находится в папке `/src`.

Находясь в корневой директории проекта, запустить проект можно командой:

```shell
$ fastapi dev src/main.py
```

Проект будет работать по адресу http://127.0.0.1:8000/

### Как установить python-пакет в виртуальное окружение

В качестве менеджера пакетов используется [uv](https://docs.astral.sh/uv/).

Вот пример как добавить в зависимости библиотеку `beautifulsoup4`.

```shell
$ uv add beautifulsoup4
```

Конфигурационные файлы `pyproject.toml` и `uv.lock` обновятся автоматически.

Аналогичным образом можно удалять python-пакеты:

```shell
$ uv remove beautifulsoup4
```

Если необходимо обновить `uv.lock` вручную, то используйте команду:

```shell
$ uv lock
```

### Команды для быстрого запуска с помощью make

Для часто используемых команд подготовлен набор альтернативных коротких команд `make`.

```shell
$ make help
Cписок доступных команд:
lint                      Проверяет линтерами код в репозитории
format                    Автоматически исправляет форматирование кода -- порядок импортов, лишние пробелы и т.д.
help                      Отображает список доступных команд и их описания
```

## Схемы приложения FastAI

[Схема локальной инсталляции бэкенда](https://gitlab.dvmn.org/root/fastapi-articles/-/wikis/fastai/backend_local_installation.drawio.png)

[Схема продовой инсталляции бэкенда](https://gitlab.dvmn.org/root/fastapi-articles/-/wikis/fastai/backend_prod_installation.drawio.png)

[Схема подсистем бэкенда](https://gitlab.dvmn.org/root/fastapi-articles/-/wikis/fastai/backend_decomposition.drawio.png)


## Как развернуть фронтенд локально

В папке `src` создайте папку `frontend`.
Скачайте и распакуйте в нее [архив с фронтендом](https://dvmn.org/filer/canonical/1750917110/1035/)

В папке `frontend` создайте файл `frontend-settings.json` и добавьте в него настройки
```
{
    "backendBaseUrl": "/frontend-api"
}
```
