# -*- coding: utf-8 -*-
import scrapy
from hk_price.items import GoodsItem
from .item_parser import parse_sasa


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
            yield parse_sasa(item)
        next_page = response.xpath('//a[@class="btn_next"]/@href')
        if next_page:
            next_page_url = self.root + next_page[0].extract()
            yield scrapy.Request(next_page_url, callback = self.parse_price)