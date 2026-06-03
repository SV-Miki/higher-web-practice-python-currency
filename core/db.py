"""Настройка подключения к базе данных."""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from core.config import settings


class Base(DeclarativeBase):
    """Базовый класс для ORM-моделей."""


engine = create_async_engine(settings.database_url)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Генерирует асинхронную сессию БД."""
    async with AsyncSessionLocal() as session:
        yield session


async def create_db() -> None:
    """Создаёт таблицы базы данных."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
