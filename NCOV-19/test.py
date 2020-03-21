import time
import json
import requests
from lxml import etree
import pymysql
from bs4 import BeautifulSoup
import pymysql
from collections import OrderedDict


# 连接mysql服务器
conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='root',db='wordpress01',charset='utf8')
# 使用游标操作
cursor = conn.cursor()
cursor.execute('select id from city_id')
city_id = cursor.fetchall()
# city代码也可去country_code获取
city_urls = []
for city_code in city_id:
    city_urls.append("https://gwpre.sina.cn/interface/news/wap/fymap2020_citydata.d.json?citycode=%s" % (city_code))
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
}
city_urls
city_info_list = []
city_history_list = []
for city_url in city_urls:
    try:
        r = requests.get(city_url,headers=headers).text
    except:
        print("网页获取失败")
    result = json.loads(r)
    data = (result['data']['times'],result['data']['province'],result['data']['city'],'市级',
    result['data']['contotal'],result['data']['deathtotal'],
    result['data']['sustotal'],result['data']['curetotal'],result['data']['econNum'],
    result['data']['adddaily']['conadd_n'],result['data']['adddaily']['deathadd_n'],result['data']['adddaily']['cureadd_n'])
    history_lists = result['data']['historylist']
    province_name = result['data']['province']
    city_name = result['data']['city']
    city_info_list.append(data)
    for history in history_lists:
        d = OrderedDict()
        d['datetime'] = history['date']
        d['province'] = province_name
        d['city'] = city_name
        d['type'] = '市级'
        d['total'] = history['conNum']
        d['add'] = history['conadd']
        d['cure'] = history['cureNum']
        d['death'] = history['deathNum']
        d['remain'] =history['econNum']
        city_history_list.append(tuple(d.values()))
city_info_list
city_history_list

# 连接mysql服务器
conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='root',db='wordpress01',charset='utf8')
# 使用游标操作
cursor = conn.cursor()
# 删除要一次性把所有表都清空再重新加入，目前对于更新的方法比较有问题，后续要研究下怎么处理。
delete = """DELETE FROM country_info"""
cursor.execute(delete)
conn.commit()
sql = "INSERT INTO country_info(`datetime`, `province`, `city`,`type`,`total`,`deathtotal`,`sustotal`,`curetotal`,`remain`,`connadd`,`deathadd`,`cureadd`) values(%s, %s,%s,%s, %s,%s,%s,%s,%s,%s,%s,%s)"
cursor.executemany(sql,city_info_list)
conn.commit()
delete = """DELETE FROM country_history"""
cursor.execute(delete)
conn.commit()
sql = "INSERT INTO country_history(`datetime`,`province`,`city`,`type`,`total`,`connadd`,`curetotal`,`deathtotal`,`remain`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
cursor.executemany(sql,city_history_list)
conn.commit()
#关闭游标
cursor.close()
#关闭连接
conn.close()





cursor.execute('SELECT id from country_id where id not like "SC%"')
province_id = cursor.fetchall()
cursor.execute('SELECT id from country_id where id like "SC%"')
country_id = cursor.fetchall()


province_urls = []
for province_code in province_id:
    province_urls.append("https://gwpre.sina.cn/interface/news/wap/historydata.d.json?province=%s" % (province_code))
province_urls
province_info_list=[]
province_history_list=[]
for province_url in province_urls:
    r = requests.get(province_url,headers=headers).text
    result = json.loads(r)
    # 多加1个result['data']['province']用于填充city信息,后续同一张表里用type字段区分提取。
    data = (result['data']['times'],result['data']['province'],result['data']['province'],'省级',
    result['data']['contotal'],result['data']['deathtotal'],
    result['data']['sustotal'],result['data']['curetotal'],result['data']['econNum'],
    result['data']['adddaily']['conadd_n'],result['data']['adddaily']['deathadd_n'],result['data']['adddaily']['cureadd_n'])
    province_info_list.append(data)
    province_name = result['data']['province']
    history_lists = result['data']['historylist']
    for history in history_lists:
        d = OrderedDict()
        d['datetime'] = history['date']
        d['province'] = province_name
        d['city'] = province_name
        d['type'] = '省级'
        d['total'] = history['conNum']
        d['add'] = history['conadd']
        d['cure'] = history['cureNum']
        d['death'] = history['deathNum']
        d['remain'] =history['econNum']
        province_history_list.append(tuple(d.values()))

