# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join
import re


def convert_currency_format(value):

    """
    Strips away currency symbol and applies multiplier based on abbreviation (K to 1,000, M to 1,000,000).

    >>> convert_currency_format('€110.5M')
    >>> 110500000.0

    >>> convert_currency_format('€110K')
    >>> 110000.0

    >>> convert_currency_format('99.5M')
    >>> 99500000.0

    >>> convert_currency_format('21')
    >>> 21.0

    >>> convert_currency_format('€190')
    >>> 190.0

    >>> convert_currency_format(0)
    >>> 0.0
    """

    pattern = r'\W|[0-9.]+|[a-zA-Z]'

    if type(value) is str:
        if re.findall(pattern, value)[0] == u"\u20ac" and re.findall(pattern, value)[-1] == 'K':
            new_value = float(re.findall(pattern, value)[1]) * 1000
            return new_value
        elif re.findall(pattern, value)[0] == u"\u20ac" and re.findall(pattern, value)[-1] == 'M':
            new_value = float(re.findall(pattern, value)[1]) * 1000000
            return new_value
        elif re.findall(pattern, value)[0] == u"\u20ac" and re.findall(pattern, value)[-1] != ('M' or 'K'):
            new_value = float(re.findall(pattern, value)[1])
            return new_value
        elif re.findall(pattern, value)[0] != u"\u20ac" and re.findall(pattern, value)[-1] != ('M' or 'K'):
            new_value = float(re.findall(pattern, value)[0])
            return new_value
    else:
        return float(value)


def get_id(value):

    pattern = r'ID:\ |[0-9]+'
    match = re.findall(pattern, value)[-1]
    return match


class SofifaItem(scrapy.Item):

    id = scrapy.Field(
        input_processor=MapCompose(get_id, eval),
        output_processor=TakeFirst()
    )
    name = scrapy.Field()
    position = scrapy.Field()
    age = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )
    overall = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )
    potential = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )
    team = scrapy.Field()
    contract = scrapy.Field()
    value = scrapy.Field(
        input_processor=MapCompose(convert_currency_format),
        output_processor=TakeFirst()
    )
    wage = scrapy.Field(
        input_processor=MapCompose(convert_currency_format),
        output_processor=TakeFirst()
    )
    total_stats = scrapy.Field(
        input_processor=MapCompose(convert_currency_format),
        output_processor=TakeFirst()
    )
    hits_comments = scrapy.Field()


class ImageItem(scrapy.Item):
    images = scrapy.Field()
    image_urls = scrapy.Field()
