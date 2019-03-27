# stock_data_crawler
This project is used to crawl stock related data for another project.[Sentiment Analysis in Event-Driven Stock Price Movement Prediction](https://github.com/WayneDW/Sentiment-Analysis-in-Event-Driven-Stock-Price-Movement-Prediction)



1. crawl ticker list from NASDAQ

```shell
python crawl_allTickers.py
python filter_good.py
```

2. crawl news headlines from Reuters

```shell
python main.py # this will run a scrapy crawler to get reuters news and save the data to mongodb
python save_news_to_csv.py # fetch news data from mongodb and save it to csv file
```
