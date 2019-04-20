import scrapy


class TestSpider(scrapy.Spider):

    name = 'test_spider'
    start_urls = ['http://quotes.toscrape.com/']

    custom_settings = {
        'EXTENSIONS': {
            'scrapy.extensions.test_extension.CustomStats': 500
        }
    }

    def parse(self, response):
        for row in response.xpath("//div[@class='row']/div[@class='col-md-8']/div"):
            yield {
                'quote': row.xpath(".//span[@class='text']/text()"),
            }

        next_page = response.xpath("//li[@class='next']/a/@href").get()
        if next_page is not None:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)
