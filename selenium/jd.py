import sys
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyexcel

# 传入参数，让京东去搜索

if __name__ == '__main__':
    keyword = 'iphone'
    if len(sys.argv) > 1:
        keyword = sys.argv[1]
    # 设置不打开浏览器爬取
    option = Options()
    option.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=option)
    driver.get('https://www.jd.com/')
    # 在对应步骤截图来查看状态
    driver.get_screenshot_as_file(u"F:\scrapy_learning\selenium\screenshot\登录成功.png")
    kw = driver.find_element_by_id('key')
    kw.send_keys(keyword)
    kw.send_keys(Keys.RETURN)
    time.sleep(3)
    # 点击按销量排序
    sort_btn = driver.find_element_by_xpath('.//div[@class="f-sort"]/a[2]')
    sort_btn.click()
    driver.get_screenshot_as_file(u"F:\scrapy_learning\selenium\screenshot\排序完成.png")

    has_next = True
    rows = []
    page_count = 0

    while has_next:
        page_count += 1
        if page_count > 10:
            break
        time.sleep(3)
        cur_page = driver.find_element_by_xpath('//div[@id="J_bottomPage"]//a[@class="curr"]').text
        print('---------current page is %s ----------' % cur_page)
        # 先获取整个商品区域的尺寸坐标
        goods_list = driver.find_element_by_id('J_goodsList')
        # 根据区域大小决定往下滑动多少
        y = goods_list.rect['y'] + goods_list.rect['height']
        driver.execute_script('window.scrollTo(0, %s)' % y)
        # 获取所有商品的节点
        products = driver.find_elements_by_class_name('gl-item')
        for p in products:
            row = {}
            sku = p.get_attribute('data-sku')
            row['price'] = p.find_element_by_css_selector('strong.J_%s' % sku).text
            row['name'] = p.find_element_by_css_selector('div.p-name>a>em').text.replace('\n', '')
            row['comments'] = p.find_element_by_id('J_comment_%s' % sku).text
            try:
                row['shop'] = p.find_element_by_css_selector('div.p-shop>span>a').text
            except:
                row['shop'] = '无'
            rows.append(row)

        next_page = driver.find_element_by_css_selector('a.pn-next')
        if 'disabled' in next_page.get_attribute('class'):
            has_next = False
        else:
            next_page.click()
    pyexcel.save_as(records=rows, dest_file_name='%s.xls' % keyword)


    driver.quit()
