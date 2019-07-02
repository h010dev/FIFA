import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity


class TestLoader(scrapy.Item):

    first_name = scrapy.Field(
        input_processor=Identity(),
        output_processor=Identity()
    )

    last_name = scrapy.Field(
        input_processor=Identity(),
        output_processor=Identity()
    )


class TestSpider(scrapy.Spider):

    name = 'test_spider'

    def start_requests(self):

        urls = [
            'https://google.com'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        l = ItemLoader(item=TestLoader(), response=response)
        l.add_value('first_name', 'billy')
        l.add_value('last_name', 'jones')
        print(self.item.__getitem__())
        print(self.item.keys())
        return l.load_item()


if __name__ == '__main__':
    TestSpider()
