import pymongo
import csv


def reformat(datestr):
    return datestr[-4:] + datestr[:4]


csvfile = open('news_reuters.csv', 'w', encoding='utf-8', newline='')
writer = csv.writer(csvfile)
client = pymongo.MongoClient()
db = client.us
col_count = 0
news_count = 0
for col_name in sorted(db.collection_names()):
    col = db[col_name]
    col_count += 1
    print('processing ', col_name)
    for k in col.find():
        data = [k['symbol'], k['name'], reformat(k['date']), k['title'], k['content']]
        writer.writerow(data)
        news_count += 1
print(col_count, 'stocks, and', news_count, 'pieces of news')
csvfile.close()
