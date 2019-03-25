import scrapy


class SofifaSpider(scrapy.Spider):

    name = 'sofifa'

    def start_requests(self):

        urls = [
            'https://sofifa.com/players'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        page = response.url
        _file = f'{page}.html'
        with open(_file, 'wb') as f:
            f.write(response.body)


