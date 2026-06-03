"""Настройки Scrapy-парсера."""

BOT_NAME = 'parser'

NEWSPIDER_MODULE = 'parser.parser.spiders'
SPIDER_MODULES = [NEWSPIDER_MODULE]

ROBOTSTXT_OBEY = False

ITEM_PIPELINES = {
    'parser.parser.pipelines.CurrencyPipeline': 300,
}

TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'

FEED_EXPORT_ENCODING = 'utf-8'
