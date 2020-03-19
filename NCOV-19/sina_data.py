import time
import json
import requests
from lxml import etree
import pymysql
from bs4 import BeautifulSoup
import pymysql

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

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
}
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
for city_url in city_urls:
    r = requests.get(world_url,headers=headers).text
    if r.status_code !=200:
        r.raise_for_status()
    result = json.loads(r)



# 中国省份和市号码也在country_code中可以获取，但是网址不同

world_url = "https://gwpre.sina.cn/interface/news/wap/ncp_foreign.d.json?citycode=%s" % (country)
map_url = "https://finance.sina.com.cn/other/src/%s_map.js" % (country)


def parse(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
    }
    try:
        r = requests.get(url,headers=headers).text
    except:
        print('网页获取失败')
    result = json.loads(r)
    data = {}
    data['datetime'] = result




if __name__ == '__main__':
    for city_url in city_urls:
         parse(city_url)

















# province代码就是拼音，可在country_code的e=进行遍历获取
cn_province_url = "https://gwpre.sina.cn/interface/news/wap/historydata.d.json?province=%s" % (province_code)



# 国外当前数据及历史总数趋势
foreign_url = "https://gwpre.sina.cn/ncp/foreign"

# 中国当前及历史数据趋势
cn_url = "https://gwpre.sina.cn/interface/fymap2020_data.json"
