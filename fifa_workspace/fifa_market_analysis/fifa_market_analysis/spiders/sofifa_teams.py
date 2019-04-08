# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from fifa_market_analysis.items import TeamStatItem, DetailedTeamStatItem, NationalTeamDetailedStats, NationalTeamStats
import logging
from scrapy.utils.log import configure_logging
import datetime


class SofifaClubsSpider(CrawlSpider):

    name = 'sofifa_clubs'

    allowed_domains = ['sofifa.com']
    start_urls = ['https://sofifa.com/teams/club']

    rules = (
        Rule(
            LinkExtractor(
                deny=(
                    [r'\?', r'/[0-9]+', r'/forgot', r'/shortlist', r'/authorize', r'/leagues', r'/squad', r'/help',
                     r'/compare', r'/players', r'/teams']
                )
            ),
            callback='parse_start_url',
            follow=True
        ),
        Rule(
            LinkExtractor(
                deny=(
                    [r'\?', r'/player/', r'/squads', r'/live', r'/formerPlayers', r'/\#comments']
                ),
                restrict_xpaths="//a[contains(@href, '/team/')]"
            ),
            callback='parse_item',
            follow=True
        ),
        # Rule(
        #     LinkExtractor(
        #         restrict_xpaths="//a[text()='Next']"
        #     ), callback='parse_item',
        #     follow=True
        # )
    )

    custom_settings = {
        'MONGO_DB': 'sofifa',
        'DEPTH_LIMIT': 1,
        'HTTPCACHE_ENABLED': True,
        'ITEM_PIPELINES': {
            'fifa_market_analysis.pipelines.MongoDBPipeline': 300,
        },
        'ROBOTSTXT_OBEY': True,
        'COLLECTION_NAME': 'club_stats',
        'SPIDERMON_ENABLED': True,
        'EXTENSIONS': {
            'spidermon.contrib.scrapy.extensions.Spidermon': 500,
        },
        'SPIDERMON_SPIDER_CLOSE_MONITORS': (
            'fifa_market_analysis.monitors.SpiderCloseMonitorSuite',
        ),
        'SPIDERMON_VALIDATION_MODELS': (
            'fifa_market_analysis.validators.ClubItem',
        )
    }

    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename=f'log_{name}_{datetime.date.today()}.txt',
        format='%(levelname)s: %(message)s',
        level=logging.INFO
    )

    def parse_start_url(self, response):

        """
        Parse main page for data that is not available in extracted links.
        """

        for row in response.xpath("//table[@class='table table-hover persist-area']/tbody/tr"):

            loader = ItemLoader(item=TeamStatItem(), selector=row, response=response)

            loader.add_xpath('id_club_main', ".//a[contains(@href, 'team/')]/@href")
            loader.add_xpath('nationality', ".//a[contains(@href, 'teams?na')]/text()")
            loader.add_xpath('region', ".//a[contains(@href, 'teams?ct')]/text()")
            loader.add_xpath('num_players', ".//td[@class='col text-center'][last()]/div/text()")
            loader.add_xpath('hits', ".//div[@class='col-comments text-right text-ellipsis rtl']/text()")
            loader.add_xpath('comments', ".//div[@class='col-comments text-right text-ellipsis rtl']/text()")

            yield loader.load_item()

    def parse_item(self, response):

        loader = ItemLoader(DetailedTeamStatItem(), response=response)

        # GENERAL CLUB INFORMATION

        loader.add_xpath('id_club_secondary', ".//div[@class='info']/h1/text()")
        loader.add_xpath('club_name', ".//div[@class='info']/h1/text()")
        loader.add_xpath('division', ".//div[@class='meta']//a[last()]/text()")
        loader.add_xpath('club_logo', ".//div[@class='card card-border player fixed-width']/img/@data-src")
        loader.add_xpath('flag', ".//div[@class='meta']//a[last()-1]//img/@data-src")

        # GENERAL TEAM STATS

        loader.add_xpath('overall', "(.//div[@class='column col-4 text-center']"
                                    "/preceding::text()[contains(.,'Overall')])[2]/following::span[1]/text()")
        loader.add_xpath('attack', "(.//div[@class='column col-4 text-center']"
                                   "/preceding::text()[contains(.,'Attack')])[2]/following::span[1]/text()")
        loader.add_xpath('midfield', "(.//div[@class='column col-4 text-center']"
                                     "/preceding::text()[contains(.,'Midfield')])[2]/following::span[1]/text()")
        loader.add_xpath('defence', "(.//div[@class='column col-4 text-center']"
                                    "/following::text()[contains(.,'Defence')])[1]/following::span[1]/text()")

        # DETAILED TEAM STATS

        loader.add_xpath('home_stadium', ".//div[@class='column col-6']//following::label[contains(., 'Home Stadium')]"
                                         "/following::text()[1]")
        loader.add_xpath('rival_team', ".//div[@class='column col-6']//following::label[contains(., 'Rival Team')]"
                                       "/following::a[1]/text()")
        loader.add_xpath('international_prestige', ".//div[@class='column col-6']"
                                                   "//following::label[contains(., 'International Prestige')]"
                                                   "/following::span[1]/text()")
        loader.add_xpath('domestic_prestige', ".//div[@class='column col-6']"
                                              "//following::label[contains(., 'Domestic Prestige')]"
                                              "/following::span[1]/text()")
        loader.add_xpath('transfer_budget', ".//div[@class='column col-6']"
                                            "//following::label[contains(., 'Transfer Budget')]"
                                            "/following::text()[1]")
        loader.add_xpath('starting_xi_average_age', ".//div[@class='column col-6']"
                                                    "//following::label[contains(., 'Starting XI Average Age')]"
                                                    "/following::text()[1]")
        loader.add_xpath('whole_team_average_age', ".//div[@class='column col-6']"
                                                   "//following::label[contains(., 'Whole Team Average Age')]"
                                                   "/following::text()[1]")
        loader.add_xpath('captain', ".//div[@class='column col-6']"
                                    "//following::label[contains(., 'Captain')]"
                                    "/following::a[1]/@href")
        loader.add_xpath('short_free_kick', ".//div[@class='column col-6']//following::label[text()='Short Free Kick']"
                                            "/following::a[1]/@href")
        loader.add_xpath('long_free_kick', ".//div[@class='column col-6']//following::label[text()='Long Free Kick']"
                                           "/following::a[1]/@href")
        loader.add_xpath('left_short_free_kick', ".//div[@class='column col-6']"
                                                 "//following::label[text()='Left Short Free Kick']"
                                                 "/following::a[1]/@href")
        loader.add_xpath('right_short_free_kick', ".//div[@class='column col-6']"
                                                  "//following::label[text()='Right Short Free Kick']"
                                                  "/following::a[1]/@href")
        loader.add_xpath('penalties', ".//div[@class='column col-6']//following::label[text()='Penalties']"
                                      "/following::a[1]/@href")
        loader.add_xpath('left_corner', ".//div[@class='column col-6']//following::label[text()='Left Corner']"
                                        "/following::a[1]/@href")
        loader.add_xpath('right_corner', ".//div[@class='column col-6']//following::label[text()='Right Corner']"
                                         "/following::a[1]/@href")
        loader.add_xpath('starting_xi', ".//div[@class='field-player']/a/@href")

        # TACTICS

        loader.add_xpath('defence_defensive_style', ".//dl//span/preceding::dd[text()='Defensive Style']"
                                                    "/span/span/text()")
        loader.add_xpath('defence_team_width', "(.//dl//span/preceding::span[text()='Team Width']"
                                               "/following::div/meter)[1]/@value")
        loader.add_xpath('defence_depth', "(.//dl//span/preceding::span[text()='Depth']"
                                          "/following::div/meter)[1]/@value")
        loader.add_xpath('offense_offensive_style', ".//dl//span/preceding::dd[text()='Offensive Style']"
                                                    "/span/span/text()")
        loader.add_xpath('offense_width', "(.//dl//span/preceding::span[text()='Width']/following::div/meter)[1]"
                                          "/@value")
        loader.add_xpath('offense_players_in_box', "(.//dl//span/preceding::span[text()='Players in box']"
                                                   "/following::div/meter)[1]/@value")
        loader.add_xpath('offense_corners', "(.//dl//span/preceding::span[text()='Corners']"
                                            "/following::div/meter)[1]/@value")
        loader.add_xpath('offense_free_kicks', "(.//dl//span/preceding::span[text()='Free Kicks']"
                                               "/following::div/meter)[1]/@value")
        loader.add_xpath('build_up_play_speed', ".//dl//span/preceding::span[text()='Speed']/following::span/text()")
        loader.add_xpath('build_up_play_dribbling', "(.//dl//span/preceding::dd[text()='Dribbling']//span)[1]"
                                                    "/span/text()")
        loader.add_xpath('build_up_play_passing', "(.//dl//span/preceding::span[text()='Passing']/following::span)[1]"
                                                  "/span/text()")
        loader.add_xpath('build_up_play_positioning', "(.//dl//span/preceding::span[text()='Positioning'])[1]"
                                                      "/following::span[1]/text()")
        loader.add_xpath('chance_creation_passing', "(.//dl//span/preceding::span[text()='Shooting']"
                                                    "/following::span)[1]/span/text()")
        loader.add_xpath('chance_creation_crossing', "(.//dl//span/preceding::span[text()='Crossing']"
                                                     "/following::span)[1]/span/text()")
        loader.add_xpath('chance_creation_shooting', "(.//dl//span/preceding::span[text()='Shooting']"
                                                     "/following::span)[1]/span/text()")
        loader.add_xpath('chance_creation_positioning', "(.//dl//span/preceding::span[text()='Positioning'])[2]"
                                                        "/following::span[1]/text()")
        loader.add_xpath('defence_extra_pressure', "(.//dl//span/preceding::span[text()='Pressure']"
                                                   "/following::span)[1]/span/text()")
        loader.add_xpath('defence_extra_aggression', "(.//dl//span/preceding::span[text()='Aggression']"
                                                     "/following::span)[1]/span/text()")
        loader.add_xpath('defence_extra_team_width', "(.//span[text()='Team Width'])[2]/following::span[1]/span/text()")
        loader.add_xpath('defence_extra_defender_line', ".//span[text()='Defender Line']/following::span/text()")

        # PLAYERS

        loader.add_xpath('squad', "(.//table)[1]/tbody/tr//a[contains(@href, '/player/')]/@href")
        loader.add_xpath('on_loan', "(.//table)[2]/tbody/tr//a[contains(@href, '/player/')]/@href")

        # MEDIA

        loader.add_xpath('kits', ".//div[@class='column col-sm-5 text-center']//img/@src")

        # COMMUNITY

        loader.add_xpath('likes', ".//div[@class='operation mt-2']/a/text()[contains(.,'Like')]"
                                  "/following::span[1]/text()")
        loader.add_xpath('dislikes', ".//div[@class='operation mt-2']/a/text()[contains(.,'Dislike')]"
                                     "/following::span[1]/text()")

        yield loader.load_item()


