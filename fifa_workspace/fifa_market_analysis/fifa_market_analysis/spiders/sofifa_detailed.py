# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class SofifaDetailedSpider(CrawlSpider):
    name = 'sofifa_detailed'
    allowed_domains = ['sofifa.com']
    start_urls = ['http://sofifa.com/players/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//a[contains(@href, 'player/')]"), callback='parse_item', follow=True)
    )

    def parse_item(self, response):

        for stat in response.xpath("//div[@class='teams']/div[@class='columns']/div[@class='column col-4'][1]/ul"):
            yield {
                'player':
                    response.xpath("//div[@class='info']/h1/text()").extract_first(),
                'preferred_foot':
                    stat.xpath(".//li/label[text()='Preferred Foot']/following::text()").extract_first(),
                'international_reputation':
                    stat.xpath(".//li/label[text()='International Reputation']/following::text()").extract_first(),
                'weak_foot':
                    stat.xpath(".//li/label[text()='Weak Foot']/following::text()").extract_first(),
                'skill_moves':
                    stat.xpath(".//li/label[text()='Skill Moves']/following::text()").extract_first(),
                'work_rate':
                    stat.xpath(".//li/label[text()='Work Rate']/following::span/text()").extract_first(),
                'body_type':
                    stat.xpath(".//li/label[text()='Body Type']/text()/following::span/text()").extract_first(),
                'real_face':
                    stat.xpath(".//li/label[text()='Real Face']/text()/following::span/text()").extract_first(),
                'release_clause':
                    stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first()
            }
