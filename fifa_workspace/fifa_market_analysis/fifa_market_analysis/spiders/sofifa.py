import scrapy


class SofifaSpider(scrapy.Spider):

    name = 'sofifa'

    def start_requests(self):

        urls = [
            'https://sofifa.com/players'
        ]

        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}

        for url in urls:
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    def parse(self, response):

        page = response.url
        _file = 'sofifa.html'
        with open(_file, 'wb') as f:
            f.write(response.body)


