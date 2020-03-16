# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import redis
from scrapy.exceptions import  DropItem

# redis
class RedisPipeline(object):
    def open_spider(self, spider):
        self.r = redis.Redis(host='127.0.0.1')

# def close_spider(self,spider):
#     # 关闭对象
#     self.r.close()

    def process_item(self, item, spider):
        if self.r.sadd(spider.name, item['av_code']):
            return item
    # 如果异常使用dropitem抛出异常
        raise DropItem


# item通过管道到达地点（mysql文件夹）
class MysqlPipeline(object):
    def open_spider(self, spider):
        self.conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            db='scrapy_data',
            user='root',
            password='81820720',
            charset='utf8',
        )
        self.cur = self.conn.cursor()
        self.tablename = 'p141jav_info'
        sql = """
            CREATE TABLE IF NOT EXISTS %s (
            av_code VARCHAR(128) NOT NULL,
            actress VARCHAR(128),
            tag VARCHAR(256) NOT NULL,
            magnet text NOT NULL,
            img VARCHAR(256))
            """ % self.tablename

        self.cur.execute(sql)

    def close_spider(self,spider):
        # 关闭对象
        self.cur.close()
        self.conn.close()
    #以上2个函数只会在爬虫被创建和销毁的时候被调用一次，process则是每次创建一个item都被调用1次


    def process_item(self, item, spider):
        # keys = item.keys()
        # values = [item[k] for k in keys]  # 确保values和keys一一对应
        keys, values = zip(*item.items())  # 将items里的keys和values进行拉开操作，zip(*...)相当于解压操作
        sql = "insert into {} ({}) values({})".format(
            'p141jav_info',
            ','.join(keys),
            ','.join(['%s'] * len(values))
        )
        self.cur.execute(sql, values)
        self.conn.commit()
        print(self.cur._last_executed)
        return item
