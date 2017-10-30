#!/usr/bin/python
from urllib import request
import csv
import sys
import numpy as np
import pymongo


def getTickers(percent):
    # file = open('./tickerList.csv', 'w')
    # writer = csv.writer(file, delimiter=',')
    capStat, output = np.array([]), []
    fields = None
    for exchange in ["NASDAQ", "NYSE", "AMEX"]:
        url = "http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange="
        repeat_times = 10  # repeat downloading in case of http error
        for _ in range(repeat_times):
            try:
                print("Download tickers from " + exchange)
                response = request.urlopen(url + exchange + '&render=download')
                content = response.read().decode('utf-8').split('\n')
                for num, line in enumerate(content):
                    line = line.strip().strip('"').split('","')
                    if num == 0: fields = line
                    if num == 0 or len(line) != 9: continue  # filter unmatched format
                    ticker, name, lastSale, MarketCap, IPOyear, sector, \
                    industry = line[0: 4] + line[5: 8]
                    capStat = np.append(capStat, float(MarketCap))
                    output.append([ticker, name.replace(',', '').replace('.', ''), exchange, MarketCap])
                break
            except:
                continue
    collection = pymongo.MongoClient().us.stocklist
    for data in output:
        marketCap = float(data[3])
        if marketCap < np.percentile(capStat, 100 - percent): continue
        # writer.writerow(data)
        d = dict(zip(fields, data))
        collection.update({'Symbol': d['Symbol']}, d, upsert=True)


def main():
    percent = 100
    s = getTickers(percent)  # keep the top N% market-cap companies


if __name__ == "__main__":
    main()
