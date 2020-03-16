from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# 传入参数，让京东去搜索


driver = webdriver.Chrome()
driver.get('https://www.jd.com/')

kw = driver.find_element_by_id('key')
kw.send_keys('iphone')
kw.send_keys(Keys.RETURN)

# 点击按销量排序
sort_btn = driver.find_element_by_xpath('.//div[@class="f-sort"]/a[2]')
sort_btn.click()

# 获取产品的整个部分
products = driver.find_elements_by_class_name('gl-item')
len(products)
p = products[0]
sku = p.get_attribute('data-sku')
sku
price = p.find_element_by_css_selector('strong.J_%s' % sku).text
price
name = p.find_element_by_css_selector('div.p-name>a>em').text
name
comment = p.find_element_by_id('J_comment_%s' % sku).text
comment
shop = p.find_element_by_css_selector('div.p-shop>span>a').text
shop

# 拖动网页（jd页面有拖动到底部再显示部分的操作，所以需要拖动加载）
driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
# 这种模式的问题是，取到的位置可能看不到想要的按键，所以要定位到指定地点
next_page = driver.find_element_by_css_selector('a.pn-next')
next_page.location
driver.execute_script('window.scrollTo({x},{y})'.format(**next_page.location))
next_page.click()
# 发现由于新加载了产品因此长度发生变化，导致next_page无法定位，采用整个产品列表长度进行举例测算
goods_list = driver.find_element_by_id('J_goodsList')
goods_list.rect
goods_list.rect['y'] + goods_list.rect['height']
cur_page = driver.find_element_by_xpath('//div[@id="J_bottomPage"]//a[@class="curr"]').text
cur_page