sql = "INSERT INTO country_info(`datetime`, `province`, `city`,`type`,`total`,`deathtotal`,`sustotal`,`curetotal`,`remain`,`connadd`,`deathadd`,`cureadd`) values(%s, %s,%s,%s, %s,%s,%s,%s,%s,%s,%s,%s)"
cursor.executemany(sql,province_info_list)
conn.commit()

sql = "INSERT INTO country_history(`datetime`,`province`,`city`,`type`,`total`,`connadd`,`curetotal`,`deathtotal`,`remain`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
cursor.executemany(sql,province_history_list)
conn.commit()



# 世界国家层级
country_urls = []

for country_code in country_id:
    country_urls.append("https://gwpre.sina.cn/interface/news/wap/ncp_foreign.d.json?citycode=%s" % (country_code))
country_info_list=[]
country_history_list=[]
foreign_city_info_list=[]
for country_url in country_urls:
    r = requests.get(country_url,headers=headers).text
    result = json.loads(r)
    # 多加1个result['data']['province']用于填充city信息,后续同一张表里用type字段区分提取。
    data = (result['data']['times'],result['data']['country'],result['data']['country'],'外国国家',
    result['data']['contotal'],result['data']['deathtotal'],result['data']['curetotal'],
    result['data']['adddaily']['conadd_n'],result['data']['adddaily']['deathadd_n'],result['data']['adddaily']['cureadd_n'])
    country_info_list.append(data)
    country_name = result['data']['country']
    history_lists = result['data']['historylist']
    for history in history_lists:
        d = OrderedDict()
        d['date'] = history['date']
        d['country'] = country_name
        d['type'] = '外国国家'
        d['total'] = history['conNum']
        d['add'] = history['conadd']
        d['cure'] = history['cureNum']
        d['death'] = history['deathNum']
        country_history_list.append(tuple(d.values()))
    if result['data']['city'] is not None:
        city_lists = result['data']['city']
    for city in city_lists:
            c = OrderedDict()
            c['date'] = result['data']['times']
            c['country'] = country_name
            c['city'] = city['name']
            c['type'] = '外国城市'
            c['total'] = city['conNum']
            c['deathtotal'] = city['deathNum']
            c['curetotal'] = city['cureNum']
            c['add'] = city['conadd']
            c['death'] = city['deathadd']
            c['cure'] = city['cureadd']
            foreign_city_info_list.append(tuple(c.values()))
country_info_list
country_history_list
foreign_city_info_list

# 连接mysql服务器
conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='root',db='wordpress01',charset='utf8')
# 使用游标操作
cursor = conn.cursor()

sql = "INSERT INTO foreign_country_info(`date`,`country`,`city`,`type`,`total`,`deathtotal`,`curetotal`,`connadd`,`deathadd`,`cureadd`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
cursor.executemany(sql,country_info_list)
conn.commit()

sql = "INSERT INTO foreign_country_history(`date`,`country`,`type`,`total`,`connadd`,`curetotal`,`deathtotal`) values(%s,%s,%s,%s,%s,%s,%s)"
cursor.executemany(sql,country_history_list)
conn.commit()

sql = "INSERT INTO foreign_country_info(`date`,`country`,`city`,`type`,`total`,`deathtotal`,`curetotal`,`connadd`,`deathadd`,`cureadd`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
cursor.executemany(sql,foreign_city_info_list)
conn.commit()
