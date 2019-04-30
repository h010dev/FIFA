# -*- coding: utf-8 -*-

# Scrapy settings for fifa_market_analysis_ project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'fifa_data'

SPIDER_MODULES = ['fifa_data.spiders']
NEWSPIDER_MODULE = 'fifa_data.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    # 'fifa_market_analysis_.middlewares.UserAgentRotatorMiddleware': 400,
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

DOWNLOADER_MIDDLEWARES.update(
    {
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
    }
)

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#     # 'fifa_market_analysis_.pipelines.MongoDBPipeline': 300,
#     'fifa_market_analysis_.pipelines.ImagesToDownloadPipeline': 1,
#     'fifa_market_analysis_.pipelines.DuplicatesPipeline': 100,
#     'scrapy.pipelines.images.ImagesPipeline': 1,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Specify directory to save scrapy crawl files to by default:

# FEED_FORMAT = 'json'
# FEED_URI = 'file:///C:/Users/E46Racing/Documents/PycharmProjects/my_projects/fifa_workspace/fifa_market_analysis_' \
#            '/fifa_market_analysis_/feed_dump/test.json'

MONGO_URI = 'mongodb://mongo:27017'
# MONGO_DB = 'sofifa_stats'

SPLASH_URL = 'http://localhost:8050'

IMAGES_STORE = 'C:/Users/E46Racing/Documents/PycharmProjects/FIFA/data'

MEDIA_ALLOW_REDIRECTS = True

# DOWNLOAD_TIMEOUT = 1200

# COLLECTION_NAME = 'player_stats'

# ROTATING_PROXY_LIST = [
#             'https://35.225.204.126:80',
#             'https://207.148.9.125:80',
#             'https://159.203.65.214:3128'
#         ]
# 
# USER_AGENTS = [
#     (
#         "Microsoft Office/14.0 (Windows NT 6.1; Microsoft Outlook 14.0.7143; Pro)"
#     ),
#     (
#         "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-en) AppleWebKit/533.19.4 (KHTML, like Gecko) "
#         "Version/5.0.3 Safari/533.19.4"
#     ),
#     (
#         "Mozilla/5.0 (X11; U; Linux i686; en-US) U2/1.0.0 UCBrowser/9.3.1.344"
#     ),
# ]

TELNETCONSOLE_USERNAME = 'mo3nzo'
TELNETCONSOLE_PASSWORD = 'ab7#d_Pl29'
# SPIDERMON_EXPECTED_FINISH_REASONS = ['finished', ]


EXTENSIONS = {'fifa_data.test_extension.CustomStats': 600}
