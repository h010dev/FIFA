from datetime import datetime

import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider
from scrapy.utils.log import configure_logging

from pymongo import MongoClient
from twisted.internet import reactor

from fifa_data.items import DetailedTeamStatItem
from fifa_data.mongodb_addr import host, port
from fifa_data.tests.sofifa_settings import sofifa_settings
from proxies.proxy_generator import gen_proxy_list
from user_agents.user_agent_generator import gen_useragent_list

from fifa_data.spiders.tests.sofifa_club_pages_test import SofifaClubPagesSpider1
from fifa_data.spiders.tests.sofifa_club_pages_test_2 import SofifaClubPagesSpider2
from fifa_data.spiders.tests.sofifa_club_pages_test_3 import SofifaClubPagesSpider3
from fifa_data.spiders.tests.sofifa_club_pages_test_4 import SofifaClubPagesSpider4
from fifa_data.spiders.tests.sofifa_club_pages_test_5 import SofifaClubPagesSpider5
from fifa_data.spiders.tests.sofifa_club_pages_test_6 import SofifaClubPagesSpider6
from fifa_data.spiders.tests.sofifa_club_pages_test_7 import SofifaClubPagesSpider7
from fifa_data.spiders.tests.sofifa_club_pages_test_8 import SofifaClubPagesSpider8
from fifa_data.spiders.tests.sofifa_club_pages_test_9 import SofifaClubPagesSpider9
from fifa_data.spiders.tests.sofifa_club_pages_test_10 import SofifaClubPagesSpider10


def main():
    configure_logging()
    runner = CrawlerRunner()
    runner.crawl(SofifaClubPagesSpider1)
    runner.crawl(SofifaClubPagesSpider2)
    runner.crawl(SofifaClubPagesSpider3)
    runner.crawl(SofifaClubPagesSpider4)
    runner.crawl(SofifaClubPagesSpider5)
    runner.crawl(SofifaClubPagesSpider6)
    runner.crawl(SofifaClubPagesSpider7)
    runner.crawl(SofifaClubPagesSpider8)
    runner.crawl(SofifaClubPagesSpider9)
    runner.crawl(SofifaClubPagesSpider10)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    reactor.run()


if __name__ == '__main__':
    main()
