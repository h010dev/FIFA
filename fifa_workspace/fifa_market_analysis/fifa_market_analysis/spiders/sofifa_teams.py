# -*- coding: utf-8 -*-
import scrapy


class SofifaTeamsSpider(scrapy.Spider):
    name = 'sofifa_teams'
    allowed_domains = ['sofifa.com']
    start_urls = ['http://sofifa.com/']

    def parse(self, response):
        pass
