# -*- coding: utf-8 -*-
import scrapy
import json


class FutbinSpider(scrapy.Spider):

    name = 'futbin'
    allowed_domains = ['www.futbin.com']

    def start_requests(self):
        yield scrapy.Request(url="https://www.futbin.com/auctionsGraph?type=live_graph&console=XONE",
                             callback=self.parse)

    def parse(self, response):
        data = json.loads(response.body)

        for val in data['XONE']:
            yield {
                'time_stamp': val[0],
                'trades': val[1]
            }

        for val in data['flag']:
            yield {
                'title': val['title'],
                'description': val['description'],
                'date': val['flag_date']
            }
