"""ORM-модели валют и курсов валют."""

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    Date,
    DateTime,
    ForeignKey,
    Numeric,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.constants import (
    CURRENCY_CODE_MAX_LENGTH,
    CURRENCY_NAME_MAX_LENGTH,
    DEFAULT_CURRENCY_NOMINAL,
    EXCHANGE_RATE_PRECISION,
    EXCHANGE_RATE_SCALE,
)
from core.db import Base


class Currency(Base):
    """Модель валюты."""

    __tablename__ = "currencies"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(
        String(CURRENCY_CODE_MAX_LENGTH),
        unique=True,
        index=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        String(CURRENCY_NAME_MAX_LENGTH),
        nullable=False,
    )
    nominal: Mapped[int] = mapped_column(
        nullable=False,
        default=DEFAULT_CURRENCY_NOMINAL,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )

    rates: Mapped[list["ExchangeRate"]] = relationship(
        back_populates="currency",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        """Возвращает строковое представление валюты."""
        return (
            f"Currency("
            f"id={self.id!r}, "
            f"code={self.code!r}, "
            f"name={self.name!r}"
            ")"
        )


class ExchangeRate(Base):
    """Модель курса валюты к рублю на конкретную дату."""

    __tablename__ = "exchange_rates"

    __table_args__ = (
        UniqueConstraint(
            "currency_id",
            "rate_date",
            name="uq_exchange_rate_currency_date",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    currency_id: Mapped[int] = mapped_column(
        ForeignKey("currencies.id"),
        nullable=False,
    )
    rate_to_rub: Mapped[Decimal] = mapped_column(
        Numeric(EXCHANGE_RATE_PRECISION, EXCHANGE_RATE_SCALE),
        nullable=False,
    )
    rate_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )

    currency: Mapped[Currency] = relationship(
        back_populates="rates",
    )

    def __repr__(self) -> str:
        """Возвращает строковое представление курса валюты."""
        return (
            f"ExchangeRate("
            f"id={self.id!r}, "
            f"currency_id={self.currency_id!r}, "
            f"rate_to_rub={self.rate_to_rub!r}, "
            f"rate_date={self.rate_date!r}"
            ")"
        )
