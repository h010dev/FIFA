import datetime

from fifa_data.mongodb_addr import host, port


def sofifa_settings(name, proxies, user_agent, validator):

    settings = {

        # STORAGE
        'FEED_FORMAT': 'json',
        'FEED_URI': f'/home/mohamed/Projects/FIFA/fifa_data/{name}_data.json',

        # SPIDER LOGGING
        'LOG_ENABLED': False,

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
            'fifa_data.pipelines.SpiderStats': 301,
        },

        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_useragents.downloadermiddlewares.useragents.'\
            'UserAgentsMiddleware': 500,
            'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
            'rotating_proxies.middlewares.BanDetectionMiddleware': 620
        },

        # TODO integrate expected finish reasons into settings: currently
        # defined in monitors.
        # 'SPIDERMON_EXPECTED_FINISH_REASONS': ['finished', ]
    }

    return settings
