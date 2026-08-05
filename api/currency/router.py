"""API-ручки валют."""

from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.constants import CURRENCY_NOT_FOUND_ERROR
from core.db import get_async_session
from core.exceptions import CurrencyNotFoundError
from domain.auth.dependencies import get_current_user
from domain.currency.dto import CurrencyDTO, ExchangeRateDTO
from domain.currency.service import CurrencyService
from domain.users.models import User

router = APIRouter(prefix="/currencies", tags=["currencies"])


@router.get(
    "",
    response_model=list[CurrencyDTO],
)
async def list_currencies(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> list[CurrencyDTO]:
    """Возвращает список валют."""
    service = CurrencyService(session)
    currencies = await service.list_currencies()

    return [CurrencyDTO.model_validate(currency) for currency in currencies]


@router.get(
    "/{currency_code}",
    response_model=ExchangeRateDTO,
)
async def get_latest_rate(
    currency_code: str,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> ExchangeRateDTO:
    """Возвращает последний курс валюты."""
    service = CurrencyService(session)

    try:
        rate = await service.get_latest_rate(currency_code)
    except CurrencyNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=CURRENCY_NOT_FOUND_ERROR,
        ) from error

    return ExchangeRateDTO.model_validate(rate)


@router.get(
    "/{currency_code}/history",
    response_model=list[ExchangeRateDTO],
)
async def get_rate_history(
    currency_code: str,
    start_date: Annotated[date, Query()],
    end_date: Annotated[date, Query()],
    session: Annotated[AsyncSession, Depends(get_async_session)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> list[ExchangeRateDTO]:
    """Возвращает историю курсов валюты за период."""
    if start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Start date must not be later than end date",
        )

    service = CurrencyService(session)

    try:
        rates = await service.get_rate_history(
            target_code=currency_code,
            start_date=start_date,
            end_date=end_date,
        )
    except CurrencyNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=CURRENCY_NOT_FOUND_ERROR,
        ) from error

    return [ExchangeRateDTO.model_validate(rate) for rate in rates]


@router.get(
    "/{currency_code}/all",
    response_model=list[ExchangeRateDTO],
)
async def get_rates_for_currency(
    currency_code: str,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> list[ExchangeRateDTO]:
    """Возвращает всю историю курсов валюты."""
    service = CurrencyService(session)

    try:
        rates = await service.get_rates_for_currency(currency_code)
    except CurrencyNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=CURRENCY_NOT_FOUND_ERROR,
        ) from error

    return [ExchangeRateDTO.model_validate(rate) for rate in rates]
