# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from fifa_market_analysis.items import SofifaItem, MainPageItem
from urllib.parse import urljoin
from pymongo import MongoClient
from fifa_market_analysis.proxy_generator import proxies
from fifa_market_analysis.user_agent_generator import user_agent
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from fifa_market_analysis.items import TeamStatItem, DetailedTeamStatItem, NationalTeamDetailedStats, NationalTeamStats
import logging
from scrapy.utils.log import configure_logging
import datetime


class SofifaTeamPagesSpider(scrapy.Spider):

    name = 'team_details'
    allowed_domains = ['sofifa.com']

    custom_settings = {
        'MONGO_DB': 'sofifa',
        'HTTPCACHE_ENABLED': False,
        'ITEM_PIPELINES': {
            'fifa_market_analysis.pipelines.MongoDBPipeline': 300,
        },
        'ROBOTSTXT_OBEY': True,
        'COLLECTION_NAME': 'team_details',
        'PROXY_POOL_ENABLED': True,
        'ROTATING_PROXY_LIST': proxies,
        'USER_AGENTS': user_agent,
        'DOWNLOAD_TIMEOUT': 30,
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
            'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
            'rotating_proxies.middlewares.BanDetectionMiddleware': 620
        }
    }

    def start_requests(self):

        client = MongoClient('localhost', 27017)
        db = client.sofifa
        collection = db.team_urls

        urls = [f'{urljoin("https://sofifa.com", x["team_page"])}' for x in
                collection.find({'team_page': {'$exists': 'true'}})]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        loader = ItemLoader(NationalTeamDetailedStats(), response=response)
        mt_2_loader = loader.nested_xpath(".//div[@class='operation mt-2']/a")
        col_6_loader = loader.nested_xpath(".//div[@class='column col-6']")

        # GENERAL CLUB INFORMATION

        loader.add_xpath('id', ".//div[@class='info']/h1/text()")
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

        col_6_loader.add_xpath('home_stadium', ".//following::label[contains(., 'Home Stadium')]/following::text()[1]")
        col_6_loader.add_xpath('rival_team', ".//following::label[contains(., 'Rival Team')]/following::a[1]/text()")
        col_6_loader.add_xpath('international_prestige', ".//following::label[contains(., 'International Prestige')]"
                                                         "/following::span[1]/text()")
        col_6_loader.add_xpath('starting_xi_average_age', ".//following::label[contains(., 'Starting XI Average Age')]"
                                                          "/following::text()[1]")
        col_6_loader.add_xpath('whole_team_average_age', ".//following::label[contains(., 'Whole Team Average Age')]"
                                                         "/following::text()[1]")
        col_6_loader.add_xpath('captain', ".//following::label[contains(., 'Captain')]/following::a[1]/@href")
        col_6_loader.add_xpath('short_free_kick', ".//following::label[text()='Short Free Kick']/following::a[1]/@href")
        col_6_loader.add_xpath('long_free_kick', ".//following::label[text()='Long Free Kick']/following::a[1]/@href")
        col_6_loader.add_xpath('left_short_free_kick', ".//following::label[text()='Left Short Free Kick']"
                                                       "/following::a[1]/@href")
        col_6_loader.add_xpath('right_short_free_kick', ".//following::label[text()='Right Short Free Kick']"
                                                        "/following::a[1]/@href")
        col_6_loader.add_xpath('penalties', ".//following::label[text()='Penalties']/following::a[1]/@href")
        col_6_loader.add_xpath('left_corner', ".//following::label[text()='Left Corner']/following::a[1]/@href")
        col_6_loader.add_xpath('right_corner', ".//following::label[text()='Right Corner']/following::a[1]/@href")
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

        mt_2_loader.add_xpath('likes', "text()[contains(.,'Like')]/following::span[1]/text()")
        mt_2_loader.add_xpath('dislikes', "text()[contains(.,'Dislike')]/following::span[1]/text()")

        print(response.request.headers['User-Agent'])
        self.logger.info(f'Parse function called on {response.url}')

        yield loader.load_item()
