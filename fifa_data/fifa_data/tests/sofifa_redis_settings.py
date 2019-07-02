import datetime


def sofifa_settings(name, proxies, user_agent, validator):

    settings = {

        # REDIS
        'DUPEFILTER_CLASS': 'fifa_data.scrapy_redis_dupefilter.RFPDupeFilter',
#        'SCHEDULER': 'fifa_data.scrapy_redis_scheduler.Scheduler',
        'SCHEDULER_PERSIST': False,
        'DOWNLOAD_DELAY': 1,
        'REDIS_START_URLS_AS_SET': True,
        'REDIS_START_URLS_KEY': 'all_urls',
        'SCHEDULER_QUEUE_CLASS': 'fifa_data.scrapy_redis_queue.FifoQueue',
        'REDIS_START_URLS_BATCH_SIZE': 10,

        # SPIDER LOGGING
        'LOG_ENABLED': True,
        'LOG_LEVEL': 'DEBUG',
        'LOG_FILE': f'logs/{name}_log_{datetime.date.today()}.txt',

        # EXTENSION ACTIVATION
        'PROXY_POOL_ENABLED': True,
        'EXTENSIONS': {
            'fifa_data.test_extension.CustomStats': 600,
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
            'fifa_data.scrapy_redis_pipelines.RedisPipeline': 300,
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
