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
        if self.r.sadd(spider.name, item['name']):
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
            charset='utf8mb4',
        )
        self.cur = self.conn.cursor()


    def close_spider(self,spider):
        # 关闭对象
        self.cur.close()
        self.conn.close()
    #以上2个函数只会在爬虫被创建和销毁的时候被调用一次，process则是每次创建一个item都被调用1次


    def process_item(self, item, spider):
        # keys = item.keys()
        # values = [item[k] for k in keys]  # 确保values和keys一一对应
        keys, values = zip(*item.items())  # 将items里的keys和values进行拉开操作，zip(*...)相当于解压操作
        sql = "insert into {} ({}) values({}) ON DUPLICATE KEY UPDATE {}".format(
            item.table_name,
            ','.join(keys),
            ','.join(['%s'] * len(values)),
            ','.join(['`{}`=%s'.format(k) for k in keys])
        )
        self.cur.execute(sql, values * 2)
        self.conn.commit()
        print(self.cur._last_executed)
        return item
