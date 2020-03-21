import time
import json
import requests
import pymysql
from collections import OrderedDict


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
}

def get_urls():
    # 连接mysql服务器
    conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='root',db='wordpress01',charset='utf8')
    # 使用游标操作,获取城市及国家ID
    cursor = conn.cursor()
    cursor.execute('SELECT id from city_id')
    city_id = cursor.fetchall()
    cursor.execute('SELECT id from country_id where id not like "SC%"')
    province_id = cursor.fetchall()
    cursor.execute('SELECT id from country_id where id like "SC%"')
    country_id = cursor.fetchall()
    #关闭游标
    cursor.close()
    #关闭连接
    conn.close()

    # city代码也可去country_code获取
    city_urls = []
    for city_code in city_id:
        city_urls.append("https://gwpre.sina.cn/interface/news/wap/fymap2020_citydata.d.json?citycode=%s" % (city_code))
    # 中国省份和市号码也在country_code中可以获取，但是网址不同
    province_urls = []
    for province_code in province_id:
        province_urls.append("https://gwpre.sina.cn/interface/news/wap/historydata.d.json?province=%s" % (province_code))
    # 世界国家层级
    country_urls = []
    for country_code in country_id:
        country_urls.append("https://gwpre.sina.cn/interface/news/wap/ncp_foreign.d.json?citycode=%s" % (country_code))
    print('URL获取成功')
    return city_urls, province_urls, country_urls


# map_url = "https://finance.sina.com.cn/other/src/%s_map.js" % (country)

def delete_last_entry():
    conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='root',db='wordpress01',charset='utf8')
    # 使用游标操作
    cursor = conn.cursor()
    delete = """DELETE FROM country_info"""
    cursor.execute(delete)
    delete = """DELETE FROM country_history"""
    cursor.execute(delete)
    delete = """DELETE FROM foreign_country_info"""
    cursor.execute(delete)
    delete = """DELETE FROM foreign_country_history"""
    cursor.execute(delete)
    conn.commit()
    #关闭游标
    cursor.close()
    #关闭连接
    conn.close()
    print('数据库初始化完成')

def parse_city_info(city_urls):
    city_info_list = []
    city_history_list = []
    for city_url in city_urls:
        r = requests.get(city_url,headers=headers).text
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

    # 连接mysql服务器
    conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='root',db='wordpress01',charset='utf8')
    # 使用游标操作
    cursor = conn.cursor()
    sql = "INSERT INTO country_info(`datetime`, `province`, `city`,`type`,`total`,`deathtotal`,`sustotal`,`curetotal`,`remain`,`connadd`,`deathadd`,`cureadd`) values(%s, %s,%s,%s, %s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.executemany(sql,city_info_list)
    conn.commit()
    sql = "INSERT INTO country_history(`datetime`,`province`,`city`,`type`,`total`,`connadd`,`curetotal`,`deathtotal`,`remain`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.executemany(sql,city_history_list)
    conn.commit()
    #关闭游标
    cursor.close()
    #关闭连接
    conn.close()
    print('city info和history插入完成')

def parse_province_url(province_urls):
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

    # 连接mysql服务器
    conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='root',db='wordpress01',charset='utf8')
    # 使用游标操作
    cursor = conn.cursor()
    sql = "INSERT INTO country_info(`datetime`, `province`, `city`,`type`,`total`,`deathtotal`,`sustotal`,`curetotal`,`remain`,`connadd`,`deathadd`,`cureadd`) values(%s, %s,%s,%s, %s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.executemany(sql,province_info_list)
    conn.commit()

    sql = "INSERT INTO country_history(`datetime`,`province`,`city`,`type`,`total`,`connadd`,`curetotal`,`deathtotal`,`remain`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.executemany(sql,province_history_list)
    conn.commit()
    #关闭游标
    cursor.close()
    #关闭连接
    conn.close()
    print('province info和history插入完成')


def parse_country_url(country_urls):
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

    #关闭游标
    cursor.close()
    #关闭连接
    conn.close()
    print('foreign country info和history插入完成')
    return country_info_list


if __name__ == '__main__':
        urls = get_urls()
        delete_last_entry()
        parse_city_info(urls[0])
        parse_province_url(urls[1])
        parse_country_url(urls[2])
        print("数据更新完成")
