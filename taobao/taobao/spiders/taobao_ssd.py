# -*- coding: utf-8 -*-
import scrapy


class TaobaoSsdSpider(scrapy.Spider):
    name = 'taobao_ssd'
    allowed_domains = ['https://www.taobao.com/']
    url = ['https://s.taobao.com/search?q=m2+ssd+1t&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20200317&ie=utf8&cps=yes&ppath=20122%3A118104']

    def start_requests(self):
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"}
        cookies = {
            'miid':'1695763006812937565',
            'cna':'CqDNFpHwt2ICAXTmGqBbZ22/',
            'hng':'CN%7Czh-CN%7CCNY%7C156',
            'thw':'cn',
            'uc3':'lg2=VT5L2FSpMGV7TQ%3D%3D&nk2=BIOI9RhsVpdxbA%3D%3D&id2=W8nTHmi4Nvs%3D',
            'lgc':'guaidao111',
            'uc4':'nk4=0%40Boc%2BmfxxZR%2Ft%2BpgeF%2Ff%2BCPFhDWHv&id4=0%40Wepx0vbv1m3tvcSTTqL%2FsZ401w%3D%3D',
            'tracknick':'guaidao111',
            '_cc_':'VFC%2FuZ9ajQ%3D%3D',
            'tg':'0',
            'enc':'5DPxAnnnv3km63hDQXKFt1CYuhxmg6kxECWvHqKRshwy2%2FStKQgRMryUK3IE2lN%2BmjxuMkw0HrTaVsbnpDCc6g%3D%3D',
            'tfstk':'c6JlB7OwgQ5SWVFU176WAje5HH5hagrP7pRe3LD6fX6BxlvV4svQg5lDnmj9rpFC.',
            'UM_distinctid':'170b9ae1038cb7-0aa8e3cb45a127-4313f6b-240000-170b9ae1039cb6',
            't':'8a2859e485763bdbd0373f623569f38a',
            '_m_h5_tk':'d88b7a71ab6d6958f4e5dabfce018f2b_1584080418497',
            '_m_h5_tk_enc':'8c801006c5b5ad288f86a8e0b1219807',
            'mt':'ci=-1_0',
            'v':'0',
            'cookie2':'1cedd84fb7c196da682ea531237b8e26',
            '_tb_token_':'5777710e1b133',
            'CNZZDATA1256793290':'1864497547-1583753586-%7C1584431473',
            'uc1':'cookie14=UoTUPvQU8zHquA%3D%3D',
            'isg':'BDY2UQptdPFyCwC05CnuM-l0h2w4V3qRM2vmf6AfIJm049Z9COfKoZyR_7ePy3Kp',
            'l':'dBOXDWGqQsH9EbVEBOCwIkjdFm_OSIRYYuPh9-4wi_5B26TszL_OorLFtF96VfWftb8B4sz4jM99-etkZQDmndHgcGAw_xDc.'}
        yield Request(start_urls, headers=headers,cookies=cookies, callback=self.parse, dont_filter=True)


    def parse(self, response):
        data = {}
        product_lists = response.xpath('//div[@class="item J_MouserOnverReq"]')
        for li in product_lists:
            data['pid'] = li.xpath('//div[@class="ctx-box J_MouseEneterLeave J_IconMoreNew"]//a[@class="J_ClickStat"]/@data-nid').extract()
            data['title'] = li.xpath('normalize-space(string(//div[@class="ctx-box J_MouseEneterLeave J_IconMoreNew"]//a[@class="J_ClickStat"]))').extract()
            data['price'] = li.xpath('//div[@class="ctx-box J_MouseEneterLeave J_IconMoreNew"]//strong').extract()
            data['shop'] = li.xpath('normalize-space(string(//div[@class="shop"]/a/span/))').extract()
            data['location']=li.xpath('//div[@class="row row-3 g-clearfix"]/div[@class="location"]/text()').extract()
