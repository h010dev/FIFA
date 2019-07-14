import datetime

from fifa_data.mongodb_addr import host, port


def useragent_settings(name, database, collection, proxies, user_agent,
                       validator, timeout):

    settings = {

        # REDIS
        'DUPEFILTER_CLASS': 'fifa_data.scrapy_redis_custom.dupefilter.RFPDupeFilter',
        'DOWNLOAD_DELAY': 1,

        # SPIDER CHECKPOINTS
        'JOBDIR': f'pause_resume/{name}',

        # SPIDER LOGGING
        'LOG_ENABLED': True,
        'LOG_LEVEL': 'DEBUG',
        'LOG_FILE': f'logs/{name}_log_{datetime.date.today()}.txt',

        # EXTENSION ACTIVATION
        'PROXY_POOL_ENABLED': True,
        'EXTENSIONS': {
            'fifa_data.test_extension.CustomStats': 600,
            'scrapy.extensions.closespider.CloseSpider': 400,
        },

        # BAN PREVENTION
        'ROTATING_PROXY_LIST': proxies,
        'USER_AGENTS': user_agent,

        # MISC. SETTINGS
        'HTTPCACHE_ENABLED': False,
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_TIMEOUT': 30,
        'CLOSESPIDER_TIMEOUT': timeout,
        'DEPTH_STATS_VERBOSE': True,

        # PIPELINES, MIDDLEWARES, AND EXTENSIONS
        'ITEM_PIPELINES': {
            'fifa_data.scrapy_redis_custom.pipelines.RedisPipeline': 300,
            'fifa_data.pipelines.SpiderStats': 301,
        },

        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_useragents.downloadermiddlewares.useragents.'\
            'UserAgentsMiddleware': 500,
            'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
            'rotating_proxies.middlewares.BanDetectionMiddleware': 620
        },
    }

    return settings
