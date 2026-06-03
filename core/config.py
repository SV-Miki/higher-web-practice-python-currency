"""Настройки приложения."""

from pydantic_settings import BaseSettings, SettingsConfigDict

from core.constants import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    APP_DESCRIPTION,
    APP_TITLE,
    DATABASE_URL,
    JWT_ALGORITHM,
    REFRESH_TOKEN_EXPIRE_DAYS,
    SECRET_KEY,
)


class Settings(BaseSettings):
    """Основные настройки приложения."""

    app_title: str = APP_TITLE
    app_description: str = APP_DESCRIPTION
    database_url: str = DATABASE_URL

    secret_key: str = SECRET_KEY
    jwt_algorithm: str = JWT_ALGORITHM
    access_token_expire_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES
    refresh_token_expire_days: int = REFRESH_TOKEN_EXPIRE_DAYS

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
