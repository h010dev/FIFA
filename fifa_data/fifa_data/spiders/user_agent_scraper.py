import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule
from scrapy.utils.log import configure_logging

from twisted.internet import reactor

from fifa_data.items import UserAgentScraperItem
from fifa_data.useragent_settings import useragent_settings
from proxies.proxy_generator import gen_proxy_list
from user_agents.user_agent_generator import gen_useragent_list


class UserAgentScraperSpider(CrawlSpider):

    """
    Collects all user-agents from whatismybrowser.com, to be used by
    both this spider and others.
    """

    name = 'user_agent_scraper'

    proxies = gen_proxy_list()
    user_agent = gen_useragent_list()

    allowed_domains = [
        'developers.whatismybrowser.com'
    ]

    start_urls = [
        'https://developers.whatismybrowser.com/useragents/explore/'
    ]

    rules = (
        Rule(
            LinkExtractor(
                allow=([
                    r'^https://developers.whatismybrowser.com/useragents/explore/'
                ]),
                deny=([
                    r'order_by',
                    r'\/operating_platform\/',
                    r'\/parse\/',
                    r'\/legal\/'
                ])
            ),
            callback='parse_item',
            follow=True
        ),
        Rule(
            LinkExtractor(
                deny=([
                    r'order_by',
                    r'\/operating_platform\/',
                    r'\/parse\/',
                    r'\/legal\/'
                ]),
                restrict_xpaths="//p[@class='browse-all']/a"
            ),
            callback='parse_item',
            follow=True
        ),
        Rule(
            LinkExtractor(
                deny=([
                    r'order_by',
                    r'\/operating_platform\/',
                    r'\/parse\/',
                    r'\/legal\/'
                ]),
                restrict_xpaths=([
                    "//a[@class='maybe-long'][contains(text(), 'Computer')]",
                    "//a[@class='maybe-long'][contains(text(), 'Server')]",
                    "//a[@class='maybe-long'][contains(text(), 'Chrome')]",
                    "//a[@class='maybe-long'][contains(text(), 'Opera')]",
                    "//a[@class='maybe-long'][contains(text(), 'Server')]",
                    "//a[@class='maybe-long'][contains(text(), 'Tableau')]",
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
                    "//a[@class='maybe-long'][text()='Windows']"
                ])
            ),
            callback='parse_item',
            follow=True
        ),
        Rule(
            LinkExtractor(
                deny=([
                    r'order_by',
                    r'\/operating_platform\/',
                    r'\/parse\/',
                    r'\/legal\/'
                ]),
                restrict_xpaths="//div[@id='pagination']/a[text()='>']"
            ),
            callback='parse_item',
            follow=True
        )
    )

    custom_settings = useragent_settings(
        name=name,
        database='agents_proxies',
        collection='user_agents',
        proxies=proxies,
        user_agent=user_agent,
        validator='UserAgentItem',
        timeout=60*2
    )

    def parse_item(self, response):

        """
        @url https://developers.whatismybrowser.com/useragents/explore
        /software_name/chrome/
        @returns items 1 10
        @returns requests 0 0
        @scrapes user_agent_generator.py
        """

        for row in response.xpath("//div[@class='content-base']//tbody/tr"):

            loader = ItemLoader(
                UserAgentScraperItem(),
                selector=row,
                response=response
            )

            loader.add_xpath(
                'user_agent',
                ".//td[@class='useragent']/a/text()"
            )
            loader.add_xpath(
                'version',
                ".//td[@class='useragent']/following-sibling::td[1]/text()"
            )
            loader.add_xpath(
                'OS',
                ".//td[@class='useragent']/following-sibling::td[2]/text()"
            )
            loader.add_xpath(
                'hardware_type',
                ".//td[@class='useragent']/following-sibling::td[3]/text()"
            )
            loader.add_xpath(
                'popularity',
                ".//td[@class='useragent']/following-sibling::td[4]/text()"
            )

            self.logger.info(f'Parse function called on {response.url}')

            yield loader.load_item()


def main():

    configure_logging()
    runner = CrawlerRunner()

    d = runner.crawl(UserAgentScraperSpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()


if __name__ == '__main__':
    main()
