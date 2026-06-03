"""Паук для загрузки курсов валют с сайта ЦБ РФ."""

from datetime import date, datetime

from scrapy import Request, Spider

from core.constants import (
    CBR_REQUEST_DAY_FORMAT,
    CBR_REQUEST_MONTH_FORMAT,
    CBR_REQUEST_YEAR_FORMAT,
    CBR_RESPONSE_DATE_FORMAT,
    CBR_URL_TEMPLATE,
)
from parser.parser.items import CurrencyItem


class CbrSpider(Spider):
    """Паук для получения ежедневных курсов валют ЦБ РФ."""

    name = 'cbr'

    async def start(self):
        """Создаёт запрос к XML с курсами валют на текущую дату."""
        today = date.today()
        url = self._build_url(today)
        yield Request(url=url, callback=self.parse)

    def parse(self, response):
        """Парсит XML с курсами валют."""
        rate_date = datetime.strptime(
            response.xpath('//ValCurs/@Date').get(),
            CBR_RESPONSE_DATE_FORMAT,
        ).date()

        for currency in response.xpath('//Valute'):
            value = currency.xpath('Value/text()').get()

            yield CurrencyItem(
                code=currency.xpath('CharCode/text()').get(),
                name=currency.xpath('Name/text()').get(),
                nominal=int(currency.xpath('Nominal/text()').get()),
                rate_to_rub=value.replace(',', '.'),
                rate_date=rate_date,
            )

    @staticmethod
    def _build_url(rate_date: date) -> str:
        """Создаёт URL для запроса курсов валют на указанную дату."""
        return CBR_URL_TEMPLATE.format(
            day=rate_date.strftime(CBR_REQUEST_DAY_FORMAT),
            month=rate_date.strftime(CBR_REQUEST_MONTH_FORMAT),
            year=rate_date.strftime(CBR_REQUEST_YEAR_FORMAT),
        )
