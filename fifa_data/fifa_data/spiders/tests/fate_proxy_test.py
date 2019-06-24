import atexit
import cProfile
import line_profiler
import pstats
from pstats import SortKey

import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.loader import ItemLoader
from scrapy.utils.log import configure_logging

from twisted.internet import reactor, defer
from twisted.internet.task import LoopingCall

from fifa_data.items import ProxyItem
from fifa_data.mongodb_addr import host
from fifa_data.proxy_settings import proxy_settings
from proxies.proxy_generator import gen_proxy_list
from user_agents.user_agent_generator import gen_useragent_list

profile = line_profiler.LineProfiler()
atexit.register(profile.print_stats)


class FateProxySpider(scrapy.Spider):

    """
    Collects all proxies from the fate0 proxy list on github, to be
    used by both this spider and others.
    """

    name = 'fate_proxy'

    proxies = gen_proxy_list()
    user_agent = gen_useragent_list()

    custom_settings = proxy_settings(
        name=name,
        database='agents_proxies',
        collection='proxy_test_new',
        proxies=proxies,
        user_agent=user_agent,
        validator='ProxyItem'
    )

    start_urls = [
        'https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list'
    ]

    @profile
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

    """
    Run the spider a single time only. Use this when the airflow dag
    for this spider controls the schedule interval (i.e. once per
    15 minutes). Note that the fate0 list gets updated once per 15
    minutes.
    """

    configure_logging()
    runner = CrawlerRunner()
    d = runner.crawl(FateProxySpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()


def task():

    """
    Run this spider continuosly, restarting it every 15 minutes. Use
    this when the airflow dag only instantiates this spider once.
    """

    configure_logging()
    runner = CrawlerRunner()
    task = LoopingCall(lambda: runner.crawl(FateProxySpider))
    task.start(60 * 15)
    reactor.run()


if __name__ == '__main__':
#    cProfile.run('main()', 'restats')
#    p = pstats.Stats('restats')
#    p.sort_stats(SortKey.CUMULATIVE).dump_stats('mystats.txt')
    main()
