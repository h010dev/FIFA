# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import ImageItem
from scrapy.loader import ItemLoader


class SofifaImagesSpider(CrawlSpider):
    name = 'sofifa_images'
    allowed_domains = ['sofifa.com']
    start_urls = ['http://sofifa.com/players/']

    rules = (
        Rule(LinkExtractor(deny=([r'\?', r'[0-9]+/[0-9]+/', r'/changeLog', r'/live', r'/squads', r'/calculator/']),
                           restrict_xpaths="//a[contains(@href, 'player/')]"), callback='parse', follow=True),
        # Rule(LinkExtractor(restrict_xpaths="//a[text()='Next']"), callback='parse', follow=True)
    )

    def parse_item(self, response):

        for img in response.xpath("//div/div/article/div/img"):
            loader = ItemLoader(item=ImageItem(), selector=img)
            img_url = img.xpath("./@data-src").get()
            loader.add_value('image_urls', img_url)
            loader.add_xpath('id', ".//div[@class='info']/h1/text()")
            yield loader.load_item()
