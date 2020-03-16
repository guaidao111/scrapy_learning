# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.exceptions import NotConfigured
import random


class P141JavSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class P141JavDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


# 设置IP代理池
# class RandomProxyMiddleWare(object):
#     def __init__(self, settings):
#         # 2.初始化配置和相关变量
#         self.proxies = settings.getlist('PROXIES')
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         #  1.调用函数创建中间件的对象
#         if not crawler.settings.getbool('HTTPPROXY_ENABLED'):
#             raise NotConfigured
#
#         return cls(crawler.settings)
#
#     def process_request(self, request, spider):
#         # 3.为每个request对象分配一个随机的IP代理
#         if not request.meta.get('proxy'):
#             request.meta['proxy'] = random.choice(self.proxies)
#
#     def process_response(self, request, response, spider):
#         # 4. 请求成功则调用process_response
#         return response
#
#     def process_exception(self, request, exception, spider):
#         # 5. 请求失败则调用process_exception
#         cur_proxy = request.meta.get('proxy')
#         from twisted.internet.error import ConnectionRefusedError, TimeoutError
#         if cur_proxy and isinstance(exception, (ConnectionRefusedError, TimeoutError)):
#             print('error (%s) occured when use proxy %s' % (exception,cur_proxy))
#             return request
