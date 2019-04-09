# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Identity, Compose
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


def player_id_list(value):

    player_list = list()
    eval_list = list()
    pattern = r'[0-9]+'

    for player in value:
        player_list.append(re.findall(pattern, player))

    for i in range(len(player_list)):
        eval_list.append(eval(player_list[i][0]))

    return eval_list


class SofifaItem(scrapy.Item):

    # GENERAL PLAYER INFORMATION

    id_player_secondary = scrapy.Field(
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

    # GENERAL PLAYER STATS

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

    # CLUB/TEAM INFORMATION

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

    loaned_from = scrapy.Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )

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

    # PLAYER GAME STATS

    overall_rating = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    potential_rating = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    positions = scrapy.Field(
        input_processor=Identity(),
        output_processor=Identity()
    )

    unique_attributes = scrapy.Field(
        input_processor=Identity(),
        output_processor=Identity()
    )

    PAC = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'pointPAC = ([0-9]+)', x)[0], eval),
        output_processor=TakeFirst()
    )

    SHO = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'pointSHO = ([0-9]+)', x)[0], eval),
        output_processor=TakeFirst()
    )

    PAS = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'pointPAS = ([0-9]+)', x)[0], eval),
        output_processor=TakeFirst()
    )

    DRI = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'pointDRI = ([0-9]+)', x)[0], eval),
        output_processor=TakeFirst()
    )

    DEF = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'pointDEF = ([0-9]+)', x)[0], eval),
        output_processor=TakeFirst()
    )

    PHY = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'pointPHY = ([0-9]+)', x)[0], eval),
        output_processor=TakeFirst()
    )

    DIV = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'pointPAC = ([0-9]+)', x)[0], eval),
        output_processor=TakeFirst()
    )

    HAN = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'pointSHO = ([0-9]+)', x)[0], eval),
        output_processor=TakeFirst()
    )

    KIC = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'pointPAS = ([0-9]+)', x)[0], eval),
        output_processor=TakeFirst()
    )

    REF = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'pointDRI = ([0-9]+)', x)[0], eval),
        output_processor=TakeFirst()
    )

    SPD = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'pointDEF = ([0-9]+)', x)[0], eval),
        output_processor=TakeFirst()
    )

    POS = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'pointPHY = ([0-9]+)', x)[0], eval),
        output_processor=TakeFirst()
    )

    # PLAYER DETAILED STATS

    crossing = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    finishing = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    heading_accuracy = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    short_passing = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    volleys = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    aggression = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    interceptions = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    positioning = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    vision = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    penalties = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    composure = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    dribbling = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    curve = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    fk_accuracy = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    long_passing = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    ball_control = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    marking = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    standing_tackle = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    sliding_tackle = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    acceleration = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    sprint_speed = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    agility = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    reactions = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    balance = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    gk_diving = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    gk_handling = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    gk_kicking = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    gk_positioning = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    gk_reflexes = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    shot_power = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    jumping = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    stamina = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    strength = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    long_shots = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    traits = scrapy.Field(
        input_processor=Identity(),
        output_processor=Identity()
    )

    # PLAYER REAL OVERALL RATING (POSITIONAL STATS)

    LS = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'[0-9]+', x), eval),
        output_processor=Identity()
    )

    ST = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'[0-9]+', x), eval),
        output_processor=Identity()
    )

    RS = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'[0-9]+', x), eval),
        output_processor=Identity()
    )

    LW = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'[0-9]+', x), eval),
        output_processor=Identity()
    )

    LF = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'[0-9]+', x), eval),
        output_processor=Identity()
    )

    CF = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'[0-9]+', x), eval),
        output_processor=Identity()
    )

    RF = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'[0-9]+', x), eval),
        output_processor=Identity()
    )

    RW = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'[0-9]+', x), eval),
        output_processor=Identity()
    )

    LAM = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'[0-9]+', x), eval),
        output_processor=Identity()
    )

    CAM = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'[0-9]+', x), eval),
        output_processor=Identity()
    )

    RAM = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'[0-9]+', x), eval),
        output_processor=Identity()
    )

    LM = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'[0-9]+', x), eval),
        output_processor=Identity()
    )

    LCM = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'[0-9]+', x), eval),
        output_processor=Identity()
    )

    CM = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'[0-9]+', x), eval),
        output_processor=Identity()
    )

    RCM = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'[0-9]+', x), eval),
        output_processor=Identity()
    )

    RM = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'[0-9]+', x), eval),
        output_processor=Identity()
    )

    LWB = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'[0-9]+', x), eval),
        output_processor=Identity()
    )

    LDM = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'[0-9]+', x), eval),
        output_processor=Identity()
    )

    CDM = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'[0-9]+', x), eval),
        output_processor=Identity()
    )

    RDM = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'[0-9]+', x), eval),
        output_processor=Identity()
    )

    RWB = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'[0-9]+', x), eval),
        output_processor=Identity()
    )

    LB = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'[0-9]+', x), eval),
        output_processor=Identity()
    )

    LCB = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'[0-9]+', x), eval),
        output_processor=Identity()
    )

    CB = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'[0-9]+', x), eval),
        output_processor=Identity()
    )

    RCB = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'[0-9]+', x), eval),
        output_processor=Identity()
    )

    RB = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'[0-9]+', x), eval),
        output_processor=Identity()
    )

    # COMMUNITY INFO

    followers = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    likes = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    dislikes = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    comments = scrapy.Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )

    # MEDIA

    face_img = scrapy.Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )

    flag_img = scrapy.Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )

    club_logo_img = scrapy.Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )

    team_logo_img = scrapy.Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )


