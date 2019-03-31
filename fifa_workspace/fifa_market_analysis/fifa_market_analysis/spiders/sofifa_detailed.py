# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


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

        for stat in response.xpath("//div[@class='teams']/div[@class='columns']/div[@class='column col-4'][1]/ul"):
            yield {
                'id':
                    response.xpath("//div[@class='info']/h1/text()").re(r'ID:\ |[0-9]+')[-1],
                'name_id':
                    response.xpath("//div[@class='info']/h1/text()").get(),
                'preferred_foot':
                    stat.xpath(".//li/label[text()='Preferred Foot']/following::text()").get(),
                'international_reputation':
                    stat.xpath(".//li/label[text()='International Reputation']/following::text()").get(),
                'weak_foot':
                    stat.xpath(".//li/label[text()='Weak Foot']/following::text()").get(),
                'skill_moves':
                    stat.xpath(".//li/label[text()='Skill Moves']/following::text()").get(),
                'work_rate':
                    stat.xpath(".//li/label[text()='Work Rate']/following::span/text()").get(),
                'body_type':
                    stat.xpath(".//li/label[text()='Body Type']/text()/following::span/text()").get(),
                'real_face':
                    stat.xpath(".//li/label[text()='Real Face']/text()/following::span/text()").get(),
                'release_clause':
                    stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").get(),
                'full_name':
                    response.xpath(".//div[@class='info']/div[@class='meta']/text()").get(),
                'flag_img':
                    response.xpath(".//div[@class='meta']/a/img/@data-src").get(),
                'player_img':
                    response.xpath(".//div/div/article/div/img//@data-src").get(),
                'club_logo_img':
                    response.xpath(".//div/ul/li/figure/img/@data-src").getall()[0],
                'national_team_logo_img':
                    response.xpath(".//div/ul/li/figure/img/@data-src").getall()[-1],
                'positions':
                    response.xpath(".//div[@class='meta']/span/text()").getall(),
                'age':
                    response.xpath(".//div[@class='meta']/text()").re(r'Age\ [0-9]+')[0],
                'dob':
                    response.xpath(".//div[@class='meta']/text()").re(r'[a-zA-Z]+\ [0-9]+,\ [0-9]+')[0],
                'height':
                    response.xpath(".//div[@class='meta']/text()").re(r'[0-9]+\W[0-9]+\W')[0],
                'weight':
                    response.xpath(".//div[@class='meta']/text()").re(r'[0-9]+lbs')[0],
                'overall_rating':
                    response.xpath(".//div[@class='column col-4 text-center']/span/text()").getall()[0],
                'potential':
                    response.xpath(".//div[@class='column col-4 text-center']/span/text()").getall()[1],
                'value':
                    response.xpath(".//div[@class='column col-4 text-center']/span/text()").getall()[2],
                'wage':
                    response.xpath(".//div[@class='column col-4 text-center']/span/text()").getall()[3],
                'club_name':
                    response.xpath(".//ul[@class='pl']/li/a/text()").getall()[0],
                'national_team':
                    response.xpath(".//ul[@class='pl']/li/a/text()").getall()[-1],
                'club_rating':
                    response.xpath(".//div[@class='teams']/div[@class='columns']/div[@class='column col-4'][3]"
                                   "/ul/li[2]/span/text()").get(),
                'national_team_rating':
                    response.xpath(".//div[@class='teams']/div[@class='columns']/div[@class='column col-4'][4]"
                                   "/ul/li[2]/span/text()").get(),
                'club_position':
                    response.xpath(".//div[@class='teams']/div[@class='columns']/div[@class='column col-4'][3]"
                                   "/ul/li[3]/span/text()").get(),
                'national_team_position':
                    response.xpath(".//div[@class='teams']/div[@class='columns']/div[@class='column col-4'][4]"
                                   "/ul/li[3]/span/text()").get(),
                'club_jersey_no':
                    response.xpath(".//div[@class='teams']/div[@class='columns']/div[@class='column col-4'][3]"
                                   "/ul/li[4]/label/following::text()").get(),
                'national_team_jersey_no':
                    response.xpath(".//div[@class='teams']/div[@class='columns']/div[@class='column col-4'][4]"
                                   "/ul/li[4]/label/following::text()").get(),
                'club_join_date':
                    response.xpath(".//div[@class='teams']/div[@class='columns']/div[@class='column col-4'][3]"
                                   "/ul/li[5]/label/following::text()").get(),
                'club_contract_valid_until':
                    response.xpath(".//div[@class='teams']/div[@class='columns']/div[@class='column col-4'][3]"
                                   "/ul/li[6]/label/following::text()").get(),
                'unique_attributes_tags':
                    response.xpath(".//div[@class='mt-2']/a/text()").getall(),
                'followers':
                    response.xpath(".//div[@class='operation mt-2']/a/span/text()").getall()[0],
                'likes':
                    response.xpath(".//div[@class='operation mt-2']/a/span/text()").getall()[1],
                'dislikes':
                    response.xpath(".//div[@class='operation mt-2']/a/span/text()").getall()[2],
                'crossing':
                    response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Crossing']/text()").get(),
                'finishing':
                    response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Finishing']/text()").get(),
                'heading_accuracy':
                    response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Heading Accuracy']"
                                   "/text()").get(),
                'short_passing':
                    response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Short Passing']"
                                   "/text()").get(),
                'volleys':
                    response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Volleys']/text()").get(),
                'aggression':
                    response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Aggression']/text()").get(),
                'interceptions':
                    response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Interceptions']"
                                   "/text()").get(),
                'positioning':
                    response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Positioning']/text()").get(),
                'vision':
                    response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Vision']/text()").get(),
                'penalties':
                    response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Penalties']/text()").get(),
                'composure':
                    response.xpath(".//div[@class='column col-4']/div/ul/li[contains(text(), 'Composure')]/span"
                                   "/text()").get(),
                'dribbling':
                    response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Dribbling']/text()").get(),
                'curve':
                    response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Curve']/text()").get(),
                'fk_accuracy':
                    response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='FK Accuracy']/text()").get(),
                'long_passing':
                    response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Long Passing']/text()").get(),
                'ball_control':
                    response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Ball Control']/text()").get(),
                'marking':
                    response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Marking']/text()").get(),
                'standing_tackle':
                    response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Standing Tackle']"
                                   "/text()").get(),
                'sliding_tackle':
                    response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Sliding Tackle']"
                                   "/text()").get(),
                'acceleration':
                    response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Acceleration']/text()").get(),
                'sprint_speed':
                    response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Sprint Speed']/text()").get(),
                'agility':
                    response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Agility']/text()").get(),
                'reactions':
                    response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Reactions']/text()").get(),
                'balance':
                    response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Balance']/text()").get(),
                'gk_diving':
                    response.xpath(".//div[@class='column col-4']/div/ul/li[contains(text(), 'GK Diving')]/span"
                                   "/text()").get(),
                'gk_handling':
                    response.xpath(".//div[@class='column col-4']/div/ul/li[contains(text(), 'GK Handling')]/span"
                                   "/text()").get(),
                'gk_kicking':
                    response.xpath(".//div[@class='column col-4']/div/ul/li[contains(text(), 'GK Kicking')]/span"
                                   "/text()").get(),
                'gk_positioning':
                    response.xpath(".//div[@class='column col-4']/div/ul/li[contains(text(), 'GK Positioning')]/span"
                                   "/text()").get(),
                'gk_reflexes':
                    response.xpath(".//div[@class='column col-4']/div/ul/li[contains(text(), 'GK Reflexes')]/span"
                                   "/text()").get(),
                'shot_power':
                    response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Shot Power']/text()").get(),
                'jumping':
                    response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Jumping']/text()").get(),
                'stamina':
                    response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Stamina']/text()").get(),
                'strength':
                    response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Strength']/text()").get(),
                'long_shots':
                    response.xpath(".//div[@class='column col-4']/div/ul/li/span[../span='Long Shots']/text()").get(),
                'traits':
                    response.xpath(".//div[@class='column col-4']/div/h5[text()='Traits']/following-sibling::ul/li/span"
                                   "/text()").getall(),
                'LS':
                    response.xpath(".//div[../div='LS']/following::text()").get(),
                'ST':
                    response.xpath(".//div[../div='ST']/following::text()").get(),
                'RS':
                    response.xpath(".//div[../div='RS']/following::text()").get(),
                'LW':
                    response.xpath(".//div[../div='LW']/following::text()").get(),
                'LF':
                    response.xpath(".//div[../div='LF']/following::text()").get(),
                'CF':
                    response.xpath(".//div[../div='CF']/following::text()").get(),
                'RF':
                    response.xpath(".//div[../div='RF']/following::text()").get(),
                'RW':
                    response.xpath(".//div[../div='RW']/following::text()").get(),
                'LAM':
                    response.xpath(".//div[../div='LAM']/following::text()").get(),
                'CAM':
                    response.xpath(".//div[../div='CAM']/following::text()").get(),
                'RAM':
                    response.xpath(".//div[../div='RAM']/following::text()").get(),
                'LM':
                    response.xpath(".//div[../div='LM']/following::text()").get(),
                'LCM':
                    response.xpath(".//div[../div='LCM']/following::text()").get(),
                'CM':
                    response.xpath(".//div[../div='CM']/following::text()").get(),
                'RCM':
                    response.xpath(".//div[../div='RCM']/following::text()").get(),
                'RM':
                    response.xpath(".//div[../div='RM']/following::text()").get(),
                'LWB':
                    response.xpath(".//div[../div='LWB']/following::text()").get(),
                'LDM':
                    response.xpath(".//div[../div='LDM']/following::text()").get(),
                'CDM':
                    response.xpath(".//div[../div='CDM']/following::text()").get(),
                'RDM':
                    response.xpath(".//div[../div='RDM']/following::text()").get(),
                'RWB':
                    response.xpath(".//div[../div='RWB']/following::text()").get(),
                'LB':
                    response.xpath(".//div[../div='LB']/following::text()").get(),
                'LCB':
                    response.xpath(".//div[../div='LCB']/following::text()").get(),
                'CB':
                    response.xpath(".//div[../div='CB']/following::text()").get(),
                'RCB':
                    response.xpath(".//div[../div='RCB']/following::text()").get(),
                'RB':
                    response.xpath(".//div[../div='RB']/following::text()").get()
            }


# 'rankings_history': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
# 'total_comments': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
# 'total_recommended': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
# 'hits_comments': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
# 'total_stats': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
# 'similar_players':
# response.xpath(".//div[@id='similar']/table/tbody/tr/td[2]/a/@title").getall()
