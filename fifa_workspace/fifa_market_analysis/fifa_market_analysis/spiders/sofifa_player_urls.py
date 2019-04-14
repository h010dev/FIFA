import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from fifa_market_analysis.items import SofifaItem, MainPageItem
from fifa_market_analysis.proxy_generator import proxies
from fifa_market_analysis.user_agent_generator import user_agent


class PlayerURLSpider(CrawlSpider):

    name = 'player_pages'

    allowed_domains = ['sofifa.com']
    start_urls = ['https://sofifa.com/players/']

    rules = (
        Rule(LinkExtractor(deny=([r'\?', r'[0-9]+/[0-9]+/', r'/changeLog', r'/live', r'/squads', r'/calculator/',
                                  r'/team/', r'[0-9]+', r'/[a-zA-Z0-9]+$'])),
             callback='parse_start_url', follow=True),
        # Rule(LinkExtractor(restrict_xpaths="//a[text()='Next']"), callback='parse_item', follow=True)
    )

    custom_settings = {
        'MONGO_DB': 'sofifa',
        'HTTPCACHE_ENABLED': False,
        'ITEM_PIPELINES': {
            'fifa_market_analysis.pipelines.MongoDBPipeline': 300,
            'spidermon.contrib.scrapy.pipelines.ItemValidationPipeline': 800,
        },
        'ROBOTSTXT_OBEY': True,
        'COLLECTION_NAME': 'player_urls',
        'SPIDERMON_ENABLED': True,
        'EXTENSIONS': {
            'spidermon.contrib.scrapy.extensions.Spidermon': 500,
        },
        'SPIDERMON_SPIDER_CLOSE_MONITORS': (
            'fifa_market_analysis.monitors.SpiderCloseMonitorSuite',
        ),
        'SPIDERMON_VALIDATION_MODELS': (
            'fifa_market_analysis.validators.PlayerItem',
        ),
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
        },
        'USER_AGENTS': user_agent
    }

    def parse_start_url(self, response):

        """
        @url http://sofifa.com/players/
        @returns items 1 61
        @returns requests 0 0
        @scrapes id_player_main total_stats hits comments
        """

        for row in response.xpath("//table[@class='table table-hover persist-area']/tbody/tr"):
            loader = ItemLoader(item=MainPageItem(), selector=row, response=response)

            loader.add_xpath('id_player_main', ".//a[contains(@href, 'player/')]/@href")
            loader.add_xpath('total_stats', ".//div[@class='col-digit col-tt']/text()")
            loader.add_xpath('hits', ".//div[@class='col-comments text-right text-ellipsis rtl']/text()")
            loader.add_xpath('comments', ".//div[@class='col-comments text-right text-ellipsis rtl']/text()")
            loader.add_xpath('player_page', ".//a[contains(@href, 'player/')]/@href")

            yield loader.load_item()
