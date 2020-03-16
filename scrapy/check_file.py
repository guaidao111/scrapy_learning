# 打开json文件
import json
quotes = json.load(open(r'C:\Users\aragorn\Desktop\python\web scrawper\Scrapy\quotes.json'))
for quote in quotes:
    print(quote['ID'],quote['Magnet'],quote['Torrent'])
