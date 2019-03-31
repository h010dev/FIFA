# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import ImageItem


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
        image = ImageItem()
        img_urls = []

        for img in response.xpath("//div/div/article/div/img"):
            img_urls.append(img.xpath("./@data-src").get())
        image["image_urls"] = img_urls
        return image






            # yield{
            #     'name': response.xpath(".//div[@class='info']/h1/text()").get(),
            #     'face': img.xpath("./@data-src").get(),
            #     'flag': response.xpath(".//div[@class='meta']/a/img/@data-src").get(),
            #     'club': response.xpath(".//div/ul/li/figure/img/@data-src").getall()[0],
            #     'team': response.xpath(".//div/ul/li/figure/img/@data-src").getall()[-1]
            # }
