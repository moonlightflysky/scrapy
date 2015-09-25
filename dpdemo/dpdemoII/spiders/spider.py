# -*- coding: utf-8 -*-

import re
from urlparse import urljoin


from scrapy.selector import Selector
try:
    from scrapy.spider import Spider
except:
    from scrapy.spider import BaseSpider as Spider
from scrapy.utils.response import get_base_url
from scrapy import log
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.http import Request
from scrapy.contrib.closespider import CloseSpider

from dpdemoII.items import ShopsItem
from dpdemoII.misc.log import *

class DianpingSpider(CrawlSpider):
    """爬取大众点评一个页面信息"""
    name = "DpSpider"
    allowed_domains = ["dianping.com"]
    website = 'http://www.dianping.com'
    download_delay = 2

    start_urls = [
        'http://www.dianping.com/search/category/17/10'
    ]

    rules = (
        Rule(LinkExtractor(allow=r'/search/category/17/10/g\d+'), callback='parse_shop_list', follow=True),
        Rule(LinkExtractor(allow=r'/shop/[0-9]+$'), callback='parse_shop', follow=True),
        Rule(LinkExtractor(allow=r'/search/category/17/10/p[0-9]+\?aid=.*'), callback='parse_shop_list', follow=True)
    )


    def parse_start_url(self, response):
        shop_list_pattern = re.compile("/search/category/17/10/g\d+")
        shop_urls = response.xpath("//@href").extract()
        for url in shop_urls:
            if shop_list_pattern.findall(url):
                yield Request(self.website + url.encode('utf8'), cookies={'cye': 'xian'},
                              callback=self.parse_shop_list)

    def parse_shop_list(self, response):
        shop_urls = response.xpath('//*[@id="shop-all-list"]/ul/li/div[2]/div[1]/a[1]/@href').extract()
        for url in shop_urls:
            yield Request(self.website + url.encode("utf8"), cookies={'cye': 'xian'}, callback=self.parse_shop)

    def parse_shop(self, response):
        shop = ShopsItem()
        shop_url = response.url

        status_code = response.status
        if status_code == 403:  #当爬虫被禁时，关闭爬虫
            raise CloseSpider('========   SPIDER WAS FORBIDDEN  =========')

        shop['shop_name'] = response.xpath('//h1[@class="shop-name"]/text()').extract()
        shop['street_address'] = response.xpath('//span[@itemprop="street-address"]/text()').extract()
        shop['shop_tel'] = response.xpath(
            '//p[@class="expand-info tel"]/span[text()="' + u"电话：" + '"]/..//text()[position()>1]').extract()
        shop['open_time'] = response.xpath(
            '//p[@class="info info-indent"]/span[text()="' + u"营业时间：" + '"]/..//text()[position()>1]').extract()
        shop['shop_tags'] = response.xpath(
            '//p[@class="info info-indent"]/span[text()="' + u"分类标签：" + '"]/..//text()[position()>1]').extract()
        scripts = response.xpath('//script/text()').extract()
        shop['shop_dianping_url'] = [shop_url]
        shop['id'] = shop_url.rsplit('/', 1)[1]
        shop['shop_city'] = response.xpath("//div[@class='breadcrumb']/a[1]/text()").extract()
        shop['shop_district'] = response.xpath("//div[@class='breadcrumb']/a[2]/text()").extract()
        shop['shop_region'] = response.xpath("//div[@class='breadcrumb']/a[3]/text()").extract()
        shop['shop_category'] = response.xpath("//div[@class='breadcrumb']/a[4]/text()").extract()



        yield shop