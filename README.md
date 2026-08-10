# Currency Service

## Описание проекта

Currency Service - API-сервис для получения курсов валют Центрального банка РФ.

Проект реализован на FastAPI. Данные о валютах загружаются Scrapy-парсером с сайта ЦБ РФ и сохраняются в базу данных. API поддерживает регистрацию пользователей, авторизацию через JWT-токены и защищённые эндпоинты для просмотра курсов валют.

Проект позволяет:

- регистрировать пользователей
- авторизовывать пользователей через JWT
- обновлять access и refresh токены
- получать пользователя по ID
- получать пользователя по email
- обновлять данные текущего пользователя
- получать список всех доступных валют
- получать последний курс валюты по её коду
- получать всю историю курсов валюты
- получать историю курсов валюты за выбранный период
- загружать актуальные курсы валют с сайта ЦБ РФ
- сохранять данные в SQLite при локальном запуске
- сохранять данные в PostgreSQL при Docker-запуске
- запускать API, базу данных и парсер через Docker Compose
- автоматически запускать парсер один раз в сутки в Docker

## Технологии

В проекте используются:

- Python 3.12
- FastAPI
- Pydantic
- SQLAlchemy
- SQLite
- PostgreSQL
- Scrapy
- JWT
- Docker
- Docker Compose
- Uvicorn
- Ruff

## Структура проекта

```text
higher-web-practice-python-currency/
├── api/
│   ├── auth/
│   │   └── router.py
│   ├── currency/
│   │   └── router.py
│   └── users/
│       └── router.py
├── core/
│   ├── config.py
│   ├── constants.py
│   ├── db.py
│   ├── exceptions.py
│   └── security.py
├── domain/
│   ├── auth/
│   │   ├── dependencies.py
│   │   ├── dto.py
│   │   └── service.py
│   ├── currency/
│   │   ├── dto.py
│   │   ├── models.py
│   │   └── service.py
│   └── users/
│       ├── dto.py
│       ├── models.py
│       └── service.py
├── parser/
│   └── parser/
│       ├── spiders/
│       │   └── cbr.py
│       ├── items.py
│       ├── pipelines.py
│       └── settings.py
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── main.py
├── pyproject.toml
├── README.md
├── requirements.txt
├── scrapy.cfg
└── uv.lock
```

Основные части проекта:

- `api/` — FastAPI-роутеры
- `core/` — настройки, подключение к базе данных, безопасность, исключения и константы
- `domain/` — доменные модели, DTO-схемы и сервисный слой
- `parser/` — Scrapy-парсер и pipeline для сохранения данных
- `main.py` — точка входа FastAPI-приложения
- `Dockerfile` — инструкция сборки Docker-образа
- `docker-compose.yml` — запуск API, PostgreSQL и парсера
- `requirements.txt` — зависимости проекта
- `scrapy.cfg` — настройки запуска Scrapy из корня проекта

## Архитектура

Код разделён на несколько слоёв:

### Слой приложения

Слой приложения находится в директории `api/`.

Он отвечает за:

- регистрацию эндпоинтов
- получение данных из запроса
- вызов сервисов
- преобразование доменных ошибок в HTTP-ответы

Роутеры не работают с базой данных напрямую.

### Сервисный слой

Сервисный слой находится в директории `domain/`.

Он отвечает за бизнес-логику:

- создание пользователей
- поиск пользователей
- проверку авторизации
- создание JWT-токенов
- получение валют и курсов
- обработку случаев, когда данные не найдены

### Слой базы данных

ORM-модели находятся в:

```text
domain/users/models.py
domain/currency/models.py
```

В проекте используются модели:

- `User` — пользователь
- `Currency` — валюта
- `ExchangeRate` — курс валюты к рублю на конкретную дату

### Парсер

Scrapy-парсер находится в директории `parser/`.

Паук `CbrSpider` получает данные с сайта ЦБ РФ:

