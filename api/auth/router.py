"""API-ручки авторизации."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.constants import INVALID_CREDENTIALS_ERROR
from core.db import get_async_session
from core.exceptions import CredentialsError
from domain.auth.dto import LoginDTO, RefreshTokenDTO, Token
from domain.auth.service import AuthService

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post(
    '/login',
    response_model=Token,
)
async def login(
    login_data: LoginDTO,
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> Token:
    """Авторизует пользователя и возвращает токены."""
    service = AuthService(session)

    try:
        return await service.login(
            email=login_data.email,
            password=login_data.password,
        )
    except CredentialsError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=INVALID_CREDENTIALS_ERROR,
        ) from error


@router.post(
    '/refresh',
    response_model=Token,
)
async def refresh_tokens(
    token_data: RefreshTokenDTO,
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> Token:
    """Обновляет access и refresh токены."""
    service = AuthService(session)

    try:
        return await service.refresh_tokens(token_data.refresh_token)
    except CredentialsError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=INVALID_CREDENTIALS_ERROR,
        ) from error
