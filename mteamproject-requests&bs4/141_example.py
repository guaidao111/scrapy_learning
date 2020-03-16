# 这样的请求效率太低，尝试用多线程的方式优化,分布式
# 需要将数据做成队列的形式
import time
import requests
from queue import Queue
from bs4 import BeautifulSoup
from lxml import etree


start_url = 'https://www.141jav.com/new'
# create a Queue对象
download_pages = 0

def fetch(url):
    r = requests.get(url)
    if r.status_code !=200:
        r.raise_for_status()
    global download_pages    # 设定为全局变量以通用使用
    download_pages +=1  # 每完成一次下载自动计数+1
    return r.text


def process_data(data):
     # 处理数据
     if data:
         print(data)


def parse_page_info(url):
    detail_selector = etree.HTML(fetch(url))
    # 将所有信息存储在一个字典里，方便后续使用
    data = {}
    data['title'] = detail_selector.xpath('normalize-space(.//h5[@class="title is-4 is-spaced"]/a/text())')
    data['actress'] = detail_selector.xpath('.//a[@class="panel-block"]/text()')
    data['magnet'] = detail_selector.xpath('.//a[@title="Magnet torrent"]/@href')
    data['tag'] = detail_selector.xpath('normalize-space(string(//div[@class="tags"]))')
    return data

if __name__ == '__main__':
    start_time = time.time() # 设定初始时间
    # 请求入口页面
    selector = etree.HTML(fetch(start_url))
    # 解析页面text，获取对应的每个页面的link
    links = selector.xpath('//h5[@class="title is-4 is-spaced"]/a/@href')
    for link in links:
        if not link.startswith('https://www.141jav.com'):
            link = 'https://www.141jav.com%s' % link
            data = parse_page_info(link)
            process_data(data)
    cost_seconds = time.time() - start_time # 计算下载时间
    print('download %s pages, cost %.2f seconds' %
    (download_pages, cost_seconds))
