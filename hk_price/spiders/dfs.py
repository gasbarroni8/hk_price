# -*- coding: utf-8 -*-
import scrapy
from hk_price.items import BrandItem, GoodsItem
from .item_parser import parse_dfs

class DFSSpider(scrapy.Spider):
    name = 'dfs'
    allowed_domains = ['www.dfsglobal.cn']
    start_urls = ['https://www.dfsglobal.cn/cn/hong-kong/brands']

    def parse(self, response):
        for b in response.xpath('//a[@itemprop="url"]'):
            brand = BrandItem()
            brand['name'] = b.xpath("span/text()").extract()
            brand['link'] = b.xpath('./@href').extract()
            link = b.xpath('./@href').extract()[0]
            brand_page = 'https://www.dfsglobal.cn' + link
            yield scrapy.Request(brand_page, callback=self.parse_price)

    def parse_price(self, response):
        item = response.xpath('//a[@itemprop="url"]')
        for i in item:
            yield parse_dfs(i)
        pages = response.xpath('//ul[@class="pagination"]')
        last_page = pages.xpath('li[@class="last"]/a/text()').extract()
        if last_page:
            brand_url = response.url.split("?")[0]
            last_page = int(last_page[0])
            for page in range(1, last_page):
                next_page = brand_url + "?q=:blprelevance&page=" + str(page)
                yield scrapy.Request(next_page, callback=self.parse_price)

