"""Middleware Scrapy-парсера."""

from scrapy import signals


class ParserSpiderMiddleware:
    """Spider middleware Scrapy-парсера."""

    @classmethod
    def from_crawler(cls, crawler):
        """Создаёт middleware через crawler Scrapy."""
        middleware = cls()
        crawler.signals.connect(
            middleware.spider_opened,
            signal=signals.spider_opened,
        )
        return middleware

    def process_spider_input(self, response, spider):
        """Обрабатывает response перед передачей в spider."""
        return None

    def process_spider_output(self, response, result, spider):
        """Обрабатывает результат работы spider."""
        yield from result

    def process_spider_exception(self, response, exception, spider):
        """Обрабатывает исключения spider."""
        pass

    async def process_start(self, start):
        """Обрабатывает стартовые request-объекты spider."""
        async for item_or_request in start:
            yield item_or_request

    def spider_opened(self, spider):
        """Логирует открытие spider."""
        spider.logger.info('Spider opened: %s', spider.name)


class ParserDownloaderMiddleware:
    """Downloader middleware Scrapy-парсера."""

    @classmethod
    def from_crawler(cls, crawler):
        """Создаёт middleware через crawler Scrapy."""
        middleware = cls()
        crawler.signals.connect(
            middleware.spider_opened,
            signal=signals.spider_opened,
        )
        return middleware

    def process_request(self, request, spider):
        """Обрабатывает request перед загрузкой."""
        return None

    def process_response(self, request, response, spider):
        """Обрабатывает response после загрузки."""
        return response

    def process_exception(self, request, exception, spider):
        """Обрабатывает исключения downloader."""
        pass

    def spider_opened(self, spider):
        """Логирует открытие spider."""
        spider.logger.info('Spider opened: %s', spider.name)
