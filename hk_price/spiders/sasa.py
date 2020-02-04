# -*- coding: utf-8 -*-
import scrapy
from hk_price.items import GoodsItem


class SasaSpider(scrapy.Spider):
    name = 'sasa'
    allowed_domains = ['hongkong.sasa.com']
    start_urls = ['https://hongkong.sasa.com/SasaWeb/sch/product/shop_by_brand.jsp?cm_re=sch_nav_searchbybrand']
    brand_prefix = "/SasaWeb/sch/product/searchProduct.jspa?brandId="
    root = "https://hongkong.sasa.com/"

    def parse(self, response):
        for brands in response.xpath('//div[@class="search_num"]'):
            for brand in brands.xpath('./descendant::a/@href').extract():
                if self.brand_prefix in brand:
                    yield scrapy.Request(self.root + brand, callback = self.parse_price)

    def parse_price(self, response):
        for item in response.xpath('//div[@class="box_list"]/ul/li/div'):
            good = GoodsItem()
            good['brand'] = item.xpath('./a[2]/h2/b/text()').extract()
            good['name'] = item.xpath('@note').extract()
            good['price'] = item.xpath('@price').extract()
            good['old_price'] = item.xpath('@ckj').extract()
            if not good['old_price']:
                good['old_price'] = good['price']
            good['is_promo'] = good['old_price'] != good['price']
            yield good
        next_page = response.xpath('//a[@class="btn_next"]/@href')
        if next_page:
            next_page_url = self.root + next_page[0].extract()
            yield scrapy.Request(next_page_url, callback = self.parse_price)