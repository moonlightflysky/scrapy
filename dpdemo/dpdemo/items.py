# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class DpdemoItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = Field()
    stars = Field()
    binfo = Field()
    phone = Field()
    address = Field()
    time = Field()
    labels = Field()
