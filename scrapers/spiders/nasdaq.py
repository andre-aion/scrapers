# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector,HtmlXPathSelector as hxs
from scrapers.items import NasdaqItem
import logging

logging.getLogger('scrapy').setLevel(logging.WARNING)


class NasdaqSpider(scrapy.Spider):
    name = 'nasdaq'
    allowed_domains = ['nasdaq.com']
    start_urls = ['https://www.nasdaq.com/']

    def parse(self, response):
        sel = Selector(response)
        print("PROCESSING:" + response.url)
        pattern = '[ ]?nasdaqHomeIndexChart\.storeIndexInfo\(\"NASDAQ\",[0-9|\"|,|\.|\-]*\)'
        table = sel.xpath('//table[@id="indexTable"]').get()
        data = sel.xpath('//table[@id="indexTable"]').re(pattern)
        lst = data[0].split(",")
        lst[1] = lst[1].replace('"',' ').strip()
        lst[2] = lst[2].replace('"',' ').strip()

        item = NasdaqItem()
        item['nasdaq'] = float(lst[1])
        item['nasdaq_delta'] = float(lst[2])
        print('nasdaq',item['nasdaq'])
        yield item
