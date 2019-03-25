# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SofifaItem(scrapy.Item):

    name = scrapy.Field()
    position = scrapy.Field()
    age = scrapy.Field()
    overall = scrapy.Field()
    potential = scrapy.Field()
    team = scrapy.Field()
    contract = scrapy.Field()
    value = scrapy.Field()
    wage = scrapy.Field()
    total_stats = scrapy.Field()
    hits_comments = scrapy.Field()
