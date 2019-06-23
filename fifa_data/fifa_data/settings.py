from fifa_data.mongodb_addr import host, port

BOT_NAME = 'fifa_data'

SPIDER_MODULES = ['fifa_data.spiders']

NEWSPIDER_MODULE = 'fifa_data.spiders'

USER_AGENT = "'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) "\
    "Gecko/20100101 Firefox/48.0'"

ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 400

#DOWNLOAD_DELAY = 1

CONCURRENT_REQUESTS_PER_DOMAIN = 200

CONCURRENT_REQUESTS_PER_IP = 0

DNSCACHE_ENABLED = True

DNSCACHE_SIZE = 10000

DNS_TIMEOUT = 60

MEMUSAGE_ENABLED = True

#COOKIES_ENABLED = False

#TELNETCONSOLE_ENABLED = False

#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

#SPIDER_MIDDLEWARES = {
#    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
#}

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    # 'fifa_market_analysis_.middlewares.UserAgentRotatorMiddleware': 400,
    # 'scrapy_splash.SplashCookiesMiddleware': 723,
    # 'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.'\
    'HttpCompressionMiddleware': 810,
}

DOWNLOADER_MIDDLEWARES.update(
    {
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        'scrapy_useragents.downloadermiddlewares.useragents.'\
        'UserAgentsMiddleware': 500,
    }
)

#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# ITEM_PIPELINES = {
#     # 'fifa_market_analysis_.pipelines.MongoDBPipeline': 300,
#     'fifa_market_analysis_.pipelines.ImagesToDownloadPipeline': 1,
#     'fifa_market_analysis_.pipelines.DuplicatesPipeline': 100,
#     'scrapy.pipelines.images.ImagesPipeline': 1,
# }

AUTOTHROTTLE_ENABLED = True

#AUTOTHROTTLE_START_DELAY = 5

#AUTOTHROTTLE_MAX_DELAY = 60

AUTOTHROTTLE_TARGET_CONCURRENCY = 200

AUTOTHROTTLE_DEBUG = True

#HTTPCACHE_ENABLED = True

#HTTPCACHE_EXPIRATION_SECS = 0

#HTTPCACHE_DIR = 'httpcache'

#HTTPCACHE_IGNORE_HTTP_CODES = []

#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# FEED_FORMAT = 'json'

# FEED_URI = 'file:///C:/Users/E46Racing/Documents/PycharmProjects/'\
# 'my_projects/fifa_workspace/fifa_market_analysis_' \
#            '/fifa_market_analysis_/feed_dump/test.json'

MONGO_URI = f'mongodb://{host}:{port}'

SPLASH_URL = 'http://localhost:8050'

#IMAGES_STORE = 'C:/Users/E46Racing/Documents/PycharmProjects/FIFA/data'

MEDIA_ALLOW_REDIRECTS = True

TELNETCONSOLE_USERNAME = 'mo3nzo'

TELNETCONSOLE_PASSWORD = 'ab7#d_Pl29'
