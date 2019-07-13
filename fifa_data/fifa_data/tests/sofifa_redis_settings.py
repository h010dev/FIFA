import datetime


def sofifa_settings(name, proxies, user_agent, validator):

    settings = {

        # REDIS
        'DUPEFILTER_CLASS': 'fifa_data.scrapy_redis_custom.dupefilter.RFPDupeFilter',
#        'SCHEDULER': 'fifa_data.scrapy_redis_scheduler.Scheduler',
#        'SCHEDULER_PERSIST': False,
        'DOWNLOAD_DELAY': 1,
        'REDIS_START_URLS_AS_SET': True,
        'REDIS_START_URLS_BATCH_SIZE': 550,

        # SPIDER LOGGING
        'LOG_ENABLED': False,
        'LOG_LEVEL': 'DEBUG',
        'LOG_FILE': f'logs/{name}_log_{datetime.date.today()}.txt',

        # EXTENSION ACTIVATION
        'PROXY_POOL_ENABLED': True,
        'EXTENSIONS': {
            'fifa_data.test_extension.CustomStats': 700,
        },

        # BAN PREVENTION
        'ROTATING_PROXY_LIST': proxies,
        'USER_AGENTS': user_agent,

        # MISC. SETTINGS
        'HTTPCACHE_ENABLED': False,
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_TIMEOUT': 0,
        'ROTATING_PROXY_BACKOFF_BASE': 1200,

        # PIPELINES, MIDDLEWARES, AND EXTENSIONS
        'ITEM_PIPELINES': {
            'fifa_data.scrapy_redis_custom.pipelines.RedisPipeline': 300,
            'fifa_data.pipelines.SpiderStats': 400,
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
