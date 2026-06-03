"""Сервис пользователей."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import UserAlreadyExistsError, UserNotFoundError
from core.security import hash_password
from domain.users.dto import CreateUserDTO, UpdateUserDTO
from domain.users.models import User


class UserService:
    """Сервис для работы с пользователями."""

    def __init__(self, session: AsyncSession):
        """Инициализирует сервис сессией БД."""
        self.session = session

    async def get_user_by_email(self, email: str) -> User:
        """Получает пользователя по адресу электронной почты."""
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        user = result.scalars().first()

        if user is None:
            raise UserNotFoundError

        return user

    async def get_user_by_id(self, user_id: int) -> User:
        """Получает пользователя по ID."""
        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalars().first()

        if user is None:
            raise UserNotFoundError

        return user

    async def create_user(self, user: CreateUserDTO) -> User:
        """Создаёт нового пользователя."""
        result = await self.session.execute(
            select(User).where(User.email == user.email)
        )
        existing_user = result.scalars().first()

        if existing_user is not None:
            raise UserAlreadyExistsError

        db_user = User(
            email=user.email,
            password_hash=hash_password(user.password),
        )
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)

        return db_user

    async def update_user(
        self,
        current_user: User,
        user_data: UpdateUserDTO,
    ) -> User:
        """Обновляет данные текущего пользователя."""
        if (
            user_data.email is not None
            and user_data.email != current_user.email
        ):
            result = await self.session.execute(
                select(User).where(User.email == user_data.email)
            )
            existing_user = result.scalars().first()

            if existing_user is not None:
                raise UserAlreadyExistsError

            current_user.email = user_data.email

        if user_data.password is not None:
            current_user.password_hash = hash_password(user_data.password)

        self.session.add(current_user)
        await self.session.commit()
        await self.session.refresh(current_user)

        return current_user
