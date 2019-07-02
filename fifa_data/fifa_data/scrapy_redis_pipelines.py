from rejson import Client, Path

from scrapy.utils.misc import load_object
from scrapy.utils.serialize import ScrapyJSONEncoder
from twisted.internet.threads import deferToThread

from fifa_data import scrapy_redis_defaults


default_serialize = ScrapyJSONEncoder().encode


class RedisPipeline(object):
    """Pushes serialized item into a redis list/queue
    Settings
    --------
    REDIS_ITEMS_KEY : str
        Redis key where to store items.
    REDIS_ITEMS_SERIALIZER : str
        Object path to serializer function.
    """

    def __init__(self, server,
                 key=scrapy_redis_defaults.PIPELINE_KEY,
                 serialize_func=default_serialize):
        """Initialize pipeline.
        Parameters
        ----------
        server : StrictRedis
            Redis client instance.
        key : str
            Redis key where to store items.
        serialize_func : callable
            Items serializer function.
        """
        self.server = server
        self.key = key
        self.serialize = serialize_func

    @classmethod
    def from_settings(cls, settings):
        params = {
            'server': Client(
                host='localhost', port=6379, decode_responses=True
            ),
        }
        if settings.get('REDIS_ITEMS_KEY'):
            params['key'] = settings['REDIS_ITEMS_KEY']
        if settings.get('REDIS_ITEMS_SERIALIZER'):
            params['serialize_func'] = load_object(
                settings['REDIS_ITEMS_SERIALIZER']
            )

        return cls(**params)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    def process_item(self, item, spider):
        return deferToThread(self._process_item, item, spider)

    def _process_item(self, item, spider):
        key = self.item_key(item, spider)
        self.server.jsonset(key, Path.rootPath(), item._values)
#        self.server.sadd('club_keys', key)
#        self.server.sadd('club_urls', self.server.jsonget(key, Path('.club_page')))
        return item

    def item_key(self, item, spider):
        """Returns redis key based on given spider.
        Override this function to use a different key depending on the item
        and/or spider.
        """
        key = str(spider.name + ':' + 'item' + ':' + str(item['id']))
        return key
