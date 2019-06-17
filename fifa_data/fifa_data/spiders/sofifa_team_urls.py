import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from fifa_data.items import NationalTeamStats
from fifa_data.sofifa_settings import sofifa_settings
from scrapy.utils.log import configure_logging
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor

from proxies.proxy_generator import gen_proxy_list
from user_agents.user_agent_generator import gen_useragent_list

class SofifaTeamUrlsSpider(CrawlSpider):

    name = 'team_pages'

    proxies = gen_proxy_list()
    user_agent = gen_useragent_list()

    allowed_domains = [
        'sofifa.com'
    ]

    start_urls = [
        'https://sofifa.com/teams/national/'
    ]

    rules = (

        Rule(
            LinkExtractor(
                deny=(
                    [
                        r'\?',
                        r'/[0-9]+',
                        r'/forgot',
                        r'/shortlist',
                        r'/authorize',
                        r'/leagues',
                        r'/squad',
                        r'/help',
                        r'/compare',
                        r'/players',
                        r'/teams'
                    ]
                )
            ),
            callback='parse_start_url',
            follow=True
        ),

        Rule(
            LinkExtractor(
                restrict_xpaths="//a[text()='Next']"
            ),
            callback='parse_item',
            follow=True
        )
    )

    custom_settings = sofifa_settings(
        name=name,
        database='sofifa',
        proxies=proxies,
        user_agent=user_agent,
        collection='team_urls',
        validator='TeamItem'
    )

    def parse_start_url(self, response):

        """
        Parse main page for data that is not available in extracted links.
        """

        for row in response.xpath(
                "//table[@class='table table-hover persist-area']/tbody/tr"
        ):

            loader = ItemLoader(
                item=NationalTeamStats(),
                selector=row,
                response=response
            )

            loader.add_xpath(
                'id',
                ".//a[contains(@href, 'team/')]/@href"
            )

            loader.add_xpath(
                'nationality',
                ".//a[contains(@href, 'teams?na')]/text()"
            )

            loader.add_xpath(
                'region',
                ".//a[contains(@href, 'teams?ct')]/text()"
            )

            loader.add_xpath(
                'num_players',
                ".//td[@class='col text-center'][last()]/div/text()"
            )

            loader.add_xpath(
                'hits',
                ".//div[@class='col-comments text-right text-ellipsis rtl']\
                /text()"
            )

            loader.add_xpath(
                'comments',
                ".//div[@class='col-comments text-right text-ellipsis rtl']\
                /text()"
            )

            loader.add_xpath(
                'team_page',
                ".//a[contains(@href, 'team/')]/@href"
            )

            yield loader.load_item()


def main():

    configure_logging()
    runner = CrawlerRunner()

    d = runner.crawl(SofifaTeamUrlsSpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()


if __name__ == '__main__':
    main()
