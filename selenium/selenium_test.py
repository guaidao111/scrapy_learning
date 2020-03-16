from selenium import webdriver
driver = webdriver.Chrome()
driver.get('https://www.baidu.com')
driver.current_url
a = driver.find_element_by_xpath('//div[@id="u1"]/a[2]')
a
a.get_attribute('name')
a.value_of_css_property('float')
a.click()
driver.back()
kw = driver.find_element_by_id('kw')
kw.send_keys('python')
su = driver.find_element_by_id('su')
su.click()
h3_list = driver.find_elements_by_tag_name('h3')
for h3 in h3_list:
    print(h3.text)
driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
# 翻页操作只能用于当前页，多重翻页需要用循环解决
next_page = driver.find_element_by_class_name('n')
next_page.click()
driver.quit()
