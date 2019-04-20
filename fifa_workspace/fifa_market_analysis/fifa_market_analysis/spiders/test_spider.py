import scrapy
import logging
import datetime
from scrapy.utils.log import configure_logging
from logging.handlers import TimedRotatingFileHandler


class TestSpider(scrapy.Spider):

    name = 'test_spider'
    start_urls = ['http://quotes.toscrape.com/']

    custom_settings = {
        'EXTENSIONS': {
            'scrapy.extensions.test_extension.CustomStats': 500
        }
    }

    configure_logging(install_root_handler=False)

    log_format = '%(levelname)s: %(message)s'
    log_level = logging.DEBUG
    log_file = 'test_log_file.log'
    logging.basicConfig(
        filename=log_file,
        format=log_format,
        level=log_level
    )

    timed_file_log = TimedRotatingFileHandler(log_file, when='S', interval=1, backupCount=5)
    timed_file_log.setFormatter(logging.Formatter(log_format))
    root_logger = logging.getLogger()
    root_logger.addHandler(timed_file_log)

    def parse(self, response):
        for row in response.xpath("//div[@class='row']/div[@class='col-md-8']/div"):
            yield {
                'quote': row.xpath(".//span[@class='text']/text()").get(),
            }

        next_page = response.xpath("//li[@class='next']/a/@href").get()
        if next_page is not None:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)
