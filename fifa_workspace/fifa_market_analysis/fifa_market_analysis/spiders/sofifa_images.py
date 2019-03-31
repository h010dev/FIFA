# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import ImageItem
from scrapy.loader import ItemLoader


class SofifaDetailedSpider(CrawlSpider):
    name = 'sofifa_images'
    allowed_domains = ['sofifa.com']
    start_urls = ['http://sofifa.com/players/']

    rules = (
        Rule(LinkExtractor(deny=([r'\?', r'[0-9]+/[0-9]+/', r'/changeLog', r'/live', r'/squads', r'/calculator/']),
                           restrict_xpaths="//a[contains(@href, 'player/')]"), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths="//a[text()='Next']"), callback='parse_item', follow=True)
    )

    def parse_item(self, response):

        face = ImageItem()
        flag = ImageItem()
        club = ImageItem()
        team = ImageItem()

        face_url = []
        flag_url = []
        club_url = []
        team_url = []

        for img in response.xpath("//div/div/article/div/img"):
            face_url.append(img.xpath("./@data-src").get())
            flag_url.append(response.xpath(".//div[@class='meta']/a/img/@data-src").get())
            club_url.append(response.xpath(".//div/ul/li/figure/img/@data-src").getall()[0])
            team_url.append(response.xpath(".//div/ul/li/figure/img/@data-src").getall()[-1])
        face["image_urls"] = face_url
        flag["image_urls"] = flag_url
        club["image_urls"] = club_url
        team["image_urls"] = team_url
        return face, flag, club, team

        # for img in response.xpath("//div/div/article/div/img"):
        #     yield{
        #         'name': response.xpath(".//div[@class='info']/h1/text()").get(),
        #         'face': img.xpath("./@data-src").get(),
        #         'flag': response.xpath(".//div[@class='meta']/a/img/@data-src").get(),
        #         'club': response.xpath(".//div/ul/li/figure/img/@data-src").getall()[0],
        #         'team': response.xpath(".//div/ul/li/figure/img/@data-src").getall()[-1]
        #     }