class SofifaTeamsSpider(SofifaClubsSpider):

    name = 'sofifa_teams'

    start_urls = ['https://sofifa.com/teams/national']

    custom_settings = {
        'MONGO_DB': 'sofifa',
        'DEPTH_LIMIT': 1,
        'HTTPCACHE_ENABLED': True,
        'ITEM_PIPELINES': {
            'fifa_market_analysis.pipelines.MongoDBPipeline': 300,
        },
        'ROBOTSTXT_OBEY': True,
        'COLLECTION_NAME': 'team_stats',
        'SPIDERMON_ENABLED': True,
        'EXTENSIONS': {
            'spidermon.contrib.scrapy.extensions.Spidermon': 500,
        },
        'SPIDERMON_SPIDER_CLOSE_MONITORS': (
            'fifa_market_analysis.monitors.SpiderCloseMonitorSuite',
        ),
        'SPIDERMON_VALIDATION_MODELS': (
            'fifa_market_analysis.validators.TeamItem',
        )
    }

    def parse_start_url(self, response):

        """
        Parse main page for data that is not available in extracted links.
        """

        for row in response.xpath("//table[@class='table table-hover persist-area']/tbody/tr"):

            loader = ItemLoader(item=NationalTeamStats(), selector=row, response=response)

            loader.add_xpath('id_team_main', ".//a[contains(@href, 'team/')]/@href")
            loader.add_xpath('nationality', ".//a[contains(@href, 'teams?na')]/text()")
            loader.add_xpath('region', ".//a[contains(@href, 'teams?ct')]/text()")
            loader.add_xpath('num_players', ".//td[@class='col text-center'][last()]/div/text()")
            loader.add_xpath('hits', ".//div[@class='col-comments text-right text-ellipsis rtl']/text()")
            loader.add_xpath('comments', ".//div[@class='col-comments text-right text-ellipsis rtl']/text()")

            yield loader.load_item()

    def parse_item(self, response):

        loader = ItemLoader(NationalTeamDetailedStats(), response=response)

        # GENERAL CLUB INFORMATION

        loader.add_xpath('id_team_secondary', ".//div[@class='info']/h1/text()")
        loader.add_xpath('team_name', ".//div[@class='info']/h1/text()")
        loader.add_xpath('team_logo', ".//div[@class='card card-border player fixed-width']/img/@data-src")
        loader.add_xpath('flag', ".//div[@class='meta']//a[last()-1]//img/@data-src")

        # GENERAL TEAM STATS

        loader.add_xpath('overall', "(.//div[@class='column col-4 text-center']"
                                    "/preceding::text()[contains(.,'Overall')])[2]/following::span[1]/text()")
        loader.add_xpath('attack', "(.//div[@class='column col-4 text-center']"
                                   "/preceding::text()[contains(.,'Attack')])[2]/following::span[1]/text()")
        loader.add_xpath('midfield', "(.//div[@class='column col-4 text-center']"
                                     "/preceding::text()[contains(.,'Midfield')])[2]/following::span[1]/text()")
        loader.add_xpath('defence', "(.//div[@class='column col-4 text-center']"
                                    "/following::text()[contains(.,'Defence')])[1]/following::span[1]/text()")

        # DETAILED TEAM STATS

        loader.add_xpath('home_stadium', ".//div[@class='column col-6']//following::label[contains(., 'Home Stadium')]"
                                         "/following::text()[1]")
        loader.add_xpath('rival_team', ".//div[@class='column col-6']//following::label[contains(., 'Rival Team')]"
                                       "/following::a[1]/text()")
        loader.add_xpath('international_prestige', ".//div[@class='column col-6']"
                                                   "//following::label[contains(., 'International Prestige')]"
                                                   "/following::span[1]/text()")
        loader.add_xpath('starting_xi_average_age', ".//div[@class='column col-6']"
                                                    "//following::label[contains(., 'Starting XI Average Age')]"
                                                    "/following::text()[1]")
        loader.add_xpath('whole_team_average_age', ".//div[@class='column col-6']"
                                                   "//following::label[contains(., 'Whole Team Average Age')]"
                                                   "/following::text()[1]")
        loader.add_xpath('captain', ".//div[@class='column col-6']"
                                    "//following::label[contains(., 'Captain')]"
                                    "/following::a[1]/@href")
        loader.add_xpath('short_free_kick', ".//div[@class='column col-6']//following::label[text()='Short Free Kick']"
                                            "/following::a[1]/@href")
        loader.add_xpath('long_free_kick', ".//div[@class='column col-6']//following::label[text()='Long Free Kick']"
                                           "/following::a[1]/@href")
        loader.add_xpath('left_short_free_kick', ".//div[@class='column col-6']"
                                                 "//following::label[text()='Left Short Free Kick']"
                                                 "/following::a[1]/@href")
        loader.add_xpath('right_short_free_kick', ".//div[@class='column col-6']"
                                                  "//following::label[text()='Right Short Free Kick']"
                                                  "/following::a[1]/@href")
        loader.add_xpath('penalties', ".//div[@class='column col-6']//following::label[text()='Penalties']"
                                      "/following::a[1]/@href")
        loader.add_xpath('left_corner', ".//div[@class='column col-6']//following::label[text()='Left Corner']"
                                        "/following::a[1]/@href")
        loader.add_xpath('right_corner', ".//div[@class='column col-6']//following::label[text()='Right Corner']"
                                         "/following::a[1]/@href")
        loader.add_xpath('starting_xi', ".//div[@class='field-player']/a/@href")

        # TACTICS

        loader.add_xpath('defence_defensive_style', ".//dl//span/preceding::dd[text()='Defensive Style']"
                                                    "/span/span/text()")
        loader.add_xpath('defence_team_width', "(.//dl//span/preceding::span[text()='Team Width']"
                                               "/following::div/meter)[1]/@value")
        loader.add_xpath('defence_depth', "(.//dl//span/preceding::span[text()='Depth']"
                                          "/following::div/meter)[1]/@value")
        loader.add_xpath('offense_offensive_style', ".//dl//span/preceding::dd[text()='Offensive Style']"
                                                    "/span/span/text()")
        loader.add_xpath('offense_width', "(.//dl//span/preceding::span[text()='Width']/following::div/meter)[1]"
                                          "/@value")
        loader.add_xpath('offense_players_in_box', "(.//dl//span/preceding::span[text()='Players in box']"
                                                   "/following::div/meter)[1]/@value")
        loader.add_xpath('offense_corners', "(.//dl//span/preceding::span[text()='Corners']"
                                            "/following::div/meter)[1]/@value")
        loader.add_xpath('offense_free_kicks', "(.//dl//span/preceding::span[text()='Free Kicks']"
                                               "/following::div/meter)[1]/@value")
        loader.add_xpath('build_up_play_speed', ".//dl//span/preceding::span[text()='Speed']/following::span/text()")
        loader.add_xpath('build_up_play_dribbling', "(.//dl//span/preceding::dd[text()='Dribbling']//span)[1]"
                                                    "/span/text()")
        loader.add_xpath('build_up_play_passing', "(.//dl//span/preceding::span[text()='Passing']/following::span)[1]"
                                                  "/span/text()")
        loader.add_xpath('build_up_play_positioning', "(.//dl//span/preceding::span[text()='Positioning'])[1]"
                                                      "/following::span[1]/text()")
        loader.add_xpath('chance_creation_passing', "(.//dl//span/preceding::span[text()='Shooting']"
                                                    "/following::span)[1]/span/text()")
        loader.add_xpath('chance_creation_crossing', "(.//dl//span/preceding::span[text()='Crossing']"
                                                     "/following::span)[1]/span/text()")
        loader.add_xpath('chance_creation_shooting', "(.//dl//span/preceding::span[text()='Shooting']"
                                                     "/following::span)[1]/span/text()")
        loader.add_xpath('chance_creation_positioning', "(.//dl//span/preceding::span[text()='Positioning'])[2]"
                                                        "/following::span[1]/text()")
        loader.add_xpath('defence_extra_pressure', "(.//dl//span/preceding::span[text()='Pressure']"
                                                   "/following::span)[1]/span/text()")
        loader.add_xpath('defence_extra_aggression', "(.//dl//span/preceding::span[text()='Aggression']"
                                                     "/following::span)[1]/span/text()")
        loader.add_xpath('defence_extra_team_width', "(.//span[text()='Team Width'])[2]/following::span[1]/span/text()")
        loader.add_xpath('defence_extra_defender_line', ".//span[text()='Defender Line']/following::span/text()")

        # PLAYERS

        loader.add_xpath('squad', "(.//table)[1]/tbody/tr//a[contains(@href, '/player/')]/@href")
        loader.add_xpath('on_loan', "(.//table)[2]/tbody/tr//a[contains(@href, '/player/')]/@href")

        # MEDIA

        loader.add_xpath('kits', ".//div[@class='column col-sm-5 text-center']//img/@src")

        # COMMUNITY

        loader.add_xpath('likes', ".//div[@class='operation mt-2']/a/text()[contains(.,'Like')]"
                                  "/following::span[1]/text()")
        loader.add_xpath('dislikes', ".//div[@class='operation mt-2']/a/text()[contains(.,'Dislike')]"
                                     "/following::span[1]/text()")

        yield loader.load_item()
