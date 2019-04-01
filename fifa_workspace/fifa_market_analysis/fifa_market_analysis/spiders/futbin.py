# -*- coding: utf-8 -*-
import scrapy


class FutbinSpider(scrapy.Spider):
    name = 'futbin'
    allowed_domains = ['www.futbin.com']
    start_urls = ['http://www.futbin.com/']

    def parse(self, response):
        pass
