# 这样的请求效率太低，尝试用多线程的方式优化
# 需要将数据做成队列的形式
import time
import requests
import threading
from queue import Queue
from bs4 import BeautifulSoup
from lxml import etree
import pandas as pd

start_url = 'https://pt.m-team.cc/adult.php?cat=410'
# create a Queue对象
link_queue = Queue()
threads = [] # 定义一个列表作为线程池
threads_num = 10 # 定义线程数量
download_pages = 0 # 初始化下载页面数

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
    global download_pages    # 设定为全局变量以通用使用
    download_pages +=1  # 每完成一次下载自动计数+1
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

def download():
    # 保持线程持续工作，不让其自动销毁,直到完成任务
    while True:
        link = link_queue.get()
        if link is None:  # 如果队列中的link没有了自动结束任务。
            break
        data = parse_page_info(link) # 将队列的link传入解析模块，返回data
        process_data(data)  # 调用处理模块
        link_queue.task_done() # 告诉队列完成了这个任务，进行下一个
        print('remaining queue: %s' % link_queue.qsize())  # 显示剩余任务量



if __name__ == '__main__':
    start_time = time.time() # 设定初始时间
    # 请求入口页面
    selector = etree.HTML(fetch(start_url))
    # 解析页面text，获取对应的每个页面的link
    links = selector.xpath('//form[@id="form_torrent"]//td[@class="torrentimg"]/following::*[1]/a/@href')
    # 由于网站的链接为去掉前面的部分，需手动加上https://pt.m-team.cc/
    weblink = "https://pt.m-team.cc/"
    reallink = list(map(lambda x:weblink + x, links))
    for link in reallink:
        link_queue.put(link) # 循环方式向队列中添加link
        # data = parse_page_info(link)
        # process_data(data)

    # 创建一个多线程函数,并将线程对象放入一个列表保存
    for i in range(threads_num):
        t = threading.Thread(target=download)
        t.start() # 启动线程
        threads.append(t)
    # 阻塞住队列，直到清空队列
    link_queue.join()
    # 向队列发送n个None，以通知线程退出
    for i in range(threads_num):
        link_queue.put(None)
    # 退出线程
    for t in threads:
        t.join()
    # 计算下载时间
    cost_seconds = time.time() - start_time
    print('download %s pages, cost %.2f seconds' %
    (download_pages, cost_seconds))
