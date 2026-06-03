"""Pydantic-схемы валют."""

from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class CurrencyDTO(BaseModel):
    """Схема валюты."""

    id: int
    code: str
    name: str
    nominal: int

    model_config = ConfigDict(from_attributes=True)


class ExchangeRateDTO(BaseModel):
    """Схема курса валюты."""

    id: int
    currency: CurrencyDTO
    rate_to_rub: Decimal
    rate_date: date

    model_config = ConfigDict(from_attributes=True)
