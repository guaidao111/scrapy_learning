import time
import json
import requests
import pymysql
from lxml import etree

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
}


cninfo = requests.get("https://interface.sina.cn/news/fy.daily.d.json",headers=headers).text
foreigninfo = requests.get("https://gwpre.sina.cn/ncp/foreign",headers=headers).text
cninfo = json.loads(cninfo)
foreigninfo = json.loads(foreigninfo)
foreign_current = foreigninfo['result']['total']
foreign_total = foreign_current['certain']
foreign_death = foreign_current['die']
foreign_cure = foreign_current['recure']
foreign_add = foreign_current['certain_inc']
foreign_deathadd = foreign_current['die_inc']
foreign_cureadd = foreign_current['recure_inc']
foreign_total = foreign_current['certain']
cninfo = cninfo['data'][0]
datetime = cninfo['title']
cn_total = cninfo['cn_conNum']
cn_death = cninfo['cn_deathNum']
cn_cure = cninfo['cn_cureNum']
cn_add = cninfo['cn_conNum_add']
cn_deathadd = cninfo['cn_deathNum_add']
cn_cureadd = cninfo['cn_cureNum_add']

world_total = int(cn_total) + int(foreign_total)
world_death = int(cn_death) + int(foreign_death)
world_cure = int(cn_cure) + int(foreign_cure)
world_add = int(cn_add) + int(foreign_add)
world_deathadd = int(cn_deathadd) + int(foreign_deathadd)
world_cureadd = int(cn_cureadd) + int(foreign_cureadd)
info_list = [datetime, world_total, world_death,world_cure,world_add,world_deathadd,world_cureadd,cn_total, cn_death,cn_cure,cn_add,cn_deathadd,cn_cureadd]
info_list



# 连接mysql服务器
conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='root',db='wordpress01',charset='utf8')
# 使用游标操作
cursor = conn.cursor()
sql = "INSERT INTO front_page_info(`datetime`, `world_total`, `world_death`,`world_cure`,`world_add`,`world_deathadd`,`world_cureadd`,`cn_total`, `cn_death`,`cn_cure`,`cn_add`,`cn_deathadd`,`cn_cureadd`) values(%s, %s,%s,%s, %s,%s,%s,%s,%s,%s,%s,%s,%s)"
cursor.execute(sql,info_list)
conn.commit()
cursor.close()
#关闭连接
conn.close()
print('front_page插入完成')
