import scrapy
from scrapy.loader import ItemLoader
from fifa_market_analysis.items import SofifaItem


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

        for row in response.selector.xpath("//table[@class='table table-hover persist-area']/tbody/tr"):

            loader = ItemLoader(item=SofifaItem(), selector=row, response=response)
            loader.add_xpath('name', ".//a[contains(@href, '/player/')]/text()[1]")
            loader.add_xpath('position', ".//span[contains(@class, 'pos')]/text()[1]")
            loader.add_xpath('age', ".//*[@class='col-digit col-ae']/text()[1]")
            loader.add_xpath('overall', ".//*[@class='col-digit col-oa']/span/text()[1]")
            loader.add_xpath('team', ".//a[contains(@href, '/team/')]/text()[1]")
            loader.add_xpath('contract', ".//div[@class='subtitle text-ellipsis rtl']/text()[1]")
            loader.add_xpath('value', ".//div[@class='col-digit col-vl']/text()[1]")
            loader.add_xpath('wage', ".//div[@class='col-digit col-wg']/text()[1]")
            loader.add_xpath('total_stats', ".//div[@class='col-digit col-tt']/text()[1]")
            loader.add_xpath('hits_comments', ".//div[@class='col-comments text-right text-ellipsis rtl']/text()[1]")

            yield loader.load_item()

        second_page = response.selector.xpath(f"//a[@class='btn pjax'][{1}]/@href").extract_first()
        next_page = response.selector.xpath(f"//a[@class='btn pjax'][{2}]/@href").extract_first()

        if next_page is None:
            # Used for first page only, since there is no previous button
            second_page_link = response.urljoin(second_page)
            yield scrapy.Request(url=second_page_link, callback=self.parse)

        elif next_page is not None:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)
