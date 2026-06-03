"""Сервис валют."""

from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.exceptions import CurrencyNotFoundError
from domain.currency.models import Currency, ExchangeRate


class CurrencyService:
    """Сервис для работы с валютами."""

    def __init__(self, session: AsyncSession):
        """Инициализирует сервис сессией БД."""
        self.session = session

    async def list_currencies(self) -> list[Currency]:
        """Возвращает список всех валют."""
        result = await self.session.execute(
            select(Currency).order_by(Currency.code)
        )
        return list(result.scalars().all())

    async def get_latest_rate(self, target_code: str) -> ExchangeRate:
        """Возвращает последний курс валюты."""
        currency = await self._get_currency_by_code(target_code)

        result = await self.session.execute(
            select(ExchangeRate)
            .options(selectinload(ExchangeRate.currency))
            .where(ExchangeRate.currency_id == currency.id)
            .order_by(ExchangeRate.rate_date.desc())
            .limit(1)
        )
        rate = result.scalars().first()

        if rate is None:
            raise CurrencyNotFoundError

        return rate

    async def get_rate_history(
        self,
        target_code: str,
        start_date: date,
        end_date: date,
    ) -> list[ExchangeRate]:
        """Возвращает историю курсов валюты за период."""
        currency = await self._get_currency_by_code(target_code)

        result = await self.session.execute(
            select(ExchangeRate)
            .options(selectinload(ExchangeRate.currency))
            .where(
                ExchangeRate.currency_id == currency.id,
                ExchangeRate.rate_date >= start_date,
                ExchangeRate.rate_date <= end_date,
            )
            .order_by(ExchangeRate.rate_date)
        )
        return list(result.scalars().all())

    async def get_rates_for_currency(
        self,
        target_code: str,
    ) -> list[ExchangeRate]:
        """Возвращает всю историю курсов валюты."""
        currency = await self._get_currency_by_code(target_code)

        result = await self.session.execute(
            select(ExchangeRate)
            .options(selectinload(ExchangeRate.currency))
            .where(ExchangeRate.currency_id == currency.id)
            .order_by(ExchangeRate.rate_date)
        )
        return list(result.scalars().all())

    async def _get_currency_by_code(self, target_code: str) -> Currency:
        """Возвращает валюту по коду."""
        result = await self.session.execute(
            select(Currency).where(Currency.code == target_code.upper())
        )
        currency = result.scalars().first()

        if currency is None:
            raise CurrencyNotFoundError

        return currency
