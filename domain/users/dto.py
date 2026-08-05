"""Pydantic-схемы пользователей."""

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from core.constants import USER_EMAIL_MAX_LENGTH


class CreateUserDTO(BaseModel):
    """Схема создания пользователя."""

    email: EmailStr = Field(max_length=USER_EMAIL_MAX_LENGTH)
    password: str


class UpdateUserDTO(BaseModel):
    """Схема обновления пользователя."""

    email: EmailStr | None = Field(
        default=None,
        max_length=USER_EMAIL_MAX_LENGTH,
    )
    password: str | None = None


class UserDTO(BaseModel):
    """Схема пользователя без пароля."""

    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)
