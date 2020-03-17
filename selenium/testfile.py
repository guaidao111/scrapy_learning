import sys
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

date = datetime.now().strftime('%F')

driver = webdriver.Chrome()
driver.get('https://www.ctrip.com/')
flight = driver.find_element_by_xpath('//li[@styletag="flight"]')
flight.click()
depature = driver.find_element_by_xpath('//div[@class="s_item"]/input[@data-target="DCity1"]')
depature.send_keys('上海')

depature.send_keys(Keys.RETURN)

dest = driver.find_element_by_xpath('//div[@class="s_item"]/input[@data-target="ACity1"]')
dest.send_keys('成都')

dest.send_keys(Keys.RETURN)

de_date = driver.find_element_by_id('FD_StartDate')
de_date.send_keys(date)

de_date.send_keys(Keys.RETURN)
