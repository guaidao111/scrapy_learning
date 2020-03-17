# Selenium

------

`学习笔记` `爬虫工具` `浏览器调试`



### 选择器

#### element

```python
from selenium import webdriver
driver = webdriver.Chrome()
driver.get('https://www.baidu.com')
driver.current_url
a = driver.find_element_by_xpath('//div[@id="u1"]/a[1]')
```

> **Selenium**里只能取得对应节点，不能取到text部分。

* 因此取文本应该：

```python
	driver.find_element_by_xpath('//div[@id="u1"]/a[2]').text
```

* 可以看到是在xpath结束后加上text，属性同理

* 获取属性则可以使用

```python
a.get_attribute('name')
```

* css的值可以通过：

  ```python
  a.value_of_css_property('float')
  ```



#### 动作



| Command                                                      | usage                              |
| ------------------------------------------------------------ | ---------------------------------- |
| a.click(0)                                                   | 点击a（需要可以被点击）            |
| driver.back()                                                | 浏览器退回                         |
| driver.forward()                                             | 浏览器前进                         |
| element.send_keys('python')                                  | 在输入框输入（kw为已查找好的对象） |
| element.click()                                              | 点击                               |
| element.rect                                                 | 返回元素尺寸                       |
| element.location                                             | 返回元素坐标                       |
| element.text                                                 | 返回文本信息                       |
| element.get_attribute                                        | 获取属性                           |
| element.get_property                                         | 也是获取属性值                     |
| element.value_of_css_property                                | 获取节点的CSS样式属性              |
| driver.execute_script('window.scrollTo(0,document.body.scrollHeight)') | 滑动到浏览器底部（可拖动高度）     |
| ~~driver.save_sreenshot(‘1.png’)~~                           | 截图（已不再使用）                 |
| get_screenshot_as_file（）                                   | 路径截图更好用                     |
| driver.current_url                                           | 当前url                            |

> **拖动scroll**这种模式的问题是，取到的位置可能看不到想要的按键，所以要定位到指定地点
>
> 

```python
    next_page = driver.find_element_by_css_selector('a.pn-next')
    next_page.location
    # location返回的是x和y坐标值
    driver.execute_script('window.scrollTo({x},{y})'.format(**next_page.location))
```

> 测试后发现仍旧因为页面加载问题导致长度不是正好，采用获取商品尺寸的方式来解决

```python
    goods_list = driver.find_element_by_id('J_goodsList')
    # 根据区域大小决定往下滑动多少
    y = goods_list.rect['y'] + goods_list.rect['height']
    driver.execute_script('window.scrollTo(0, %s)' % y)
```
#### 特殊按键

```python
from selenium.webdriver.common.keys import Keys
```

| Command                   | Usage        |
| ------------------------- | ------------ |
| kw.send_keys(Keys.RETURN) | 传入回车按键 |
|                           |              |
|                           |              |



#### 选项

> 无界面启动chrome（替代了停止维护的phantomJS）

```python
from selenium.webdriver.chrome.options import Options
option = Options()
option.add_argument(‘--headless’)
driver = webdriver.Chrome(chrome_options=option)
```



#### 元素查找



| command                           | usage                      |
| --------------------------------- | -------------------------- |
| find_element                      | 查找元素                   |
| find_element_by_class_name        | 通过元素的class属性查找    |
| find_element_by_xpath             | 通过xpath查找              |
| find_element_by_id                | 根据id查找                 |
| find_element_by_css_selector      | 用CSS选择器查找            |
| find_element_by_tag_name          | 根据tag名查找              |
| find_element_by_name              | 根据元素名查找             |
| find_element_by_link_text         | 根据link的文字进行查找     |
| find_element_by_partial_link_text | 根据link的部分文字进行查找 |

**注：elements  则会返回一个列表，以上都是返回单个元素**



* 等待-wait



* 隐式等待

  ```python
  # 查找某元素，如果么有找到，则等10s
  driver.implicitly_wait(10)
  ```

  

* 显示等待

```python
    # 查找1个元素
    # 最长等待10s，直到查找条件的元素被添加到节点内
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    WebDriverWait(driver,10).until(
        EC.presence_of_all_elements_located((By.XPATH,'//div[@class="search_box search_box_tag search_box_light Label_Flight"]'))
    )
```

