import sys
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pyexcel

date = datetime.now().strftime('%F')
driver = webdriver.Chrome()
driver.get('https://www.ctrip.com/')
flight = driver.find_element_by_xpath('//li[@styletag="flight"]')
flight.click()

depature = WebDriverWait(driver,10).until(
    EC.presence_of_element_located((By.XPATH, '//div[@class="s_item"]/input[@data-target="DCity1"]')))
# depature = driver.find_element_by_xpath('//div[@class="s_item"]/input[@data-target="DCity1"]')
depature.clear()
time.sleep(2)
depature.send_keys('杭州')
time.sleep(2)

depature.send_keys(Keys.RETURN)

dest = driver.find_element_by_xpath('//div[@class="s_item"]/input[@data-target="ACity1"]')
dest.send_keys('成都')

time.sleep(2)
dest.send_keys(Keys.RETURN)

de_date = driver.find_element_by_id('FD_StartDate')
de_date.send_keys(date)

time.sleep(2)
de_date.send_keys(Keys.RETURN)



flights = WebDriverWait(driver,10).until(
    EC.presence_of_all_elements_located((By.XPATH,'//div[@class="search_box search_box_tag search_box_light Label_Flight"]'))
)
for f in flights:
    finfo = {}
    finfo['airlines'] = f.find_element_by_xpath('//div[@class="search_box search_box_tag search_box_light Label_Flight"]//div[@class="logo-item flight_logo"]/div[@data-ubt-hover="c_flight_aircraftInfo"]').text
    finfo['de_time'] = f.find_element_by_xpath('//div[@class="inb right"]//strong').text
    finfo['de_terminal'] = f.find_element_by_xpath('//div[@class="inb right"]//div[@class="airport"]').text
    finfo['dest_time'] = f.find_element_by_xpath('//div[@class="inb left"]//strong').text
    finfo['dest_terminal'] = f.find_element_by_xpath('//div[@class="inb left"]//div[@class="airport"]').text
    finfo['ontime_rate'] = f.find_element_by_xpath('//span[@class="direction_black_border"]').text
    finfo['price'] = f.find_element_by_xpath('//div[@class="search_box search_box_tag search_box_light Label_Flight"]//span[@class="base_price02"]').text

    print(finfo)
# driver.close()