class ImageItem(scrapy.Item):

    images = scrapy.Field()
    image_urls = scrapy.Field()

    id = scrapy.Field(
        input_processor=MapCompose(get_id, eval),
        output_processor=TakeFirst()
    )

    category = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'org/([a-zA-Z]+)', x)[0]),
        output_processor=TakeFirst()
    )

    team_or_club = scrapy.Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )


class MainPageItem(scrapy.Item):

    id_player_main = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'/([0-9]+)/', x), eval),
        output_processor=TakeFirst()
    )

    total_stats = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    hits = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'<?[0-9.K]+', x)[0]),
        output_processor=TakeFirst()
    )

    comments = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'<?[0-9.K]+', x)[1]),
        output_processor=TakeFirst()
    )


class TeamStatItem(scrapy.Item):

    id_club_main = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'/([0-9]+)/', x), eval),
        output_processor=TakeFirst()
    )

    nationality = scrapy.Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )

    region = scrapy.Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )

    num_players = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    hits = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'<?[0-9.K]+', x)[0]),
        output_processor=TakeFirst()
    )

    comments = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'<?[0-9.K]+', x)[1]),
        output_processor=TakeFirst()
    )


class DetailedTeamStatItem(scrapy.Item):

    # GENERAL CLUB INFORMATION

    id_club_secondary = scrapy.Field(
        input_processor=MapCompose(get_id, eval),
        output_processor=TakeFirst()
    )

    club_name = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'^[^\(]+', x), str.strip),
        output_processor=TakeFirst()
    )

    division = scrapy.Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )

    club_logo = scrapy.Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )

    flag = scrapy.Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )

    # GENERAL TEAM STATS

    overall = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    attack = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    midfield = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    defence = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    # DETAILED TEAM STATS

    home_stadium = scrapy.Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )

    rival_team = scrapy.Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )

    international_prestige = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    domestic_prestige = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    transfer_budget = scrapy.Field(
        input_processor=MapCompose(convert_currency_format),
        output_processor=TakeFirst()
    )

    starting_xi_average_age = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    whole_team_average_age = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    captain = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'([0-9]+)', x)[0], eval),
        output_processor=TakeFirst()
    )

    short_free_kick = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'([0-9]+)', x)[0], eval),
        output_processor=TakeFirst()
    )

    long_free_kick = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'([0-9]+)', x)[0], eval),
        output_processor=TakeFirst()
    )

    left_short_free_kick = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'([0-9]+)', x)[0], eval),
        output_processor=TakeFirst()
    )

    right_short_free_kick = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'([0-9]+)', x)[0], eval),
        output_processor=TakeFirst()
    )

    penalties = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'([0-9]+)', x)[0], eval),
        output_processor=TakeFirst()
    )

    left_corner = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'([0-9]+)', x)[0], eval),
        output_processor=TakeFirst()
    )

    right_corner = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'([0-9]+)', x)[0], eval),
        output_processor=TakeFirst()
    )

    starting_xi = scrapy.Field(
        input_processor=Compose(player_id_list),
        output_processor=Identity()
    )

    # TACTICS

    defence_defensive_style = scrapy.Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )

    defence_team_width = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    defence_depth = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    offense_offensive_style = scrapy.Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )

    offense_width = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    offense_players_in_box = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    offense_corners = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    offense_free_kicks = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    # TODO: some values are int, others str. Create a fix for this later.
    build_up_play_speed = scrapy.Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )

    build_up_play_dribbling = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    build_up_play_passing = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    build_up_play_positioning = scrapy.Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )

    chance_creation_passing = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    chance_creation_crossing = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    chance_creation_shooting = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    chance_creation_positioning = scrapy.Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )

    defence_extra_pressure = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    defence_extra_aggression = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    defence_extra_team_width = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    defence_extra_defender_line = scrapy.Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )

    # PLAYERS

    squad = scrapy.Field(
        input_processor=Compose(player_id_list),
        output_processor=Identity()
    )

    on_loan = scrapy.Field(
        input_processor=Compose(player_id_list),
        output_processor=Identity()
    )

    # MEDIA

    kits = scrapy.Field(
        input_processor=Identity(),
        output_processor=Identity()
    )

    # COMMUNITY

    likes = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )

    dislikes = scrapy.Field(
        input_processor=MapCompose(eval),
        output_processor=TakeFirst()
    )


class NationalTeamStats(TeamStatItem):

    id_team_main = scrapy.Field(
        input_processor=MapCompose(lambda x: re.findall(r'/([0-9]+)/', x), eval),
        output_processor=TakeFirst()
    )


class NationalTeamDetailedStats(DetailedTeamStatItem):

    id_team_secondary = scrapy.Field(
        input_processor=MapCompose(get_id, eval),
        output_processor=TakeFirst()
    )

    team_name = scrapy.Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )

    team_logo = scrapy.Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )


class UserAgentScraperItem(scrapy.Item):

    user_agent = scrapy.Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )

    version = scrapy.Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )

    OS = scrapy.Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )

    hardware_type = scrapy.Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )

    popularity = scrapy.Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )
