# -*- coding: utf-8 -*-
import scrapy
from hk_price.items import BrandItem, GoodsItem


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
            goods = GoodsItem()
            message = i.xpath('div[@class="message"]')
            goods['brand'] = message.xpath(
                'p[@itemprop="name"]/text()').extract()
            goods['name'] = message.xpath(
                'p[@itemprop="description"]/text()').extract()

            no_promote_price = message.xpath(
                'p[@class="price font-medium no-promo"]/text()').extract()
            if no_promote_price:
                price = old_price = no_promote_price
                goods['is_promo'] = False
            else:
                price = message.xpath(
                    'p[@class="price font-medium"]/text()').extract()
                old_price = message.xpath(
                    'p[@class="old-price font-medium"]/text()').extract()
                goods['is_promo'] = True

            goods['price'] = price
            goods['old_price'] = old_price
            yield goods

        pages = response.xpath('//ul[@class="pagination"]')
        last_page = pages.xpath('li[@class="last"]/a/text()').extract()
        if last_page:
            brand_url = response.url.split("?")[0]
            print(brand_url)
            last_page = int(last_page[0])
            for page in range(1, last_page):
                next_page = brand_url + "?q=:blprelevance&page=" + str(page)
                yield scrapy.Request(next_page, callback=self.parse_price)

