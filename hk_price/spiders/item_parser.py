# -*- coding: utf-8 -*-

# 提取网页中的商品

from hk_price.items import GoodsItem


def parse_dfs(item):
    goods = GoodsItem()
    message = item.xpath('div[@class="message"]')
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
    return goods

def parse_sasa(item):
    good = GoodsItem()
    good['brand'] = item.xpath('./a[2]/h2/b/text()').extract()
    good['name'] = item.xpath('@note').extract()
    good['price'] = item.xpath('@price').extract()
    good['old_price'] = item.xpath('@ckj').extract()
    if not good['old_price']:
        good['old_price'] = good['price']
    good['is_promo'] = good['old_price'] != good['price']
    return good
