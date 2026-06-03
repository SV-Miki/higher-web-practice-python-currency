"""Scrapy items для валют."""

import scrapy


class CurrencyItem(scrapy.Item):
    """Item с данными валюты из XML ЦБ РФ."""

    code = scrapy.Field()
    name = scrapy.Field()
    nominal = scrapy.Field()
    rate_to_rub = scrapy.Field()
    rate_date = scrapy.Field()