```text
http://www.cbr.ru/scripts/XML_daily.asp
```

Pipeline сохраняет данные в базу:

- создаёт валюту, если её ещё нет
- обновляет название и номинал валюты
- создаёт или обновляет курс валюты на конкретную дату

## Запуск проекта через Docker

Docker-запуск является основным способом запуска проекта.

### 1. Настроить переменные окружения

Скопируйте пример файла переменных окружения:

```bash
cp .env.example .env
```

При необходимости измените значения в созданном файле `.env`, особенно:

```env
POSTGRES_PASSWORD
SECRET_KEY
```

Если файл `.env` не создан, Docker Compose использует значения по умолчанию из `docker-compose.yml`.

### 2. Собрать и запустить контейнеры

```bash
docker compose up --build
```

После запуска будут созданы три сервиса:

```text
api
db
parser
```

- `api` — FastAPI-приложение
- `db` — PostgreSQL
- `parser` — Scrapy-парсер

Парсер запускается сразу после старта контейнеров, загружает курсы валют и затем повторяет запуск один раз в сутки.

### 3. Swagger-документация

При Docker-запуске Swagger доступен по адресу:

```text
http://127.0.0.1:8001/docs
```

Внутри контейнера приложение работает на порту `8000`, но наружу проброшено на порт `8001`, чтобы не конфликтовать с локальным запуском.

### 4. Проверить статус контейнеров

```bash
docker compose ps
```

Ожидаемые контейнеры:

```text
currency_api
currency_db
currency_parser
```

### 5. Проверить данные в PostgreSQL

Проверить количество валют:

```bash
docker compose exec db psql -U currency_user -d currency -c "SELECT COUNT(*) FROM currencies;"
```

Проверить количество курсов:

```bash
docker compose exec db psql -U currency_user -d currency -c "SELECT COUNT(*) FROM exchange_rates;"
```

Проверить курс USD:

```bash
docker compose exec db psql -U currency_user -d currency -c "SELECT c.code, c.name, r.rate_to_rub, r.rate_date FROM exchange_rates r JOIN currencies c ON c.id = r.currency_id WHERE c.code = 'USD';"
```

### 6. Остановить контейнеры

```bash
docker compose down
```

Остановить контейнеры и удалить данные PostgreSQL:

```bash
docker compose down -v
```

## Локальный запуск без Docker

### 1. Создать виртуальное окружение

```bash
python3 -m venv venv
```

### 2. Активировать виртуальное окружение

#### Linux/macOS

```bash
source venv/bin/activate
```

#### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Установить зависимости

```bash
python -m pip install --upgrade pip
```

```bash
python -m pip install -r requirements.txt
```

### 4. Запустить API

```bash
python -m uvicorn main:app --reload
```

При локальном запуске Swagger доступен по адресу:

```text
http://127.0.0.1:8000/docs
```

По умолчанию локально используется SQLite-база:

```text
currency.db
```

## Локальный запуск парсера

Из корня проекта выполните:

```bash
python -m scrapy crawl cbr
```

После запуска парсер загрузит курсы валют с сайта ЦБ РФ и сохранит их в локальную базу `currency.db`.

Проверить данные в SQLite можно командой:

```bash
python - <<'PY'
import sqlite3

connection = sqlite3.connect('currency.db')
cursor = connection.cursor()

print('currencies:', cursor.execute('SELECT COUNT(*) FROM currencies').fetchone()[0])
print('exchange_rates:', cursor.execute('SELECT COUNT(*) FROM exchange_rates').fetchone()[0])

print(cursor.execute(
    '''
    SELECT currencies.code, currencies.name, exchange_rates.rate_to_rub, exchange_rates.rate_date
    FROM exchange_rates
    JOIN currencies ON currencies.id = exchange_rates.currency_id
    ORDER BY currencies.code
    LIMIT 5
    '''
).fetchall())

connection.close()
PY
```

## Документация API

Swagger-документация доступна по адресам:

