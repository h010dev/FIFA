from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import reactor, defer, task
from fifa_data.spiders.sofifa_player_urls import SofifaPlayerURLsSpider
from fifa_data.spiders.sofifa_player_pages import SofifaPlayerPagesSpider
from fifa_data.spiders.sofifa_club_urls import SofifaClubUrlsSpider
import time


@defer.inlineCallbacks
def main():
    runner = CrawlerRunner()
    runner.crawl(SofifaPlayerURLsSpider)
    time.sleep(10)
    yield runner.crawl(SofifaClubUrlsSpider)
    reactor.stop()


if __name__ == '__main__':

    configure_logging()
    runner = CrawlerRunner()

    @defer.inlineCallbacks
    def crawl():
        yield runner.crawl(SofifaPlayerURLsSpider)
        # TODO: second crawl does not work, as it seems to rely on closing the db and reopening to run properly.
        yield runner.crawl(SofifaPlayerPagesSpider)
        reactor.stop()


    crawl()
    reactor.run()
