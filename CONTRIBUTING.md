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

В качестве пакетного менеджера на проекте используется [uv](https://docs.astral.sh/uv/).

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
lint                           Проверяет линтерами код в репозитории
format                         Запуск автоформатера
help                           Отображает список доступных команд и их описания
```

## Схемы приложения FastAI

[Схема локальной инсталляции бэкенда](https://gitlab.dvmn.org/root/fastapi-articles/-/wikis/fastai/backend_local_installation.drawio.png)

[Схема продовой инсталляции бэкенда](https://gitlab.dvmn.org/root/fastapi-articles/-/wikis/fastai/backend_prod_installation.drawio.png)

[Схема подсистем бэкенда](https://gitlab.dvmn.org/root/fastapi-articles/-/wikis/fastai/backend_decomposition.drawio.png)
