# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from fifa_market_analysis.items import UserAgentScraperItem


class UserAgentScraperSpider(CrawlSpider):

    name = 'user_agent_scraper'

    allowed_domains = ['developers.whatismybrowser.com']
    start_urls = ['https://developers.whatismybrowser.com/useragents/explore/']

    rules = (
        Rule(
            LinkExtractor(
                allow=(
                    r"^https://developers.whatismybrowser.com/useragents/explore/"
                ),
                deny=(
                    [
                        r'order_by'
                    ]
                )
            ),
            callback='parse_item',
            follow=True
        ),
        Rule(
            LinkExtractor(
                deny=(
                    [
                        r'order_by'
                    ]
                ),
                restrict_xpaths="//p[@class='browse-all']/a"
            ),
            callback='parse_item',
            follow=True
        ),
        Rule(
            LinkExtractor(
                deny=(
                    [
                        r'order_by'
                    ]
                ),
                restrict_xpaths="//a[@class='maybe-long']"
            ),
            callback='parse_item',
            follow=True
        ),
        Rule(
            LinkExtractor(
                deny=(
                    [
                        r'order_by'
                    ]
                ),
                restrict_xpaths="//div[@id='pagination']/a[text()='>']"
            ),
            callback='parse_item',
            follow=True
        )

    )

    custom_settings = {
        'MONGO_DB': 'agents_proxies',
        'HTTPCACHE_ENABLED': True,
        'ITEM_PIPELINES': {
            'fifa_market_analysis.pipelines.MongoDBPipeline': 300,
        },
        'COLLECTION_NAME': 'user_agents',
        'JOBDIR': 'pause_resume/agent_proxy_dir'
    }

    def parse_item(self, response):

        for row in response.xpath("//div[@class='content-base']//tbody/tr"):

            loader = ItemLoader(UserAgentScraperItem(), selector=row, response=response)

            loader.add_xpath('user_agent', ".//td[@class='useragent']/a/text()")
            loader.add_xpath('version', ".//td[@class='useragent']/following-sibling::td[1]/text()")
            loader.add_xpath('OS', ".//td[@class='useragent']/following-sibling::td[2]/text()")
            loader.add_xpath('hardware_type', ".//td[@class='useragent']/following-sibling::td[3]/text()")
            loader.add_xpath('popularity', ".//td[@class='useragent']/following-sibling::td[4]/text()")

            yield loader.load_item()
