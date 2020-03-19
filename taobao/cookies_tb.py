from selenium import webdriver
import time
import json
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
driver = webdriver.Chrome()
driver.get("https://www.taobao.com/")

dictCookies = driver.get_cookies()
jsonCookies = json.dumps(dictCookies)
print(jsonCookies)
with open('F:/scrapy_learning/taobao/taobao.txt', 'w') as f:
  f.write(jsonCookies)
