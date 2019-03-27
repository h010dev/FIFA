# -*- coding: utf-8 -*-
import scrapy


class FutbinSpider(scrapy.Spider):
    name = 'futbin'
    allowed_domains = ['www.futbin.com/market/auctions']
    start_urls = ['http://www.futbin.com/market/auctions/']

    def parse(self, response):
        pass
