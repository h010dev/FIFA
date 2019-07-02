from fifa_data.scrapy_redis_spiders import RedisSpider
from fifa_data.tests.sofifa_redis_settings import sofifa_settings
from proxies.proxy_generator import gen_proxy_list
from user_agents.user_agent_generator import gen_useragent_list


class MySpider(RedisSpider):

    name = 'myspider'
    redis_key = 'redis_club_urls:items'

    proxies = gen_proxy_list()
    user_agent = gen_useragent_list()

    custom_settings = sofifa_settings(
        name=name,
        proxies=proxies,
        user_agent=user_agent,
        validator='ClubItem'
    )

    def __init__(self, *args, **kwargs):

        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(MySpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        yield {
            'club_name': response.xpath(".//div[@class='info']/h1/text()").get()
        }
