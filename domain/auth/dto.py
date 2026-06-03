"""Pydantic-схемы авторизации."""

from datetime import datetime

from pydantic import BaseModel, EmailStr


class LoginDTO(BaseModel):
    """Схема запроса на логин."""

    email: EmailStr
    password: str


class RefreshTokenDTO(BaseModel):
    """Схема запроса на обновление токенов."""

    refresh_token: str


class Token(BaseModel):
    """Схема токенов авторизации."""

    access_token: str
    refresh_token: str
    token_type: str = 'bearer'


class TokenPayload(BaseModel):
    """Схема полезной нагрузки токена."""

    user_id: int
    email: EmailStr
    token_type: str
    exp: datetime
