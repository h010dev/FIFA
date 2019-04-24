import scrapy
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import reactor, defer
from twisted.internet.task import LoopingCall
from fifa_data.items import ProxyItem
from proxies.proxy_generator import proxies
from user_agents.user_agent_generator import user_agent


class FateProxySpider(scrapy.Spider):

    name = 'fate_proxy'
    start_urls = ['https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list']

    custom_settings = {
        # DATABASE SETTINGS
        'MONGO_DB': 'sofifa',
        'COLLECTION_NAME': 'proxies',

        # SPIDER LOGGING
        'LOG_ENABLED': True,
        'LOG_LEVEL': 'DEBUG',

        # EXTENSION ACTIVATION
        'PROXY_POOL_ENABLED': True,
        'EXTENSIONS': {
            'spidermon.contrib.scrapy.extensions.Spidermon': 510,
        },

        # BAN PREVENTION
        'ROTATING_PROXY_LIST': proxies,
        'USER_AGENTS': user_agent,

        # MISC. SETTINGS
        'HTTPCACHE_ENABLED': False,
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_TIMEOUT': 30,

        # PIPELINES, MIDDLEWARES, AND EXTENSIONS
        'ITEM_PIPELINES': {
            'fifa_data.pipelines.ProxyPipeline': 302,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
            'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
            'rotating_proxies.middlewares.BanDetectionMiddleware': 620
        },
    }

    def parse(self, response):

        loader = ItemLoader(item=ProxyItem(), response=response)
        loader.add_xpath('ip_dump', ".//body/p/text()")

        yield loader.load_item()


def main():

    configure_logging()
    runner = CrawlerRunner()
    d = runner.crawl(FateProxySpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()


def task():

    configure_logging()
    runner = CrawlerRunner()
    task = LoopingCall(lambda: runner.crawl(FateProxySpider))
    task.start(60 * 15)
    reactor.run()


if __name__ == '__main__':
    task()
