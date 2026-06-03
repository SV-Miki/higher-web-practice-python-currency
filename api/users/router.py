"""API-ручки пользователей."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.constants import USER_ALREADY_EXISTS_ERROR, USER_NOT_FOUND_ERROR
from core.db import get_async_session
from core.exceptions import UserAlreadyExistsError, UserNotFoundError
from domain.auth.dependencies import get_current_user
from domain.users.dto import CreateUserDTO, UpdateUserDTO, UserDTO
from domain.users.models import User
from domain.users.service import UserService

router = APIRouter(prefix='/users', tags=['users'])


@router.post(
    '/register',
    response_model=UserDTO,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    user_data: CreateUserDTO,
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> UserDTO:
    """Регистрирует нового пользователя."""
    service = UserService(session)

    try:
        user = await service.create_user(user_data)
    except UserAlreadyExistsError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=USER_ALREADY_EXISTS_ERROR,
        ) from error

    return UserDTO.model_validate(user)


@router.get(
    '/email/{email}',
    response_model=UserDTO,
)
async def get_user_by_email(
    email: str,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> UserDTO:
    """Возвращает пользователя по email."""
    service = UserService(session)

    try:
        user = await service.get_user_by_email(email)
    except UserNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=USER_NOT_FOUND_ERROR,
        ) from error

    return UserDTO.model_validate(user)


@router.get(
    '/{user_id}',
    response_model=UserDTO,
)
async def get_user_by_id(
    user_id: int,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> UserDTO:
    """Возвращает пользователя по ID."""
    service = UserService(session)

    try:
        user = await service.get_user_by_id(user_id)
    except UserNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=USER_NOT_FOUND_ERROR,
        ) from error

    return UserDTO.model_validate(user)


@router.put(
    '',
    response_model=UserDTO,
)
async def update_user(
    user_data: UpdateUserDTO,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> UserDTO:
    """Обновляет текущего пользователя."""
    service = UserService(session)

    try:
        user = await service.update_user(current_user, user_data)
    except UserAlreadyExistsError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=USER_ALREADY_EXISTS_ERROR,
        ) from error

    return UserDTO.model_validate(user)
