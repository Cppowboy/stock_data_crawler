# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .items import NewsItem
import pymongo


class StockDataCrawlerPipeline(object):
    def process_item(self, item, spider):
        return item


class NewsPipeline(object):
    def process_item(self, item, spider):
        item = dict(item)
        collection = pymongo.MongoClient().us[item['symbol']]
        collection.update({'date': item['date'], 'title': item['title']}, item, upsert=True)
        return item
