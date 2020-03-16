import requests
from bs4 import BeautifulSoup
from lxml import etree

proxies = {
    'http':'http://108.160.140.140:35011'
}
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
    'Cookie':'tp=ZjIyZGE5ZGMyMzc5YjgyNWYxZmE4NTk1NjlkMDI4NzY4MGE1OGVlOA%3D%3D; __cfduid=d2e5fee0ab9f9835b2112b6b151ede7e91581746087'
}
resp = requests.get('https://pt.m-team.cc/details.php?id=385857&hit=1',headers=headers,proxies=proxies)
result = resp.text.replace('\xa0',' ')
result
selector = etree.HTML(resp.text.encode('utf-8'))

info = selector.xpath('//div[@class="dmm_text"]/text()')
info
