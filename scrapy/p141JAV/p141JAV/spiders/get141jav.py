# -*- coding: utf-8 -*-
import scrapy
from p141JAV.items import PageinfoItem

class Get141javSpider(scrapy.Spider):
    name = 'get141jav'
    #  允许爬的根域名，在genspider时可以指定
    allowed_domains = ['www.141jav.com']
    #  爬虫入口地址，可以写多个
    start_urls = ['https://www.141jav.com/new']

    # 当框架请求start_urls内的链接成功以后，就会调用该方法
    def parse(self, response):
        # 提取链接，并提取
        # .extract() 返回的数据是一个列表
        links = response.xpath('//h5[@class="title is-4 is-spaced"]/a/@href').extract()
        for link in links:
            if not link.startswith('https://www.141jav.com'):
                link = 'https://www.141jav.com%s' % link
            # 让框架继续跟随链接，会再次发起请求``
            # 请求成功以后调用指定的callback函数

            request = response.follow(link, self.parse_page_info, dont_filter=True) # dont_filter用于不要过滤重复请求
            request.meta['test'] = 1
            yield request


    def parse_page_info(self,response):
        # response = response.replace(body=response.text.replace('\t','').replace('\r\n'),'') 去除特殊符号的方法
        # 将所有信息存储在一个字典里，方便后续使用
        print('test=========='),response.meta['test']
        data = {}
        item = PageinfoItem()
        # 不加extract_first返回的是一个selector。加了以后返回的是一个唯一值，按顺序提取
        data['title'] = response.xpath('normalize-space(.//h5[@class="title is-4 is-spaced"]/a/text())').extract_first() # 个人觉得这个方式去特殊符号更方便
        data['actress'] = response.xpath('.//a[@class="panel-block"]/text()').extract_first()
        data['magnet'] = response.xpath('.//a[@title="Magnet torrent"]/@href').extract_first()
        data['tag'] = response.xpath('normalize-space(string(//div[@class="tags"]))').extract_first()
        data['img'] = response.xpath('.//div[@class="column"]/img/@src').extract_first()
        # yield出的数据视为item，被框架接收，进行下一步处理
        # 如果没有任何处理，则会在console打印输出
        # 返回前进行操作
        item['av_code'] = data.get('title')
        item['actress'] = data.get('actress')
        item['tag'] = data.get('tag')
        item['magnet'] = data.get('magnet')
        item['img'] = data.get('img')
        yield item
