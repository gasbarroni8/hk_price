# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HkPriceItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class BrandItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()

class GoodsItem(scrapy.Item):
    brand = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    old_price = scrapy.Field()
    is_promo = scrapy.Field()
