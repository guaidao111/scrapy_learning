import time
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pymysql

if __name__ == '__main__':
    keyword = 'ssd 1t m2'
    url = "https://www.taobao.com/"

    # 读取保存的cookies
    with open('F:/scrapy_learning/taobao/taobao.txt', 'r', encoding='utf8') as f:
       cookies = json.loads(f.read())

    driver = webdriver.Chrome()
    driver.get(url)

    for cookie in cookies:
        if 'expiry' in cookie:
            del cookie['expiry']
        driver.add_cookie(cookie)
    # 添加user-agent
    options =webdriver.ChromeOptions()
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36')
    driver.get(url)

    time.sleep(2)
    input = driver.find_element_by_id('q')
    input.send_keys(keyword)
    time.sleep(3)
    search = driver.find_element_by_class_name('search-button')
    search.click()
    time.sleep(3)
    driver.get_screenshot_as_file(u"F:/scrapy_learning/taobao/搜索完成.png")

    # rows = []
    has_next = True
    page_count = 0
    # 连接mysql服务器
    conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='root',db='wordpress01',charset='utf8')
    # 使用游标操作
    cursor = conn.cursor()
    while has_next:
        page_count += 1
        print(page_count)
        time.sleep(3)
        # 滑动到页面底部以让他全部加载并可以点下一页
        goods_list = driver.find_element_by_id('mainsrp-itemlist')
        y = goods_list.rect['y'] + goods_list.rect['height']
        driver.execute_script('window.scrollTo(0, %s)' % y)

        product_lists = driver.find_elements_by_xpath('//div[@data-category="auctions"]')
        for p in product_lists:
            row = {}
            row['title'] = p.find_element_by_xpath('.//div[@class="row row-2 title"]/a').text
            row['pid'] = p.find_element_by_xpath('.//div[@class="row row-2 title"]/a').get_attribute("data-nid")
            row['shop'] = p.find_element_by_xpath('.//div[@class="shop"]/a').text
            row['price'] = p.find_element_by_css_selector('strong').text
            row['location']= p.find_element_by_xpath('.//div[@class="row row-3 g-clearfix"]/div[@class="location"]').text
            row['href'] = p.find_element_by_xpath('.//div[@class="row row-2 title"]/a').get_attribute("href")
            row['pic_link'] = p.find_element_by_xpath('.//img').get_attribute("src")
            # rows.append(row)
            cols = ", ".join('`{}`'.format(k) for k in row.keys())
            print(cols)
            val_cols = ', '.join('%({})s'.format(k) for k in row.keys())
            print(val_cols)
            sql = "insert into ssd_info(%s) values(%s)"
            res_sql = sql % (cols, val_cols)
            print(res_sql)
            cursor.execute(res_sql, row)  # 将字典a传入
            conn.commit()

        next_page = driver.find_element_by_css_selector('li.item.next')
        if 'next-disabled' in next_page.get_attribute('class'):
            has_next = False
        else:
            next_page.click()



    cursor.close()
    conn.close()



    driver.quit()
