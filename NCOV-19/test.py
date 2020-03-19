import time
import json
import requests
from lxml import etree
import pymysql
from bs4 import BeautifulSoup
import pymysql


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
}
try:
    r = requests.get('https://gwpre.sina.cn/interface/news/wap/historydata.d.json?province=shanghai',headers=headers).text
except:
    print('网页获取失败')
result = json.loads(r)
result
data = {}
data['datetime'] = result['data']['times']
data['province'] = result['data']['province']
data['total'] = result['data']['contotal']
data['deathtotal'] = result['data']['deathtotal']
# 以下3个参数为数字型
data['add'] = result['data']['adddaily']['conadd_n']
data['deathadd'] = result['data']['adddaily']['deathadd_n']
data['cureadd'] = result['data']['adddaily']['cureadd_n']
data['remain'] = result['data']['econNum']

# data
# date = []
# conNum = []
# cureNum=[]
# deathNum=[]
# remainNum=[]
# history_list = result['data']['historylist']
# for his in history_list:
#     date.append(his['date'])
#     conNum.append(his['conNum'])
#
# print(key)
# print(value)
# data['history_n'] = dict(zip(key,value))
