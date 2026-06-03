"""Сервис авторизации."""

from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.constants import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from core.exceptions import CredentialsError, TokenError, UserNotFoundError
from core.security import create_token, decode_token, verify_password
from domain.auth.dto import Token
from domain.users.models import User
from domain.users.service import UserService


class AuthService:
    """Сервис для авторизации пользователей."""

    def __init__(self, session: AsyncSession):
        """Инициализирует сервис сессией БД."""
        self.session = session
        self.user_service = UserService(session)

    async def login(self, email: str, password: str) -> Token:
        """Аутентифицирует пользователя и создаёт токены."""
        try:
            user = await self.user_service.get_user_by_email(email)
        except UserNotFoundError as error:
            raise CredentialsError from error

        if not verify_password(password, user.password_hash):
            raise CredentialsError

        return self._create_tokens(user)

    async def refresh_tokens(self, refresh_token: str) -> Token:
        """Обновляет access и refresh токены."""
        try:
            payload = decode_token(refresh_token)
        except TokenError as error:
            raise CredentialsError from error

        if payload.get('token_type') != REFRESH_TOKEN_TYPE:
            raise CredentialsError

        user_id = payload.get('user_id')

        if user_id is None:
            raise CredentialsError

        try:
            user = await self.user_service.get_user_by_id(int(user_id))
        except UserNotFoundError as error:
            raise CredentialsError from error

        return self._create_tokens(user)

    def _create_tokens(self, user: User) -> Token:
        """Создаёт пару access и refresh токенов."""
        access_token = create_token(
            data={
                'user_id': user.id,
                'email': user.email,
                'token_type': ACCESS_TOKEN_TYPE,
            },
            expires_delta=timedelta(
                minutes=settings.access_token_expire_minutes,
            ),
        )
        refresh_token = create_token(
            data={
                'user_id': user.id,
                'email': user.email,
                'token_type': REFRESH_TOKEN_TYPE,
            },
            expires_delta=timedelta(
                days=settings.refresh_token_expire_days,
            ),
        )

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
        )
