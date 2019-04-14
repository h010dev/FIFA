# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.media import *
from scrapy import Request
from scrapy.exceptions import DropItem


class MongoDBPipeline(object):

    # collection = 'player_stats'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):

        if spider.settings.get('COLLECTION_NAME') == 'player_stats':

            if (self.db[spider.settings.get('COLLECTION_NAME')].count_documents(
                    {'id': item.get('id_player_main')}) == 1
                    and
                    self.db[spider.settings.get('COLLECTION_NAME')].count_documents(
                    {'id': item.get('id_player_secondary')}) == 1):
                raise DropItem('Item dropped')
            else:
                self.db[spider.settings.get('COLLECTION_NAME')].update(
                    {
                        'id_player_main': item.get('id_player_main'),
                        'id_player_secondary': item.get('id_player_secondary')
                    },
                    dict(item),
                    upsert=True)
                return item

        elif spider.settings.get('COLLECTION_NAME') == 'club_stats':

            if (self.db[spider.settings.get('COLLECTION_NAME')].count_documents(
                    {'id': item.get('id_club_main')}) == 1
                    and
                    self.db[spider.settings.get('COLLECTION_NAME')].count_documents(
                    {'id': item.get('id_club_secondary')}) == 1):
                raise DropItem('Item dropped')
            else:
                self.db[spider.settings.get('COLLECTION_NAME')].update(
                    {
                        'id_player_main': item.get('id_club_main'),
                        'id_player_secondary': item.get('id_club_secondary')
                    },
                    dict(item),
                    upsert=True)
                return item

        elif spider.settings.get('COLLECTION_NAME') == 'team_stats':

            if (self.db[spider.settings.get('COLLECTION_NAME')].count_documents(
                    {'id': item.get('id_team_main')}) == 1
                    and
                    self.db[spider.settings.get('COLLECTION_NAME')].count_documents(
                    {'id': item.get('id_team_secondary')}) == 1):
                raise DropItem('Item dropped')
            else:
                self.db[spider.settings.get('COLLECTION_NAME')].update(
                    {
                        'id_player_main': item.get('id_team_main'),
                        'id_player_secondary': item.get('id_team_secondary')
                    },
                    dict(item),
                    upsert=True)
                return item

        elif spider.settings.get('COLLECTION_NAME') == 'user_agents':

            if self.db[spider.settings.get('COLLECTION_NAME')].count_documents(
                    {'id': item.get('user_agent')}) == 1:
                raise DropItem('Item dropped')
            else:
                self.db[spider.settings.get('COLLECTION_NAME')].update(
                    {
                        'user_agent': item.get('user_agent'),
                    },
                    dict(item),
                    upsert=True)
                return item

        elif spider.settings.get('COLLECTION_NAME') == 'player_urls':

            if self.db[spider.settings.get('COLLECTION_NAME')].count_documents(
                    {'id': item.get('id_player_main')}) == 1:
                raise DropItem('Item dropped')
            else:
                self.db[spider.settings.get('COLLECTION_NAME')].update(
                    {
                        'id_player_main': item.get('id_player_main'),
                    },
                    dict(item),
                    upsert=True)
                return item

        elif spider.settings.get('COLLECTION_NAME') == 'player_details':

            if self.db[spider.settings.get('COLLECTION_NAME')].count_documents(
                    {'id': item.get('id_player_secondary')}) == 1:
                raise DropItem('Item dropped')
            else:
                self.db[spider.settings.get('COLLECTION_NAME')].update(
                    {
                        'id_player_secondary': item.get('id_player_secondary'),
                    },
                    dict(item),
                    upsert=True)
                return item


class ImagesToDownloadPipeline(ImagesPipeline, MediaPipeline):

    def get_media_requests(self, item, info):
        return [Request(x, meta={'id': item.get('id'),
                                 'category': item.get('category'),
                                 'team_or_club': item.get('team_or_club')})
                for x in item.get(self.images_urls_field, [])]

    def _process_request(self, request, info):
        fp = request_fingerprint(request)
        cb = request.callback or (lambda _: _)
        eb = request.errback
        request.callback = None
        request.errback = None

        # Return cached result if request was already seen
        # if fp in info.downloaded:
        #     return defer_result(info.downloaded[fp]).addCallbacks(cb, eb)

        # Otherwise, wait for result
        wad = Deferred().addCallbacks(cb, eb)
        info.waiting[fp].append(wad)

        # Check if request is downloading right now to avoid doing it twice
        # if fp in info.downloading:
        #     return wad

        # Download request checking media_to_download hook output first
        info.downloading.add(fp)
        dfd = mustbe_deferred(self.media_to_download, request, info)
        dfd.addCallback(self._check_media_to_download, request, info)
        dfd.addBoth(self._cache_result_and_execute_waiters, fp, info)
        dfd.addErrback(lambda f: logger.error(
            f.value, exc_info=failure_to_exc_info(f), extra={'spider': info.spider})
        )
        return dfd.addBoth(lambda _: wad)  # it must return wad at last

    def file_path(self, request, response=None, info=None):

        def _warn():
            from scrapy.exceptions import ScrapyDeprecationWarning
            import warnings
            warnings.warn('ImagesPipeline.image_key(url) and file_key(url) methods are deprecated, '
                          'please use file_path(request, response=None, info=None) instead',
                          category=ScrapyDeprecationWarning, stacklevel=1)

        if not isinstance(request, Request):
            _warn()
            url = request
        else:
            url = request.url

        if not hasattr(self.file_key, '_base'):
            _warn()
            return self.file_key(url)
        elif not hasattr(self.image_key, '_base'):
            _warn()
            return self.image_key(url)

        return 'full/%s.jpg' % (str(request.meta['id']) + '_' + str(request.meta['category']) + '_' +
                                str(request.meta['team_or_club']))


class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item.get('id') in self.ids_seen:
            raise DropItem(f'Duplicate item found: {item}')
        else:
            self.ids_seen.add(item.get('id'))
            return item
