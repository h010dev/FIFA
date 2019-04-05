# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from fifa_market_analysis.items import TeamStatItem


class SofifaTeamsSpider(CrawlSpider):

    name = 'sofifa_teams'

    allowed_domains = ['sofifa.com']
    start_urls = ['http://sofifa.com/teams/club']

    rules = (
        Rule(
            LinkExtractor(
                deny=(
                    r'\?', r'/players/', r'/help/'
                )
            ),
            callback='parse_start_url',
            follow=True
        ),
        # Rule(
        #     LinkExtractor(
        #         deny=(
        #             r'\?'
        #         ),
        #         restrict_xpaths="//div[@class='col-name text-ellipsis rtl']/a/@href"
        #     ),
        #     callback='parse_item',
        #     follow=True
        # ),
        # Rule(
        #     LinkExtractor(
        #         restrict_xpaths="//a[text()='Next']"
        #     ), callback='parse_item',
        #     follow=True
        # )
    )

    def parse_start_url(self, response):
        for row in response.xpath("//table[@class='table table-hover persist-area']/tbody/tr"):
            loader = ItemLoader(item=TeamStatItem(), selector=row, response=response)
            loader.add_xpath('id', ".//a[contains(@href, 'team/')]/@href")
            loader.add_xpath('nationality', "(.//div[@class='col-name text-ellipsis rtl'])[2]/a/text()")
            loader.add_xpath('region', "(.//div[@class='col-name text-ellipsis rtl'])[2]/div/a/text()")
            loader.add_xpath('num_players', ".//td[@class='col text-center'][last()]/div/text()")
            loader.add_xpath('hits', ".//div[@class='col-comments text-right text-ellipsis rtl']/text()")
            loader.add_xpath('comments', ".//div[@class='col-comments text-right text-ellipsis rtl']/text()")

            yield loader.load_item()

    def parse_item(self, response):
        # loader.add_xpath('club_name', "")
        # loader.add_xpath('division', "")
        pass

