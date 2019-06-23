import datetime

from fifa_data.mongodb_addr import host, port


def sofifa_settings(name, proxies, user_agent, validator):

    settings = {

        # DATA STORAGE
        'FEED_FORMAT': 'json',
        'FEED_URI': '/home/mohamed/Projects/FIFA/fifa_data/club_dump.json',

        # SPIDER LOGGING
        'LOG_ENABLED': False,
        'LOG_LEVEL': 'DEBUG',
        'LOG_FILE': f'logs/{name}_log_{datetime.date.today()}.txt',

        # EXTENSION ACTIVATION
        'SPIDERMON_ENABLED': True,
        'EXTENSIONS': {
            'fifa_data.test_extension.CustomStats': 600,
            'spidermon.contrib.scrapy.extensions.Spidermon': 510,
        },

        # BAN PREVENTION
        'USER_AGENTS': user_agent,

        # MISC. SETTINGS
        'HTTPCACHE_ENABLED': False,
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_TIMEOUT': 30,

        # PIPELINES, MIDDLEWARES, AND EXTENSIONS
        'ITEM_PIPELINES': {
            'spidermon.contrib.scrapy.pipelines.ItemValidationPipeline': 800,
        },

        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_useragents.downloadermiddlewares.useragents.'\
            'UserAgentsMiddleware': 500,
        },

        'SPIDERMON_SPIDER_CLOSE_MONITORS': (
            'fifa_data.monitors.SpiderCloseMonitorSuite',
        ),

        'SPIDERMON_VALIDATION_MODELS': (
            f'fifa_data.validators.{validator}',
        ),

        'SPIDERMON_PERIODIC_MONITORS': {
            'fifa_data.monitors.PeriodicMonitorSuite': 300,
        },

        # TODO integrate expected finish reasons into settings: currently
        # defined in monitors.
        # 'SPIDERMON_EXPECTED_FINISH_REASONS': ['finished', ]
    }

    return settings
