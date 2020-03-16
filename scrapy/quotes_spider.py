import scrapy


class QuotesSpider(scrapy.Spider):  # 创建一个类，继承scrapy.Spider
    # 属性如下
    name = 'Aine_Maria'  # 爬虫的名称
    start_urls = [
        'https://www.141jav.com/actress/Maria%20Aine'
    ]  # 爬取的初始的url（列表）

    def parse(self, response):  # 创建parse函数
        # quotes = response.css('div.quote') 也支持css语法
        for quote in response.xpath('//div[@class="card mb-3"]'): # 有了scrapy模块，无需取单独引入repsonse
            yield {
                'ID':quote.xpath('.//h5/a/text()').get(), # CSS语法,extract_first，提取列表中第一个选择器里的内容
                'Magnet':quote.xpath('.//a[@title="Magnet torrent"]/@href').get(),
                'Torrent':quote.xpath('.//a[@title="Download .torrent"]/@href').get()
            }
            # yield将text和author数据返回
        next_page = response.xpath('//a[@class="pagination-next button is-primary"]/@href').get()
        if next_page:
            yield response.follow(next_page, self.parse) # 将next_page的内容传回给自己用
