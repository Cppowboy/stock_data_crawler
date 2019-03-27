#!/usr/bin/env python
# coding=utf-8
import csv  

fin = open('all_tickerList.csv')
reader = csv.reader(fin)
data = [row for row in reader]
data = sorted(data, key = lambda x: float(x[-1]), reverse=True)
fout = open('tickerList.csv', 'w')
writer = csv.writer(fout)
for item in data[:100]:
    print(item)
    writer.writerow(item)

