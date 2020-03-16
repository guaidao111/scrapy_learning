# -*- coding: utf-8 -*-

import re
import random
import string
import scrapy
from scrapy import Request
import json
from xpc.items import ComposerItem, PostItem, CommentItem,CopyrightItem
from scrapy_redis.spiders import RedisSpider


def convert_int(s):
    if isinstance(s, str):
        return int(s.replace(',', ''))
    return 0


cookies = dict(
Authorization='2F065A186B15C8A336B15C4A9E6B15C96016B15CDAC050644E60'
)


def gen_sessionid():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=26))


class DiscoverySpider(RedisSpider):
    name = 'discovery'
    allowed_domains = ['xinpianchang.com','openapi-vtom.vmovier.com','app.xinpianchang.com']
    # start_urls = ['https://www.xinpianchang.com/channel/index/sort-like?from=navigator']
    page_count = 0



    def parse(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        self.page_count +=1
        if self.page_count >= 10:
            cookies.update(PHPSESSID = gen_sessionid(), channel_page = 'apU%3D')
            self.page_count = 0
        post_list = response.xpath('//ul[@class="video-list"]/li')
        url = "https://www.xinpianchang.com/a%s?from=ArticleList"
        for post in post_list:
            pid = post.xpath('./@data-articleid').get()
            request = response.follow(url % pid, self.parse_post)
            request.meta['pid'] = pid
            request.meta['thumbnail'] = post.xpath('./a/img/@_src').get()
            yield request
        pages = response.xpath('//div[@class="page"]/a/@href').extract()
        for page in pages:
            yield response.follow(page, self.parse, cookies = cookies)


    # 解析获取的页面的link
    def parse_post(self, response):
        pid = response.meta['pid']
        post = PostItem(pid=pid)
        post['thumbnail'] = response.meta['thumbnail']
        post['title'] = response.xpath('//div[@class="title-wrap"]/h3/text()').get()
        # 由于视频的地址也是动态加载的，分析请求方式后发现请求url
        # 使用shell测试后得出正则表达式获取一个list形式返回的vid因此加逗号获取
        vid, = re.findall('vid: \"(\w+)",',response.text)
        video_url = 'https://openapi-vtom.vmovier.com/v3/video/%s?expand=resource&usage=xpc_web'
        # cates = response.xpath('//span[contains(@class,"cate v-center")]//text()').extract()
        post['category'] = response.xpath('normalize-space(string(//span[@class="cate v-center"]))').extract()
        post['created_at'] = response.xpath('//span[@class="update-time v-center"]/i/text()').get()
        post['play_counts'] = convert_int(response.xpath('//i[contains(@class,"play-counts")]/@data-curplaycounts').get())
        post['like_counts'] = convert_int(response.xpath('//span[contains(@class,"like-counts")]/@data-counts').get())
        post['description'] = response.xpath('normalize-space(string(//p[contains(@class,"desc")]))').get()
        # post[''] = response.xpath('').get()
        # post[''] = response.xpath('').get()
        # post[''] = response.xpath('').get()
        # post[''] = response.xpath('').get()
        request = Request(video_url % vid, callback=self.parse_video) # 解析视频接口模块回调该视频请求url，不是视频地址，里面包含了视频地址
        request.meta['post'] = post  # 通过meta把包含title信息的post传递出去
        yield request

        # 设置页面评论部分的url
        comment_url = 'https://app.xinpianchang.com/comments?resource_id=%s&type=article&page=1&per_page=24'
        request = Request(comment_url % pid, callback=self.parse_comment)
        request.meta['pid'] = pid
        yield request

        # 获取制作人信息
        creator_list = response.xpath('//div[@class="filmplay-creator right-section"]/ul/li')
        composer_url = 'https://www.xinpianchang.com/u%s?from=articleList'
        for creator in creator_list:
            cid = creator.xpath('./a/@data-userid').get()
            request = response.follow(composer_url % cid, self.parse_composer)
            request.meta['cid'] = cid
            request.meta['dont_merge_cookies'] = True
            yield request

            cr = CopyrightItem()
            cr['pcid'] = '%s_%s' % (pid, cid)
            cr['pid'] = pid
            cr['cid'] = cid
            cr['roles'] = creator.xpath('./div[@class="creator-info"]/span/text()').get()
            yield cr


    #  解析视频接口(包括视频的封面也在这里获取)
    def parse_video(self, response):
        post = response.meta['post']
        # 由于该传递参数是一个json形式的文件，使用json.loads来获取text
        result = json.loads(response.text)
        data = result['data']
        if 'resource' in data:
            post['video'] = data['resource']['default']['url']
        else:
            d = data['third']['data']
            post['video'] =d.get('iframe_url', d.get('swf', ''))
        post['preview'] = result['data']['video']['cover']
        post['duration'] = result['data']['video']['duration']
        yield post


    def parse_comment(self,response):
        # 由于comment传递参数是一个json形式的文件，使用json.loads来获取text
        pageinfo = json.loads(response.text)

        list = pageinfo['data']['list']  # 获取链接中的list进行循环获取
        for li in list:
            comment = CommentItem()
            comment["commentid"] = li['id']
            comment['cid'] = li['userInfo']['id']
            comment['pid'] = li['resource_id']
            comment["uname"] = li['userInfo']['username'] # 多层字典结构获取
            comment['avatar'] = li['userInfo']['avatar']
            comment['created_at'] = li['addtime']
            comment['like_counts'] = li['count_approve']
            comment["content"] = li['content']
            yield comment

        next_page = pageinfo['data']['next_page_url']
        comment_link = 'https://app.xinpianchang.com'
        if next_page is not None:
            next_page_link =  comment_link + next_page
            print('-------------------next_page--------------------')
            yield response.follow(next_page_link, self.parse_comment)


    def parse_composer(self, response):
        banner = response.xpath('//div[@class="banner-wrap"]/@style').get()  # banner背景图路径
        composer = ComposerItem()
        composer['cid'] = response.meta['cid'] # 主键
        composer['banner'], = re.findall('background-image:url\((.+?)\)', banner)  # 通过re提取banner的url
        composer['avatar'] = response.xpath(
            '//span[@class="avator-wrap-s"]/img/@src').get()
        composer['name'] = response.xpath(
            '//p[contains(@class, "creator-name")]/text()').get()
        composer['intro'] = response.xpath(
            '//p[contains(@class, "creator-desc")]/text()').get()
        composer['like_counts'] = convert_int(response.xpath('//span[contains(@class, "like-counts")]/text()').get())  # 字符串转化为int
        composer['fans_counts'] = convert_int(response.xpath('//span[contains(@class, "fans-counts")]/text()').get())
        composer['follow_counts'] = convert_int(response.xpath('//span[@class="follow-wrap"]/span[last()]/text()').get())
        composer['location'] = response.xpath(
            '//span[contains(@class,"icon-location")]/'
            'following-sibling::span[1]/text()').get() or ''
        composer['career'] = response.xpath(
            '//span[contains(@class,"icon-career")]/'
            'following-sibling::span[1]/text()').get() or ''
        yield composer
