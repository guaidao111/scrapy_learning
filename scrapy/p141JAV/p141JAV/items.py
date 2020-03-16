# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

#  定义一个类
class PageinfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    av_code = scrapy.Field()
    actress = scrapy.Field()
    tag = scrapy.Field()
    magnet = scrapy.Field()
    img = scrapy.Field()
