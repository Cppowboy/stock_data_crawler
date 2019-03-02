import scrapy
from bs4 import BeautifulSoup
import pymongo
import datetime
from ..items import NewsItem
import logging
import csv
import time
import random


class ReutersNewsSpider(scrapy.Spider):
    name = 'newsspider'
    suffix = {'AMEX': '.A', 'NASDAQ': '.O', 'NYSE': '.N'}
    url = "https://www.reuters.com/finance/stocks/company-news/{0}{1}?date={2}"
    custom_settings = {
        'ITEM_PIPELINES': {
            'stock_data_crawler.pipelines.NewsPipeline': 300
        }
    }
    collection = pymongo.MongoClient().us.stocklist

    def start_requests(self):
        stocklist = []
        # for i in self.collection.find().sort('Symbol', pymongo.ASCENDING):
        #     stocklist.append(dict(i))
        with open('tickerList.csv') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                stocklist.append(row)
        print('There are {} stocks'.format(len(stocklist)))
        for i in stocklist:
            try:
                symbol = i[0]
                exchange = i[2]
                name = i[1]
                start = datetime.date(year=2015, month=1, day=1)
                one_day = datetime.timedelta(days=1)
                end = datetime.date.today()
                while end >= start:
                    datestr = end.strftime('%m%d%Y')
                    urlstr = self.url.format(symbol, self.suffix[exchange], datestr)
                    yield scrapy.Request(url=urlstr, meta={'symbol': symbol, 'name': name, 'date': datestr})
                    end -= one_day
            except Exception as e:
                logging.error(e, i)

    def parse(self, response):
        symbol = response.meta.get('symbol')
        name = response.meta.get('name')
        datestr = response.meta.get('date')
        soup = BeautifulSoup(response.body, 'lxml')
        content = soup.find_all("div", {'class': ['topStory', 'feature']})
        if len(content) <= 0:
            return
        for i in range(len(content)):
            item = NewsItem()
            item['symbol'] = symbol
            item['name'] = name
            item['date'] = datestr
            item['title'] = content[i].h2.get_text().replace(",", " ").replace("\n", " ")
            item['content'] = content[i].p.get_text().replace(",", " ").replace("\n", " ")
            if i == 0 and len(soup.find_all("div", class_="topStory")) > 0:
                item['news_type'] = 'topStory'
            else:
                item['news_type'] = 'normal'
            yield item
        time.sleep(random.randint(5, 10))
