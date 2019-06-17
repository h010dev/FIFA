import datetime

import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from twisted.internet import reactor

from fifa_data.custom_logging import *
from fifa_data.custom_stats import *
from fifa_data.items import MainPageItem
from fifa_data.sofifa_settings import sofifa_settings
from proxies.proxy_generator import gen_proxy_list
from user_agents.user_agent_generator import gen_useragent_list


class SofifaPlayerURLsSpider(scrapy.Spider):

    """
    Collects all player urls found on sofifa.com to be later scraped by
    the SofifaPlayerPagesSpider. URLs are stored inside the player_urls
    collection at mongodb://mongo_server:27017/sofifa
    """

    name = 'player_pages'

    proxies = gen_proxy_list()
    user_agent = gen_useragent_list()

    custom_settings = sofifa_settings(
        name=name,
        database='sofifa',
        collection='player_urls',
        proxies=proxies,
        user_agent=user_agent,
        validator='PlayerItem'
    )

    allowed_domains = [
        'sofifa.com'
    ]

    start_urls = [
        'https://sofifa.com/players/'
    ]

    rules = (
        Rule(
            LinkExtractor(
                deny=([
                    r'\?',
                    r'[0-9]+/[0-9]+/',
                    r'/changeLog',
                    r'/live',
                    r'/squads',
                    r'/calculator/',
                    r'/team/',
                    r'[0-9]+',
                    r'/[a-zA-Z0-9]+$'
                ])
            ),
            callback='parse_item',
            follow=True
        ),
        Rule(
            LinkExtractor(
                restrict_xpaths="//a[contains(@class, 'button pjax')]/@href"
            ),
            callback='parse_item',
            follow=True
        )
    )

    def parse(self, response):

        """
        @url http://sofifa.com/players/
        @returns items 1 61
        @returns requests 0 0
        @scrapes id_player_main total_stats hits comments player_page
        """

        self.crawler.stats.set_value(
            'page_counter',
            page_counter(response.url)
        )

        for row in response.xpath(
                "//table[@class='table table-hover persist-area']/tbody/tr"
        ):

            loader = ItemLoader(
                item=MainPageItem(),
                selector=row,
                response=response
            )

            loader.add_xpath(
                'id',
                ".//a[contains(@href, 'player/')]/@href"
            )

            loader.add_xpath(
                'total_stats',
                ".//span[contains(@class, 'primary')]/text()"
            )

            loader.add_xpath(
                'hits',
                ".//td[contains(@class, 'comment')]/text()[1]"
            )

            loader.add_xpath(
                'comments',
                ".//td[contains(@class, 'comment')]/text()[2]"
            )

            loader.add_xpath(
                'player_page',
                ".//a[contains(@href, 'player/')]/@href"
            )

            print(response.request.headers['User-Agent'])

            self.logger.info(f'Currently on page {current_page(response.url)}')

            yield loader.load_item()


def main():

    """
    Run this spider a single time only.
    """

    configure_logging()

    runner = CrawlerRunner()

    d = runner.crawl(SofifaPlayerURLsSpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()


if __name__ == '__main__':
    main()
