# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ShopsItem(Item):
    shop_name = Field()
    street_address = Field()
    shop_tags = Field()
    shop_dianping_url = Field()
    shop_city = Field()
    shop_district = Field()
    shop_region = Field()
    shop_category = Field()
    shop_tel = Field()
    open_time = Field()
    shop_tag = Field()
    location = Field()
    id = Field()
    shop_star = Field()
    review_num = Field()
    individual_cost = Field()
    shop_taste = Field()
    shop_environment = Field()
    shop_service = Field()
    branches = Field()
    recommend_dishes = Field()