```text
http://127.0.0.1:8000/docs
```

для локального запуска и:

```text
http://127.0.0.1:8001/docs
```

для Docker-запуска.

OpenAPI-схема доступна по адресам:

```text
http://127.0.0.1:8000/openapi.json
```

и:

```text
http://127.0.0.1:8001/openapi.json
```

## Основные эндпоинты

### Пользователи

| Метод | Эндпоинт               | Описание                              |
|-------|------------------------|---------------------------------------|
| POST  | `/users/register`      | Зарегистрировать пользователя         |
| GET   | `/users/{user_id}`     | Получить пользователя по ID           |
| GET   | `/users/email/{email}` | Получить пользователя по email        |
| PUT   | `/users`               | Обновить данные текущего пользователя |

Эндпоинты получения и обновления пользователей доступны только авторизованным пользователям.

### Авторизация

| Метод | Эндпоинт        | Описание                                      |
|-------|-----------------|-----------------------------------------------|
| POST  | `/auth/login`   | Получить access и refresh токены              |
| POST  | `/auth/refresh` | Обновить access и refresh токены              |

### Валюты

| Метод | Эндпоинт                                                        | Описание                           |
|-------|-----------------------------------------------------------------|------------------------------------|
| GET   | `/currencies`                                                   | Получить список всех валют         |
| GET   | `/currencies/{currency_code}`                                   | Получить последний курс валюты     |
| GET   | `/currencies/{currency_code}/history?start_date=...&end_date=...` | Получить историю курсов за период  |
| GET   | `/currencies/{currency_code}/all`                               | Получить всю историю курсов валюты |

Все эндпоинты валют доступны только авторизованным пользователям.

## Авторизация в Swagger

1. Зарегистрируйте пользователя через `POST /users/register`.
2. Выполните логин через `POST /auth/login`.
3. Скопируйте `access_token`.
4. Нажмите кнопку `Authorize`.
5. Вставьте токен в формате:

```text
Bearer <access_token>
```

После этого можно выполнять защищённые эндпоинты.

## Быстрая проверка API

1. Запустите проект через Docker:

```bash
docker compose up --build
```

2. Откройте Swagger:
```text
http://127.0.0.1:8001/docs
```

3. Зарегистрируйте пользователя через POST `/users/register`.
4. Выполните логин через POST `/auth/login`.
5. Скопируйте `access_token`.
6. Нажмите кнопку `Authorize` и вставьте токен:

```text
Bearer <access_token>
```

7. Проверьте основные защищённые ручки:

```text
GET /currencies
GET /currencies/USD
GET /currencies/USD/all
GET /currencies/USD/history?start_date=2026-06-01&end_date=2026-06-10
```

8. Проверьте ошибку для несуществующей валюты:

```text
GET /currencies/XXX
```

Ожидаемый ответ:

```json
{
  "detail": "Currency not found"
}
```

9. Проверьте ошибку некорректного диапазона дат:

```text
GET /currencies/USD/history?start_date=2026-06-10&end_date=2026-06-01
```

Ожидаемый статус ответа - `422 Unprocessable Entity`.

## Примеры запросов

Значения курсов в примерах могут отличаться в зависимости от даты запуска парсера и данных, полученных с сайта ЦБ РФ.

### Регистрация пользователя

```http request
POST /users/register
```

```json
{
  "email": "test@example.com",
  "password": "12345"
}
```

Пример ответа:

```json
{
  "id": 1,
  "email": "test@example.com"
}
```

### Логин пользователя

```http request
POST /auth/login
```

```json
{
  "email": "test@example.com",
  "password": "12345"
}
```

Пример ответа:

```json
{
  "access_token": "<access_token>",
  "refresh_token": "<refresh_token>",
  "token_type": "bearer"
}
```

### Обновление токенов

```http request
POST /auth/refresh
```

```json
{
  "refresh_token": "<refresh_token>"
}
```

Пример ответа:

