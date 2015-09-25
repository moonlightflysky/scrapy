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

from dpdemo.items import DpdemoItem
from dpdemo.misc.log import *

class DianpingSpider(Spider):
    """爬取大众点评一个页面信息"""
    name = "DpSpider"
    allowed_domains = ["www.dianping.com"]

    download_delay = 2
    start_urls = ["http://www.dianping.com/shop/18525714",
                  "http://www.dianping.com/shop/21029470",
                  "http://www.dianping.com/shop/18016330",
                  "http://www.dianping.com/shop/19363280"]


    def parse(self, response):

        sel = Selector(response)
        raw_name = sel.xpath('//h1[@class = "shop-name"]')
        brief_info = sel.xpath('//div[@id="basic-info"]/div[1]/span')
        raw_phone = sel.xpath('//div[@id="basic-info"]/p[1]/span[2]')
        raw_address = sel.xpath('//div[@id="basic-info"]/div[2]/span[2]')

        #不同页面的time位置不同，顾做一个判断
        raw_time = sel.xpath('//div[@id="basic-info"]/div[3]/p[2]/span[2]')
        tags = sel.xpath('//div[@id="basic-info"]/div[3]/p[5]/span[position()>1]')
        if raw_time == []:
            raw_time = sel.xpath('//div[@id="basic-info"]/div[3]/p[1]/span[2]')
            tags = sel.xpath('//div[@id="basic-info"]/div[3]/p[4]/span[position()>1]')



        #批量获取标签
        dpitem = DpdemoItem()
        tagwords = ''
        length = len(tags)

        stars = brief_info[0].xpath('@title').extract()

        binfo = ''
        skip = True
        for element in brief_info:

            if skip == True:
                skip = False
            else:
                tmp = element.xpath('text()').extract()[0]
                binfo = binfo + tmp + ', '

        name = raw_name.xpath('text()').extract()
        phone = raw_phone.xpath('text()').extract()
        address = raw_address.xpath('text()').extract()
        #times = raw_time.xpath('text()').extract()[0].strip().split('\n')

        time_string= ''

        times = raw_time.xpath('text()').extract()[0].strip().split('\n')
        time_flag = True
        for time in times:
            if time_flag == True:
                time_string = time_string + time
                time_flag = False
            else:
                time_string = time_string + ', ' + time

        tagwords = ''
        for tag in tags:
            word = tag.xpath('a/text()').extract()
            number = tag.xpath('text()').extract()
            keyword = word[0] + number[1]
            tagwords = tagwords + keyword + ',' + ' '

        tagwords = tagwords[0: len(tagwords) - 2]

        info(tagwords.encode('utf-8'))

        dpitem['name'] = name[0]
        dpitem['stars'] = stars[0]
        dpitem['binfo'] = binfo
        dpitem['phone'] = phone[0]
        dpitem['address'] = address[0]
        dpitem['time'] = time_string
        dpitem['labels'] = tagwords


        info("Append done")
        return dpitem



