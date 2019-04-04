# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import ImageItem
from scrapy.loader import ItemLoader


class PlayerImagesSpider(CrawlSpider):

    name = 'player_images'

    allowed_domains = ['sofifa.com']
    start_urls = ['http://sofifa.com/players/']

    rules = (
        Rule(LinkExtractor(deny=([r'\?', r'[0-9]+/[0-9]+/', r'/changeLog', r'/live', r'/squads', r'/calculator/']),
                           restrict_xpaths="//a[contains(@href, 'player/')]"), callback='parse_item', follow=True),
        # Rule(LinkExtractor(restrict_xpaths="//a[text()='Next']"), callback='parse', follow=True)
    )

    def parse_item(self, response):

        for img in response.xpath("//div[@class='card card-border player fixed-width']"):
            loader = ItemLoader(item=ImageItem(), selector=img)
            img_url = img.xpath("./img/@data-src").get()
            loader.add_value('image_urls', img_url)
            loader.add_xpath('id', ".//div[@class='info']/h1/text()")
            loader.add_xpath('category', "./img/@data-src")
            yield loader.load_item()


class FlagImagesSpider(PlayerImagesSpider):

    name = 'flag_images'

    def parse_item(self, response):

        for img in response.xpath("//div[@class='card card-border player fixed-width']"):
            loader = ItemLoader(item=ImageItem(), selector=img)
            img_url = img.xpath(".//a/img/@data-src").get()
            loader.add_value('image_urls', img_url)
            loader.add_xpath('id', ".//div[@class='info']/h1/text()")
            loader.add_xpath('category', ".//a/img/@data-src")
            yield loader.load_item()


class ClubImagesSpider(PlayerImagesSpider):

    name = 'club_images'

    def parse_item(self, response):

        for img in response.xpath("//div[@class='card card-border player fixed-width']"):
            loader = ItemLoader(item=ImageItem(), selector=img)
            img_url = img.xpath(".//div[@class='column col-4'][last()-1]//img/@data-src").get()
            loader.add_value('image_urls', img_url)
            loader.add_xpath('id', ".//div[@class='info']/h1/text()")
            loader.add_xpath('category', ".//div[@class='column col-4'][last()-1]//img/@data-src")
            loader.add_value('team_or_club', 'club')
            yield loader.load_item()


class TeamImagesSpider(PlayerImagesSpider):

    name = 'team_images'

    def parse_item(self, response):

        for img in response.xpath("//div[@class='card card-border player fixed-width']"):
            loader = ItemLoader(item=ImageItem(), selector=img)
            img_url = img.xpath(".//div[@class='column col-4'][last()]//img/@data-src").get()
            loader.add_value('image_urls', img_url)
            loader.add_xpath('id', ".//div[@class='info']/h1/text()")
            loader.add_xpath('category', ".//div[@class='column col-4'][last()]//img/@data-src")
            loader.add_value('team_or_club', 'team')
            yield loader.load_item()

