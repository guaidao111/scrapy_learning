import time
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pymysql
import pyexcel

keyword = 'ssd 1t m2'
url = "https://www.taobao.com/"
driver = webdriver.Chrome()
driver.get(url)
input = driver.find_element_by_id('q')
input.send_keys(keyword)

search = driver.find_element_by_class_name('search-button')
search.click()


goods_list = driver.find_element_by_id('mainsrp-itemlist')
y = goods_list.rect['y'] + goods_list.rect['height']
driver.execute_script('window.scrollTo(0, %s)' % y)
product_lists = driver.find_elements_by_xpath('//div[@data-category="auctions"]')
len(product_lists)

a = product_lists[3].find_element_by_css_selector("a[class=J_ClickStat]").text
a
b = product_lists[3].find_element_by_xpath('.//a[@class="J_ClickStat"]').text
b
for p in product_lists:
    row = {}

    row['pid'] = p.find_element_by_xpath('//div[@class="row row-2 title"]/a').get_attribute("data-nid")
    row['shop'] = p.find_element_by_xpath('//div[@class="shop"]/a').text
    row['price'] = p.find_element_by_css_selector('strong').text
    row['location']= p.find_element_by_xpath('//div[@class="row row-3 g-clearfix"]/div[@class="location"]').text

row
