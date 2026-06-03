"""Функции безопасности: пароли и JWT-токены."""

from datetime import UTC, datetime, timedelta
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from core.config import settings
from core.exceptions import TokenError

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Возвращает хеш пароля."""
    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет пароль."""
    return password_context.verify(plain_password, hashed_password)


def create_token(
    data: dict[str, Any],
    expires_delta: timedelta,
) -> str:
    """Создаёт JWT-токен."""
    payload = data.copy()
    expire = datetime.now(UTC) + expires_delta
    payload.update({"exp": expire})
    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.jwt_algorithm,
    )


def decode_token(token: str) -> dict[str, Any]:
    """Декодирует JWT-токен."""
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.jwt_algorithm],
        )
    except JWTError as error:
        raise TokenError from error

    return payload
