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


# 建立代码存储表（国内省）
country_code_url = "https://gwpre.sina.cn/interface/wap_api/feiyan/sinawap_get_area_tree.d.json"
country_code = requests.get(country_code_url,headers=headers).text
country_code = json.loads(country_code)
# 国内信息
province_info =  country_code['data']['cities_cn']
# 国外信息
foreign_info = country_code['data']['countries']

# 连接mysql服务器
conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='root',db='wordpress01',charset='utf8')
# 使用游标操作
cursor = conn.cursor()
city=[]
# 将省信息输入国家级别表格
for province in province_info:
    city.append(province['z'])
    # sql = "insert into country_id(`province_name`, `id`) values(%s, %s)"
    # cursor.execute(sql, (province['c'],province['e']))  # 将字典a传入
    # conn.commit()

def flatten(ll):
  """
  功能:用递归方法展开多层列表,以生成器方式输出
  """
  if isinstance(ll, list):
    for i in ll:
      for element in flatten(i):
        yield element
  else:
    yield ll
city_list = list(flatten(city))

# 将市信息输入市级别表格


for i in city_list:
    sql = "insert into city_id(`city_name`, `id`) values(%s, %s)"
    cursor.execute(sql, (i['c'],i['i']))  # 将字典a传入
    conn.commit()

foreign_info
for i in foreign_info:
    print(i)

for i in foreign_info:
    sql = "insert into country_id(`province_name`,`id`) values(%s, %s)"
    cursor.execute(sql, (i['c'],i['i']))  # 将字典a传入
    conn.commit()

cursor.close()
conn.close()
