import time
import requests
from bs4 import BeautifulSoup
from lxml import etree
import pandas as pd

start_url = 'https://pt.m-team.cc/adult.php?cat=410'
download_pages = 0
# 代码太复杂，用fetch方法进行重构,专门解决数据的抓取问题
def fetch(url):
    proxies = {
        'http':'http://108.160.140.140:35011'
    }
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
        'Cookie':'tp=ZjIyZGE5ZGMyMzc5YjgyNWYxZmE4NTk1NjlkMDI4NzY4MGE1OGVlOA%3D%3D; __cfduid=d2e5fee0ab9f9835b2112b6b151ede7e91581746087'
    }
    r = requests.get(url,headers=headers,proxies=proxies)
    if r.status_code !=200:
        r.raise_for_status()
    global download_pages
    download_pages += 1
    return r.text.replace(u'\xa0',u' ')

# 将解析过程定义为一个函数, 负责解析详情页面的数据
def parse_page_info(url):
    detail_selector = etree.HTML(fetch(url))
    # 将所有信息存储在一个字典里，方便后续使用
    data = {}
    data['title'] = detail_selector.xpath('//h1/text()[1]')[0] #获取到的是一个列表，因此取列表的第一个元素
    # 由于某些td下存在多个a或其他类型标签，导致键值对数目不等，以下为笨办法，通过自行定义每一个对应的xpath解决
    # data['info'] = detail_selector.xpath('//td[@class="rowfollow"]/text()')[3]
    # data['actor'] = detail_selector.xpath('//td[@class="rowfollow"]/a/b/text()')[0]
    # data['tag'] = detail_selector.xpath('//td[@class="rowfollow"]/a[contains(@href, "adult.php")]/b/text()')
    # data['size'] = detail_selector.xpath('//td[contains(text(),"基本資訊")]/following::*[1]/text()')
    # data['torrentlinkV6'] = detail_selector.xpath('//a[contains(text(),"[IPv6+https]")]/@href')
    # data['ReleaseDate'] = detail_selector.xpath('//td[contains(text(),"発売日：")]/following::*[1]/text()')
    # data['Maker'] = detail_selector.xpath('//a[contains(@href,"dmmlist.php?label")]/text()')
    # data['profile'] = detail_selector.xpath('//div[@class="dmm_text"]/text()')
    # 更好的方法是通过一个循环的方式来解决
    keys = detail_selector.xpath('//td[contains(@class,"rowhead")]/text()')
    cols = detail_selector.xpath('//td[contains(@class,"rowfollow") and not(div[contains(@id,"kdescr")])]') # 用于提取子节点中包含指定class不包含指定div的td
    values = [''.join(col.xpath('.//text()')) for col in cols] # for循环简化为一行表达，将一个td中具有多个a标签的text进行合并
    # for i in range(len(keys)):
    #     data[keys[i]] = values[i]
    # 简化为下面的方式，zip是将多个元素进行打包成元组，返回元组组成的list的操作
    data.update(zip(keys, values))
    return data

def process_data(data):
     # 处理数据
     if data:
         print(data)


if __name__ == '__main__':
    start_time = time.time()
    # 请求入口页面
    selector = etree.HTML(fetch(start_url))
    # 解析页面text，获取对应的每个页面的link
    links = selector.xpath('//form[@id="form_torrent"]//td[@class="torrentimg"]/following::*[1]/a/@href')
    # 由于网站的链接为去掉前面的部分，需手动加上https://pt.m-team.cc/
    weblink = "https://pt.m-team.cc/"
    reallink = list(map(lambda x:weblink + x, links))
    for link in reallink:
        data = parse_page_info(link)
        process_data(data)
    cost_seconds = time.time() - start_time # 计算下载时间
    print('download %s pages, cost %.2f seconds' %
    (download_pages, cost_seconds))
