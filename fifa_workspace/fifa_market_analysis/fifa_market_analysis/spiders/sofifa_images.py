# -*- coding: utf-8 -*-
import scrapy


class SofifaImagesSpider(scrapy.Spider):
    name = 'sofifa_images'
    allowed_domains = ['sofifa.com/players']
    start_urls = ['http://sofifa.com/players/']

    def parse(self, response):
        pass
