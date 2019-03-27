# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from scrapy.selector import Selector


class FutbinSpider(scrapy.Spider):
    name = 'futbin'

    script = """
    function main(splash, args)
      assert(splash:go(args.url))
      assert(splash:wait(5))
      assert(splash:runjs('document.querySelector(".btn[href$=XONE]").href'))
      splash:set_viewport_full()
      return {
        html = splash:html(),
        png = splash:png(),
        har = splash:har(),
      }
    end
    """

    def start_request(self):
        url = 'https://www.futbin.com/market/auctions'
        yield SplashRequest(url=url, callback=self.parse, endpoint='render.html', args={'wait': 5})
        yield SplashRequest(url=url, callback=self.parse_other_links, endpoint='execute',
                            args={'wait': 5, 'lua_source': self.script}, dont_filter=True)

    def parse(self, response):

        for button in response.xpath("//li[contains(@class, 'pull-right')]"):
            yield {
                'pc': button.xpath("//li[contains(@class, 'pull-right')][1]/a/@href").extract(),
                'xbox': button.xpath("//li[contains(@class, 'pull-right')][2]/a/@href").extract(),
                'ps4': button.xpath("//li[contains(@class, 'pull-right')][3]/a/@href").extract()
            }

    def parse_other_links(self, response):
        for link in response.data:
            sel = Selector(text=link)
            yield {
                'pc': sel.xpath("//li[contains(@class, 'pull-right')][1]/a/@href").extract(),
                'xbox': sel.xpath("//li[contains(@class, 'pull-right')][2]/a/@href").extract(),
                'ps4': sel.xpath("//li[contains(@class, 'pull-right')][3]/a/@href").extract()
            }
