import scrapy
from bs4 import BeautifulSoup
import pymongo
import datetime
from ..items import NewsItem


class ReutersNewsSpider(scrapy.Spider):
    name = 'newsspider'
    suffix = {'AMEX': '.A', 'NASDAQ': '.O', 'NYSE': '.N'}
    url = "https://www.reuters.com/finance/stocks/company-news/{0}{1}?date={2}"
    custom_settings = {
        'ITEM_PIPELINES': {
            'stock_data_crawler.pipelines.NewsPipeline': 300
        }
    }

    def start_requests(self):
        collection = pymongo.MongoClient().us.stocklist
        for i in collection.find().sort('Symbol', pymongo.ASCENDING):
            symbol = i['Symbol']
            exchange = i['Exchange']
            name = i['Name']
            start = datetime.date(year=2004, month=1, day=1)
            one_day = datetime.timedelta(days=1)
            end = datetime.date.today()
            while end >= start:
                datestr = end.strftime('%m%d%Y')
                urlstr = self.url.format(symbol, self.suffix[exchange], datestr)
                yield scrapy.Request(url=urlstr, meta={'symbol': symbol, 'name': name, 'date': datestr})
                end -= one_day

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
