# -*- coding: utf-8 -*-
import scrapy
import difflib
import re
from hk_price.items import SearchItem, GoodsItem
from .item_parser import parse_sasa, parse_dfs


class SearchSpider(scrapy.Spider):
    name = 'search'
    allowed_domains = ['www.dfsglobal.cn', 'hongkong.sasa.com']
    start_urls = [
        "https://www.baidu.com/"]
    text = ""
    match_threshold = 0.4
    brand_match_threshold = 0.3
    dfs_search_prefix = "https://www.dfsglobal.cn/cn/hong-kong/search/shop?text="
    sasa_search_prefix = "https://hongkong.sasa.com/SasaWeb/sch/product/searchKeyword.jspa?qs="

    def parse(self, response):
        yield scrapy.Request(self.dfs_search_prefix + self.text, callback=self.search_dfs)
        yield scrapy.Request(self.sasa_search_prefix + self.text, callback=self.search_sasa)

    def search_sasa(self, response):
        root = "https://hongkong.sasa.com"
        has_item = response.xpath('//div[@class="filter-box mt-15"]')
        if has_item:
            for item in response.xpath('//div[@class="box_list"]/ul/li/div'):
                s = SearchItem(parse_sasa(item))
                name = s['name'][0].replace(
                    "<font color='RED'>", " ").replace("</font>", ' ')
                name = re.sub(' +', ' ', name)
                s['name'] = [name]
                s['brand'] = [' '.join(item.xpath('./a/h2[@class="ellipsis"]/b/font/text()').extract())]
                s['link'] = [
                    root + item.xpath("../a[@class='btn-gray']/@href").extract()[0]]
                if self.filter(s):
                    yield s

    def search_dfs(self, response):
        root = "https://www.dfsglobal.cn"
        for item in response.xpath('//a[@itemprop="url"]')[:10]:
            s = SearchItem(parse_dfs(item))
            s['link'] = [root + item.xpath("./@href").extract()[0]]
            s['source'] = "dfs"
            if self.filter(s):
                yield s

    def filter(self, s):
        name_score = self.string_similar(self.text.lower(), s['name'][0].lower())
        brand_score = self.string_similar(self.text.lower(), s['brand'][0].lower())
        return name_score > self.match_threshold or brand_score > self.brand_match_threshold

    def string_similar(self, s1, s2):
        return difflib.SequenceMatcher(None, s1, s2).quick_ratio()
