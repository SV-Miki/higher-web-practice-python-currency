"""Pipeline для сохранения валют в базу данных."""

from decimal import Decimal

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from core.config import settings
from core.db import Base
from domain.currency.models import Currency, ExchangeRate


def get_sync_database_url() -> str:
    """Возвращает синхронный URL базы данных для Scrapy pipeline."""
    return settings.database_url.replace('+aiosqlite', '').replace(
        '+asyncpg', '+psycopg2'
    )


class CurrencyPipeline:
    """Pipeline для сохранения валют и курсов в БД."""

    def open_spider(self):
        """Открывает соединение с БД перед запуском паука."""
        engine = create_engine(get_sync_database_url())
        Base.metadata.create_all(engine)
        self.session_factory = sessionmaker(bind=engine)

    def process_item(self, item):
        """Сохраняет валюту и курс в БД."""
        with self.session_factory() as session:
            currency = self._get_or_create_currency(session, item)
            self._create_exchange_rate(session, currency, item)
            session.commit()

        return item

    def _get_or_create_currency(self, session, item) -> Currency:
        """Возвращает существующую валюту или создаёт новую."""
        result = session.execute(
            select(Currency).where(Currency.code == item['code'])
        )
        currency = result.scalars().first()

        if currency is None:
            currency = Currency(
                code=item['code'],
                name=item['name'],
                nominal=item['nominal'],
            )
            session.add(currency)
            session.flush()
        else:
            currency.name = item['name']
            currency.nominal = item['nominal']

        return currency

    def _create_exchange_rate(
        self,
        session,
        currency: Currency,
        item,
    ) -> None:
        """Создаёт курс валюты, если его ещё нет за эту дату."""
        result = session.execute(
            select(ExchangeRate).where(
                ExchangeRate.currency_id == currency.id,
                ExchangeRate.rate_date == item['rate_date'],
            )
        )
        exchange_rate = result.scalars().first()

        if exchange_rate is None:
            exchange_rate = ExchangeRate(
                currency_id=currency.id,
                rate_to_rub=Decimal(item['rate_to_rub']),
                rate_date=item['rate_date'],
            )
            session.add(exchange_rate)
        else:
            exchange_rate.rate_to_rub = Decimal(item['rate_to_rub'])
