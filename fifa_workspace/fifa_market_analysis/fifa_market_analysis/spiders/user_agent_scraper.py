# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from fifa_market_analysis.items import UserAgentScraperItem
import logging
from scrapy.utils.log import configure_logging
import datetime
from fifa_market_analysis.proxy_generator import proxies
from fifa_market_analysis.user_agent_generator import user_agent


class UserAgentScraperSpider(CrawlSpider):

    name = 'user_agent_scraper'

    allowed_domains = ['developers.whatismybrowser.com']
    start_urls = ['https://developers.whatismybrowser.com/useragents/explore/']

    rules = (
        Rule(LinkExtractor(allow=([r"^https://developers.whatismybrowser.com/useragents/explore/"]),
                           deny=([r'order_by', r'\/operating_platform\/', r'\/parse\/', r'\/legal\/'])),
             callback='parse_item',
             follow=True),
        Rule(LinkExtractor(deny=([r'order_by', r'\/operating_platform\/', r'\/parse\/', r'\/legal\/']),
                           restrict_xpaths="//p[@class='browse-all']/a"),
             callback='parse_item',
             follow=True),
        Rule(LinkExtractor(deny=([r'order_by', r'\/operating_platform\/', r'\/parse\/', r'\/legal\/']),
                           restrict_xpaths=(["//a[@class='maybe-long'][contains(text(), 'Computer')]",
                                             "//a[@class='maybe-long'][contains(text(), 'Server')]",
                                             "//a[@class='maybe-long'][contains(text(), 'Chrome')]",
                                             "//a[@class='maybe-long'][contains(text(), 'Opera')]",
                                             "//a[@class='maybe-long'][contains(text(), 'Server')]",
                                             "//a[@class='maybe-long'][contains(text(), 'Tableau')]",
                                             "//a[@class='maybe-long'][contains(text(), 'Internet Explorer')]",
                                             "//a[@class='maybe-long'][contains(text(), 'Googlebot')]",
                                             "//a[@class='maybe-long'][contains(text(), 'Firefox')]",
                                             "//a[@class='maybe-long'][contains(text(), 'Edge')]",
                                             "//a[@class='maybe-long'][contains(text(), 'Comodo')]",
                                             "//a[@class='maybe-long'][contains(text(), 'Chromium')]",
                                             "//a[@class='maybe-long'][contains(text(), 'Bingbot')]",
                                             "//a[@class='maybe-long'][contains(text(), 'Avant')]",
                                             "//a[@class='maybe-long'][contains(text(), 'Unix')]",
                                             "//a[@class='maybe-long'][contains(text(), 'ChromeOS')]",
                                             "//a[@class='maybe-long'][contains(text(), 'bsd')]",
                                             "//a[@class='maybe-long'][contains(text(), 'Mac')]",
                                             "//a[@class='maybe-long'][contains(text(), 'Crawler')]",
                                             "//a[@class='maybe-long'][contains(text(), 'Web Browser')]",
                                             "//a[@class='maybe-long'][contains(text(), 'Trident')]",
                                             "//a[@class='maybe-long'][contains(text(), 'Presto')]",
                                             "//a[@class='maybe-long'][contains(text(), 'Goanna')]",
                                             "//a[@class='maybe-long'][contains(text(), 'Gecko')]",
                                             "//a[@class='maybe-long'][contains(text(), 'Blink')]"
                                             "//a[@class='maybe-long'][text()='Windows']"])),
             callback='parse_item',
             follow=True),
        Rule(LinkExtractor(deny=([r'order_by', r'\/operating_platform\/', r'\/parse\/', r'\/legal\/']),
                           restrict_xpaths="//div[@id='pagination']/a[text()='>']"),
             callback='parse_item',
             follow=True)
    )

    # configure_logging(install_root_handler=False)
    # logging.basicConfig(
    #     filename=f'log_{name}_{datetime.date.today()}.txt',
    #     format='%(levelname)s: %(message)s',
    #     level=logging.INFO
    # )

    custom_settings = {
        'ITEM_PIPELINES': {
            'fifa_market_analysis.pipelines.MongoDBPipeline': 300,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
            'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
            'rotating_proxies.middlewares.BanDetectionMiddleware': 620
        },
        'MONGO_DB': 'agents_proxies',
        'HTTPCACHE_ENABLED': True,
        'COLLECTION_NAME': 'user_agents',
        'JOBDIR': 'pause_resume/agent_proxy_dir',
        'PROXY_POOL_ENABLED': True,
        'ROTATING_PROXY_LIST': proxies,
        'USER_AGENTS': user_agent,
        'DOWNLOAD_TIMEOUT': 30,
        'LOG_LEVEL': 'DEBUG',
        'LOG_ENABLED': True,
        'LOG_FILE': 'user_agent_log.txt',
        'CONCURRENT_REQUESTS_PER_IP': 10,
        'DEPTH_STATS_VERBOSE': True,
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.RFPDupeFilter',
        # 'SPIDER_CONTRACTS': {},
    }

    def parse_item(self, response):

        """
        @url https://developers.whatismybrowser.com/useragents/explore/software_name/chrome/
        @returns items 1 10
        @returns requests 0 0
        @scrapes user_agent
        """

        for row in response.xpath("//div[@class='content-base']//tbody/tr"):

            loader = ItemLoader(UserAgentScraperItem(), selector=row, response=response)

            loader.add_xpath('user_agent', ".//td[@class='useragent']/a/text()")
            loader.add_xpath('version', ".//td[@class='useragent']/following-sibling::td[1]/text()")
            loader.add_xpath('OS', ".//td[@class='useragent']/following-sibling::td[2]/text()")
            loader.add_xpath('hardware_type', ".//td[@class='useragent']/following-sibling::td[3]/text()")
            loader.add_xpath('popularity', ".//td[@class='useragent']/following-sibling::td[4]/text()")

            # print(response.request.headers['proxy'])
            print(response.request.headers['User-Agent'])
            self.logger.info(f'Parse function called on {response.url}')

            yield loader.load_item()
