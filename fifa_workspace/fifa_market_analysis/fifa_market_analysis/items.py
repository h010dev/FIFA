# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Identity
import re
from datetime import datetime


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


def get_name(value):

    pattern = r'^[^\(]+'
    match = re.findall(pattern, value)[0]
    return match


def get_age(value):

    pattern_1 = r'Age\ [0-9]+'
    match = re.findall(pattern_1, value)[0]
    pattern_2 = r'[0-9]+'
    age_in_years = re.findall(pattern_2, match)
    return age_in_years


def get_dob(value):

    pattern = r'[a-zA-Z]+\ [0-9]+,\ [0-9]+'
    match = re.findall(pattern, value)[0]
    datetime_dob = datetime.strptime(match, '%b %d, %Y')
    return datetime_dob


def get_height(value):

    pattern_1 = r'[0-9]+\W[0-9]+\W'
    match = re.findall(pattern_1, value)[0]
    pattern_2 = r'([0-9]+)'
    feet = eval(re.findall(pattern_2, match)[0]) * 12
    inches = eval(re.findall(pattern_2, match)[1])
    height_in_inches = feet + inches
    return height_in_inches


def get_weight(value):

    pattern_1 = r'[0-9]+lbs'
    match = re.findall(pattern_1, value)[0]
    pattern_2 = r'[0-9]+'
    weight_in_lbs = re.findall(pattern_2, match)
    return weight_in_lbs


def get_date(value):

    try:
        date = datetime.strptime(value, '%b %d, %Y')
        return date
    except ValueError:
        date = datetime.strptime(value, '%Y')
        return date


class SofifaItem(scrapy.Item):

    # GENERAL INFO

    id = scrapy.Field(
        input_processor=MapCompose(get_id, eval),
        output_processor=TakeFirst()
    )

    name = scrapy.Field(
        input_processor=MapCompose(get_name, str),
        output_processor=TakeFirst()
    )

    full_name = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )

    age = scrapy.Field(
        input_processor=MapCompose(get_age, eval),
        output_processor=TakeFirst()
    )

    dob = scrapy.Field(
        input_processor=MapCompose(get_dob),
        output_processor=TakeFirst()
    )

    height = scrapy.Field(
        input_processor=MapCompose(get_height),
        output_processor=TakeFirst()
    )
    weight = scrapy.Field(
        input_processor=MapCompose(get_weight, eval),
        output_processor=TakeFirst()
    )

    nationality = scrapy.Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )

    # PLAYER STATS

    preferred_foot = scrapy.Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )

    international_reputation = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    weak_foot = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    skill_moves = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    work_rate = scrapy.Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )

    body_type = scrapy.Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )

    real_face = scrapy.Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )

    # CLUB/TEAM STATS

    value = scrapy.Field(
        input_processor=MapCompose(convert_currency_format),
        output_processor=TakeFirst()
    )

    wage = scrapy.Field(
        input_processor=MapCompose(convert_currency_format),
        output_processor=TakeFirst()
    )

    release_clause = scrapy.Field(
        input_processor=MapCompose(convert_currency_format),
        output_processor=TakeFirst()
    )

    club_name = scrapy.Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )

    club_rating = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    club_position = scrapy.Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )

    club_jersey_number = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    club_join_date = scrapy.Field(
        input_processor=MapCompose(lambda x: datetime.strptime(x, '%b %d, %Y')),
        output_processor=TakeFirst()
    )

    # club_contract_end_date = scrapy.Field(
    #     input_processor=Identity(),
    #     output_processor=TakeFirst()
    # )

    club_contract_end_date = scrapy.Field(
        input_processor=MapCompose(get_date),
        output_processor=TakeFirst()
    )

    team_name = scrapy.Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )

    team_rating = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    team_position = scrapy.Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )

    team_jersey_number = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    # POSITION STATS
    # SKILLS
    # COMMUNITY INFO

    position = scrapy.Field()

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


    total_stats = scrapy.Field(
        input_processor=MapCompose(convert_currency_format),
        output_processor=TakeFirst()
    )
    hits_comments = scrapy.Field()


class ImageItem(scrapy.Item):
    images = scrapy.Field()
    image_urls = scrapy.Field()
