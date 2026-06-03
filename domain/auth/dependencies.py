"""Зависимости авторизации."""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from core.constants import ACCESS_TOKEN_TYPE, INVALID_CREDENTIALS_ERROR
from core.db import get_async_session
from core.exceptions import TokenError, UserNotFoundError
from core.security import decode_token
from domain.users.models import User
from domain.users.service import UserService

bearer_scheme = HTTPBearer()


async def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials,
        Depends(bearer_scheme),
    ],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> User:
    """Возвращает пользователя из access-токена."""
    try:
        payload = decode_token(credentials.credentials)

        if payload.get('token_type') != ACCESS_TOKEN_TYPE:
            raise TokenError

        user_id = payload.get('user_id')

        if user_id is None:
            raise TokenError

        return await UserService(session).get_user_by_id(int(user_id))
    except (TokenError, UserNotFoundError) as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=INVALID_CREDENTIALS_ERROR,
        ) from error
