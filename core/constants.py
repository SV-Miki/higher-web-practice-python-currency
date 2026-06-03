"""Константы приложения Currency Service."""

APP_TITLE = 'Сервис курса валют'
APP_DESCRIPTION = 'REST API для получения курсов валют Центрального банка РФ'

DATABASE_URL = 'sqlite+aiosqlite:///./currency.db'

# Настройки JWT-токенов.
SECRET_KEY = 'CHANGE_ME_SECRET_KEY'
JWT_ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7
ACCESS_TOKEN_TYPE = 'access'
REFRESH_TOKEN_TYPE = 'refresh'

# Ограничения полей пользователя.
USER_EMAIL_MAX_LENGTH = 255
USER_PASSWORD_HASH_MAX_LENGTH = 255

# Ограничения полей валюты.
CURRENCY_CODE_MAX_LENGTH = 3
CURRENCY_NAME_MAX_LENGTH = 255
DEFAULT_CURRENCY_NOMINAL = 1

# Настройки точности курса валюты.
EXCHANGE_RATE_PRECISION = 12
EXCHANGE_RATE_SCALE = 4

# Сообщения ошибок API.
USER_ALREADY_EXISTS_ERROR = 'User already exists'
USER_NOT_FOUND_ERROR = 'User not found'
INVALID_CREDENTIALS_ERROR = 'Invalid credentials'
INVALID_TOKEN_ERROR = 'Invalid token'
CURRENCY_NOT_FOUND_ERROR = 'Currency not found'

# Настройки источника данных ЦБ РФ.
CBR_URL_TEMPLATE = (
    'http://www.cbr.ru/scripts/XML_daily.asp?date_req={day}/{month}/{year}'
)
CBR_RESPONSE_DATE_FORMAT = '%d.%m.%Y'
CBR_REQUEST_DAY_FORMAT = '%d'
CBR_REQUEST_MONTH_FORMAT = '%m'
CBR_REQUEST_YEAR_FORMAT = '%Y'
