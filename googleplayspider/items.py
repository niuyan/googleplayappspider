# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GoogleplayspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = Field()
    Name = scrapy.Field()
    Icon = scrapy.Field()
    Link = scrapy.Field()
    Last_updated = scrapy.Field()
    Author = scrapy.Field()
    Size = scrapy.Field()
    Installs = scrapy.Field()
    Version = scrapy.Field()
    OS = scrapy.Field()
    Content_rating = scrapy.Field()
    Genre = scrapy.Field()
    Price = scrapy.Field()
    Review_rating = scrapy.Field()
    Review_number = scrapy.Field()
    Description = scrapy.Field()
    Developer = scrapy.Field()
    Offeredby = scrapy.Field()
    Interactive_elements = scrapy.Field()
