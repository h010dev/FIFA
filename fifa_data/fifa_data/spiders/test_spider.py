# import scrapy
# import logging
# import os
# from scrapy.utils.log import configure_logging
# from scrapy.crawler import CrawlerRunner
# from logging.handlers import TimedRotatingFileHandler
# from twisted.internet import reactor
#
#
# class TestSpider(scrapy.Spider):
#
#     name = 'test_spider'
#     start_urls = ['http://quotes.toscrape.com/']
#
#     configure_logging(install_root_handler=False)
#
#     log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
#     log_level = logging.INFO
#     log_path = 'C:\\Users\\E46Racing\\Documents\\PycharmProjects\\FIFA\\fifa_data'
#     log_dir = os.path.join(log_path, 'logs')
#     log_file = os.path.join(log_dir, 'test_log.log')
#
#     logging.basicConfig(
#         format=log_format,
#         level=log_level
#     )
#
#     rotating_file_log = TimedRotatingFileHandler(log_file, when='S', interval=1, backupCount=5)
#     rotating_file_log.setFormatter(logging.Formatter(log_format))
#
#     root_logger = logging.getLogger()
#     root_logger.addHandler(rotating_file_log)
#
#     def parse(self, response):
#         for row in response.xpath("//div[@class='row']/div[@class='col-md-8']/div"):
#             yield {
#                 'quote': row.xpath(".//span[@class='text']/text()").get(),
#             }
#
#         next_page = response.xpath("//li[@class='next']/a/@href").get()
#         if next_page is not None:
#             next_page_link = response.urljoin(next_page)
#             yield scrapy.Request(url=next_page_link, callback=self.parse)
#
#
# def main():
#
#     runner = CrawlerRunner()
#
#     d = runner.crawl(TestSpider)
#     d.addBoth(lambda _: reactor.stop())
#     reactor.run()
#
#
# if __name__ == '__main__':
#     main()