```json
{
  "access_token": "<new_access_token>",
  "refresh_token": "<new_refresh_token>",
  "token_type": "bearer"
}
```

### Получить список валют

```http request
GET /currencies
```

Пример ответа:

```json
[
  {
    "id": 15,
    "code": "AED",
    "name": "Дирхам ОАЭ",
    "nominal": 1
  },
  {
    "id": 16,
    "code": "USD",
    "name": "Доллар США",
    "nominal": 1
  }
]
```

### Получить последний курс USD

```http request
GET /currencies/USD
```

Пример ответа:

```json
{
  "id": 16,
  "currency": {
    "id": 16,
    "code": "USD",
    "name": "Доллар США",
    "nominal": 1
  },
  "rate_to_rub": "72.5597",
  "rate_date": "2026-06-03"
}
```

### Получить историю USD за период

```http request
GET /currencies/USD/history?start_date=2026-06-01&end_date=2026-06-10
```

Пример ответа:

```json
[
  {
    "id": 16,
    "currency": {
      "id": 16,
      "code": "USD",
      "name": "Доллар США",
      "nominal": 1
    },
    "rate_to_rub": "72.5597",
    "rate_date": "2026-06-03"
  }
]
```

### Получить всю историю USD

```http request
GET /currencies/USD/all
```

Пример ответа:

```json
[
  {
    "id": 16,
    "currency": {
      "id": 16,
      "code": "USD",
      "name": "Доллар США",
      "nominal": 1
    },
    "rate_to_rub": "72.5597",
    "rate_date": "2026-06-03"
  }
]
```

## Права доступа

### Анонимный пользователь

Может:

- зарегистрироваться
- выполнить логин
- обновить токены при наличии refresh token

Не может:

- получать данные пользователей
- обновлять пользователя
- получать список валют
- получать курсы валют

### Авторизованный пользователь

Может:

- получать пользователя по ID
- получать пользователя по email
- обновлять свои данные
- получать список валют
- получать последний курс валюты
- получать историю курсов валюты
- обновлять access и refresh токены

## Примеры ошибок

Если пользователь уже существует:

```json
{
  "detail": "User already exists"
}
```

Если пользователь не найден:

```json
{
  "detail": "User not found"
}
```

Если данные авторизации неверные:

```json
{
  "detail": "Invalid credentials"
}
```

Если валюта не найдена:

```json
{
  "detail": "Currency not found"
}
```

Если начальная дата периода позже конечной:

```json
{
  "detail": "Start date must not be later than end date"
}
```

## Переменные окружения

Проект поддерживает настройку через переменные окружения.

| Переменная          | Описание                        | Значение по умолчанию для Docker |
|---------------------|---------------------------------|----------------------------------|
| `POSTGRES_DB`       | Название базы данных PostgreSQL | `currency`                       |
| `POSTGRES_USER`     | Пользователь PostgreSQL         | `currency_user`                  |
| `POSTGRES_PASSWORD` | Пароль пользователя PostgreSQL  | `currency_password`              |
| `DATABASE_URL`      | URL подключения к базе данных   | `postgresql+asyncpg://currency_user:currency_password@db:5432/currency` |
| `SECRET_KEY`        | Секретный ключ для JWT          | `CHANGE_ME_DOCKER_SECRET_KEY`    |

Пример значений находится в файле `.env.example`.

При локальном запуске без Docker, если `DATABASE_URL` не задан, используется SQLite:

```text
sqlite+aiosqlite:///./currency.db
```

## Проверка проекта

### Проверка синтаксиса

```bash
python -m compileall core domain api parser main.py
```

### Проверка Ruff

```bash
python -m ruff check .
```

### Проверка форматирования Ruff

```bash
python -m ruff format --check .
```

### Автоисправление и форматирование

```bash
python -m ruff check . --fix
python -m ruff format .
```

### Проверка Docker Compose

```bash
docker compose config
```

## Автор

Владислав Шилов
