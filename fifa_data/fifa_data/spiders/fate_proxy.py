import scrapy
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import reactor, defer
from twisted.internet.task import LoopingCall
from fifa_data.proxy_settings import proxy_settings
from fifa_data.items import ProxyItem
from proxies.proxy_generator import gen_proxy_list
from user_agents.user_agent_generator import gen_useragent_list
from fifa_data.mongodb_addr import host


class FateProxySpider(scrapy.Spider):

    """
    Collects all proxies from the fate0 proxy list on github, to be used by
    both this spider and others.
    """

    name = 'fate_proxy'

    proxies = gen_proxy_list()
    user_agent = gen_useragent_list()

    start_urls = [
        'https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list'
    ]

    custom_settings = proxy_settings(
        name=name,
        database='agents_proxies',
        collection='proxies',
        proxies=proxies,
        user_agent=user_agent,
        validator='ProxyItem'
    )

    def parse(self, response):

        loader = ItemLoader(
            item=ProxyItem(),
            response=response
        )

        loader.add_xpath(
            'ip_dump',
            ".//body/p/text()"
        )

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
    main()
