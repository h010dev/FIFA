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
        Rule(LinkExtractor(restrict_xpaths="//a[text()='Next']"), callback='parse_item', follow=True)
    )

    def parse_item(self, response):

        for stat in response.xpath("//div[@class='teams']/div[@class='columns']/div[@class='column col-4'][1]/ul"):
            yield {
                'name_id':
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
                    stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'full_name': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'flag_img': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'player_img': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'club_logo_img': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'national_team_logo_img': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'positions': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'age': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'dob': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'height': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'weight': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'overall_rating': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'potential': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'value': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'wage': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'club_name': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'national_team': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'club_rating': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'national_team_rating': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'club_position': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'national_team_position': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'club_jersey_no': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'national_team_jersey_no': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'club_join_date': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'club_contract_valid_until': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'unique_attributes_tags': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract(),
                'followers': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'likes': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'dislikes': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'crossing': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'finishing': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'heading_accuracy': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'short_passing': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'volleys': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'aggression': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'interceptions': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'positioning': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'vision': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'penalties': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'composure': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'dribbling': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'curve': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'fk_accuracy': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'long_passing': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'ball_control': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'marking': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'standing_tackle': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'sliding_tackle': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'acceleration': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'sprint_speed': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'agility': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'reactions': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'balance': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'gk_diving': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'gk_handling': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'gk_kicking': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'gk_positioning': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'gk_reflexes': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'shot_power': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'jumping': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'stamina': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'strength': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'long_shots': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'traits': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract(),
                'LS': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'ST': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'RS': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'LW': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'LF': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'CF': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'RF': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'RW': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'LAM': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'CAM': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'RAM': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'LM': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'LCM': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'CM': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'RCM': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'RM': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'LWB': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'LDM': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'CDM': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'RDM': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'RWB': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'LB': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'LCB': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'CB': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'RCB': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'RB': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'rankings_history': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'total_comments': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'total_recommended': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'hits_comments': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'total_stats': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract_first(),
                'similar_players': stat.xpath(".//li/label[text()='Release Clause']/text()/following::span/text()").extract()
            }
