# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class StockDataCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class NewsItem(scrapy.Item):
    symbol = scrapy.Field()
    name = scrapy.Field()
    date = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    news_type = scrapy.Field()
