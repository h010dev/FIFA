# -*- coding: utf-8 -*-
import scrapy
import json


class FutbinSpider(scrapy.Spider):

    name = 'futbin'
    allowed_domains = ['www.futbin.com']

    def start_requests(self):
        yield scrapy.Request(url="https://www.futbin.com/auctionsGraph?type=live_graph&console=XONE",
                             callback=self.parse_market)

    def parse_market(self, response):
        data = json.loads(response.body)
        with open('fut_market_test.json', 'w') as file:
            file.write(json.dumps(data))

    def parse(self, response):
        pass
