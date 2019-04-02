# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from fifa_market_analysis.items import SofifaItem


class SofifaDetailedSpider(CrawlSpider):

    name = 'sofifa_detailed'

    allowed_domains = ['sofifa.com']
    start_urls = ['http://sofifa.com/players/']

    rules = (
        Rule(LinkExtractor(deny=([r'\?', r'[0-9]+/[0-9]+/', r'/changeLog', r'/live', r'/squads', r'/calculator/']),
                           restrict_xpaths="//a[contains(@href, 'player/')]"), callback='parse_item', follow=True),
        # Rule(LinkExtractor(restrict_xpaths="//a[text()='Next']"), callback='parse_item', follow=True)
    )

    def parse_item(self, response):

        loader = ItemLoader(item=SofifaItem(), response=response)

        # GENERAL PLAYER INFORMATION

        loader.add_xpath('id', ".//div[@class='info']/h1/text()")
        loader.add_xpath('name', ".//div[@class='info']/h1/text()")
        loader.add_xpath('full_name', ".//div[@class='meta']/text()")
        loader.add_xpath('age', ".//div[@class='meta']/text()/following-sibling::text()[last()]")
        loader.add_xpath('dob', ".//div[@class='meta']/text()/following-sibling::text()[last()]")
        loader.add_xpath('height', ".//div[@class='meta']/text()/following-sibling::text()[last()]")
        loader.add_xpath('weight', ".//div[@class='meta']/text()/following-sibling::text()[last()]")
        loader.add_xpath('nationality', ".//div[@class='meta']/a/@title")

        # GENERAL PLAYER STATS

        loader.add_xpath('preferred_foot', "(.//label[text()='Preferred Foot']/following::text())[1]")
        loader.add_xpath('international_reputation',
                         "(.//label[text()='International Reputation']/following::text())[1]")
        loader.add_xpath('weak_foot', "(.//label[text()='Weak Foot']/following::text())[1]")
        loader.add_xpath('skill_moves', "(.//label[text()='Skill Moves']/following::text())[1]")
        loader.add_xpath('work_rate', "(.//label[text()='Work Rate']/following::span/text())[1]")
        loader.add_xpath('body_type', "(.//label[text()='Body Type']/following::span/text())[1]")
        loader.add_xpath('real_face', "(.//label[text()='Real Face']/following::span/text())[1]")

        # CLUB/TEAM INFORMATION

        loader.add_xpath('value',
                         ".//div[@class='column col-4 text-center']"
                         "/following::text()[contains(., 'Value')]/following::span[1]/text()")
        loader.add_xpath('wage',
                         ".//div[@class='column col-4 text-center']"
                         "/following::text()[contains(., 'Wage')]/following::span[1]/text()")
        loader.add_xpath('release_clause', "(.//label[text()='Release Clause']/following::span/text())[1]")
        loader.add_xpath('club_name', "(.//ul[@class='pl']//a/text())[1]")
        loader.add_xpath('club_rating', ".//div[@class='column col-4'][3]/ul/li[2]/span/text()")
        loader.add_xpath('club_position', ".//div[@class='column col-4'][3]/ul/li[3]/span/text()")
        loader.add_xpath('club_jersey_number',
                         "(.//div[@class='column col-4'][3]/ul/li[4]/label/following::text())[1]")
        loader.add_xpath('club_join_date',
                         "(.//div[@class='column col-4'][3]/ul/li[5]/label/following::text())[1]")
        loader.add_xpath('club_contract_end_date',
                         "(.//div[@class='column col-4'][3]/ul/li[6]/label/following::text())[1]")
        loader.add_xpath('team_name', "(.//ul[@class='pl']//a/text())[2]")
        loader.add_xpath('team_rating', ".//div[@class='column col-4'][4]/ul/li[2]/span/text()")
        loader.add_xpath('team_position', ".//div[@class='column col-4'][4]/ul/li[3]/span/text()")
        loader.add_xpath('team_jersey_number',
                         "(.//div[@class='column col-4'][4]/ul/li[4]/label/following::text())[1]")

        # PLAYER GAME STATS

        loader.add_xpath('overall_rating',
                         "(.//div[@class='column col-4 text-center']"
                         "/preceding::text()[contains(.,'Overall Rating')])[2]/following::span[1]/text()")
        loader.add_xpath('potential_rating',
                         ".//div[@class='column col-4 text-center']"
                         "/following::text()[contains(., 'Potential')]/following::span[1]/text()")
        loader.add_xpath('positions', ".//div[@class='meta']/span/text()")
        loader.add_xpath('unique_attributes', ".//div[@class='mt-2']/a/text()")
        loader.add_xpath('pace', ".//div[@class='wrapper']//script[contains(text(), 'var overallRating')]/text()")
        loader.add_xpath('shooting', ".//div[@class='wrapper']//script[contains(text(), 'var overallRating')]/text()")
        loader.add_xpath('passing', ".//div[@class='wrapper']//script[contains(text(), 'var overallRating')]/text()")
        loader.add_xpath('dribbling', ".//div[@class='wrapper']//script[contains(text(), 'var overallRating')]/text()")
        loader.add_xpath('defense', ".//div[@class='wrapper']//script[contains(text(), 'var overallRating')]/text()")
        loader.add_xpath('physical', ".//div[@class='wrapper']//script[contains(text(), 'var overallRating')]/text()")

        # if 'GK' in loader.add_xpath('positions', ".//div[@class='meta']/span/text()"):
        #
        #     loader.add_xpath('diving',
        #                      ".//div[@class='wrapper']//script[contains(text(), 'var overallRating')]/text()")
        #     loader.add_xpath('handling',
        #                      ".//div[@class='wrapper']//script[contains(text(), 'var overallRating')]/text()")
        #     loader.add_xpath('kicking',
        #                      ".//div[@class='wrapper']//script[contains(text(), 'var overallRating')]/text()")
        #     loader.add_xpath('reflexes',
        #                      ".//div[@class='wrapper']//script[contains(text(), 'var overallRating')]/text()")
        #     loader.add_xpath('speed',
        #                      ".//div[@class='wrapper']//script[contains(text(), 'var overallRating')]/text()")
        #     loader.add_xpath('positioning',
        #                      ".//div[@class='wrapper']//script[contains(text(), 'var overallRating')]/text()")
        #
        # else:
        #
        #     loader.add_xpath('pace',
        #                      ".//div[@class='wrapper']//script[contains(text(), 'var overallRating')]/text()")
        #     loader.add_xpath('shooting',
        #                      ".//div[@class='wrapper']//script[contains(text(), 'var overallRating')]/text()")
        #     loader.add_xpath('passing',
        #                      ".//div[@class='wrapper']//script[contains(text(), 'var overallRating')]/text()")
        #     loader.add_xpath('dribbling',
        #                      ".//div[@class='wrapper']//script[contains(text(), 'var overallRating')]/text()")
        #     loader.add_xpath('defense',
        #                      ".//div[@class='wrapper']//script[contains(text(), 'var overallRating')]/text()")
        #     loader.add_xpath('physical',
        #                      ".//div[@class='wrapper']//script[contains(text(), 'var overallRating')]/text()")

        # PLAYER DETAILED STATS

        # loader.add_xpath('crossing', "")
        # loader.add_xpath('finishing', "")
        # loader.add_xpath('heading_accuracy', "")
        # loader.add_xpath('short_passing', "")
        # loader.add_xpath('volleys', "")
        # loader.add_xpath('aggression', "")
        # loader.add_xpath('interceptions', "")
        # loader.add_xpath('positioning', "")
        # loader.add_xpath('vision', "")
        # loader.add_xpath('penalties', "")
        # loader.add_xpath('composure', "")
        # loader.add_xpath('dribbling', "")
        # loader.add_xpath('curve', "")
        # loader.add_xpath('fk_accuracy', "")
        # loader.add_xpath('long_passing', "")
        # loader.add_xpath('ball_control', "")
        # loader.add_xpath('marking', "")
        # loader.add_xpath('standing_tackle', "")
        # loader.add_xpath('sliding_tackle', "")
        # loader.add_xpath('acceleration', "")
        # loader.add_xpath('sprint_speed', "")
        # loader.add_xpath('agility', "")
        # loader.add_xpath('reactions', "")
        # loader.add_xpath('balance', "")
        # loader.add_xpath('gk_diving', "")
        # loader.add_xpath('gk_handling', "")
        # loader.add_xpath('gk_kicking', "")
        # loader.add_xpath('gk_positioning', "")
        # loader.add_xpath('gk_reflexes', "")
        # loader.add_xpath('shot_power', "")
        # loader.add_xpath('jumping', "")
        # loader.add_xpath('stamina', "")
        # loader.add_xpath('strength', "")
        # loader.add_xpath('long_shots', "")
        # loader.add_xpath('traits', "")
        #
        #
        # loader.add_xpath('', "")

        yield loader.load_item()

        # yield {
        #     'flag_img':
        #         response.xpath(".//div[@class='meta']/a/img/@data-src").get(),
        #     'player_img':
        #         response.xpath(".//div/div/article/div/img//@data-src").get(),
        #     'club_logo_img':
        #         response.xpath(".//div/ul/li/figure/img/@data-src").getall()[0],
        #     'national_team_logo_img':
        #         response.xpath(".//div/ul/li/figure/img/@data-src").getall()[-1],
        #     'followers':
        #         response.xpath(".//div[@class='operation mt-2']/a/span/text()").getall()[0],
        #     'likes':
        #         response.xpath(".//div[@class='operation mt-2']/a/span/text()").getall()[1],
        #     'dislikes':
        #         response.xpath(".//div[@class='operation mt-2']/a/span/text()").getall()[2],
        #     'crossing':
        #         response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Crossing']/text()").get(),
        #     'finishing':
        #         response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Finishing']/text()").get(),
        #     'heading_accuracy':
        #         response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Heading Accuracy']"
        #                        "/text()").get(),
        #     'short_passing':
        #         response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Short Passing']"
        #                        "/text()").get(),
        #     'volleys':
        #         response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Volleys']/text()").get(),
        #     'aggression':
        #         response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Aggression']/text()").get(),
        #     'interceptions':
        #         response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Interceptions']"
        #                        "/text()").get(),
        #     'positioning':
        #         response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Positioning']/text()").get(),
        #     'vision':
        #         response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Vision']/text()").get(),
        #     'penalties':
        #         response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Penalties']/text()").get(),
        #     'composure':
        #         response.xpath(".//div[@class='column col-4']/div/ul/li[contains(text(), 'Composure')]/span"
        #                        "/text()").get(),
        #     'dribbling':
        #         response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Dribbling']/text()").get(),
        #     'curve':
        #         response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Curve']/text()").get(),
        #     'fk_accuracy':
        #         response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='FK Accuracy']/text()").get(),
        #     'long_passing':
        #         response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Long Passing']/text()").get(),
        #     'ball_control':
        #         response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Ball Control']/text()").get(),
        #     'marking':
        #         response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Marking']/text()").get(),
        #     'standing_tackle':
        #         response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Standing Tackle']"
        #                        "/text()").get(),
        #     'sliding_tackle':
        #         response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Sliding Tackle']"
        #                        "/text()").get(),
        #     'acceleration':
        #         response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Acceleration']/text()").get(),
        #     'sprint_speed':
        #         response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Sprint Speed']/text()").get(),
        #     'agility':
        #         response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Agility']/text()").get(),
        #     'reactions':
        #         response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Reactions']/text()").get(),
        #     'balance':
        #         response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Balance']/text()").get(),
        #     'gk_diving':
        #         response.xpath(".//div[@class='column col-4']/div/ul/li[contains(text(), 'GK Diving')]/span"
        #                        "/text()").get(),
        #     'gk_handling':
        #         response.xpath(".//div[@class='column col-4']/div/ul/li[contains(text(), 'GK Handling')]/span"
        #                        "/text()").get(),
        #     'gk_kicking':
        #         response.xpath(".//div[@class='column col-4']/div/ul/li[contains(text(), 'GK Kicking')]/span"
        #                        "/text()").get(),
        #     'gk_positioning':
        #         response.xpath(".//div[@class='column col-4']/div/ul/li[contains(text(), 'GK Positioning')]/span"
        #                        "/text()").get(),
        #     'gk_reflexes':
        #         response.xpath(".//div[@class='column col-4']/div/ul/li[contains(text(), 'GK Reflexes')]/span"
        #                        "/text()").get(),
        #     'shot_power':
        #         response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Shot Power']/text()").get(),
        #     'jumping':
        #         response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Jumping']/text()").get(),
        #     'stamina':
        #         response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Stamina']/text()").get(),
        #     'strength':
        #         response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Strength']/text()").get(),
        #     'long_shots':
        #         response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Long Shots']/text()").get(),
        #     'traits':
        #         response.xpath(".//div[@class='column col-4']/div/h5[text()='Traits']/following-sibling::ul/li/span"
        #                        "/text()").getall(),
        #     'LS':
        #         response.xpath(".//div[../div='LS']/following::text()").get(),
        #     'ST':
        #         response.xpath(".//div[../div='ST']/following::text()").get(),
        #     'RS':
        #         response.xpath(".//div[../div='RS']/following::text()").get(),
        #     'LW':
        #         response.xpath(".//div[../div='LW']/following::text()").get(),
        #     'LF':
        #         response.xpath(".//div[../div='LF']/following::text()").get(),
        #     'CF':
        #         response.xpath(".//div[../div='CF']/following::text()").get(),
        #     'RF':
        #         response.xpath(".//div[../div='RF']/following::text()").get(),
        #     'RW':
        #         response.xpath(".//div[../div='RW']/following::text()").get(),
        #     'LAM':
        #         response.xpath(".//div[../div='LAM']/following::text()").get(),
        #     'CAM':
        #         response.xpath(".//div[../div='CAM']/following::text()").get(),
        #     'RAM':
        #         response.xpath(".//div[../div='RAM']/following::text()").get(),
        #     'LM':
        #         response.xpath(".//div[../div='LM']/following::text()").get(),
        #     'LCM':
        #         response.xpath(".//div[../div='LCM']/following::text()").get(),
        #     'CM':
        #         response.xpath(".//div[../div='CM']/following::text()").get(),
        #     'RCM':
        #         response.xpath(".//div[../div='RCM']/following::text()").get(),
        #     'RM':
        #         response.xpath(".//div[../div='RM']/following::text()").get(),
        #     'LWB':
        #         response.xpath(".//div[../div='LWB']/following::text()").get(),
        #     'LDM':
        #         response.xpath(".//div[../div='LDM']/following::text()").get(),
        #     'CDM':
        #         response.xpath(".//div[../div='CDM']/following::text()").get(),
        #     'RDM':
        #         response.xpath(".//div[../div='RDM']/following::text()").get(),
        #     'RWB':
        #         response.xpath(".//div[../div='RWB']/following::text()").get(),
        #     'LB':
        #         response.xpath(".//div[../div='LB']/following::text()").get(),
        #     'LCB':
        #         response.xpath(".//div[../div='LCB']/following::text()").get(),
        #     'CB':
        #         response.xpath(".//div[../div='CB']/following::text()").get(),
        #     'RCB':
        #         response.xpath(".//div[../div='RCB']/following::text()").get(),
        #     'RB':
        #         response.xpath(".//div[../div='RB']/following::text()").get(),
        #     'user-agent':
        #         response.request.headers.get('User-Agent').decode('utf-8')
        # }


# 'rankings_history': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
# 'total_comments': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
# 'total_recommended': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
# 'hits_comments': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
# 'total_stats': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
# 'similar_players':
# response.xpath(".//div[@id='similar']/table/tbody/tr/td[2]/a/@title").getall()
