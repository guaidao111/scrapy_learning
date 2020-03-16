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
| kw.send_keys('python')                                       | 在输入框输入（kw为已查找好的对象） |
| driver.execute_script('window.scrollTo(0,document.body.scrollHeight)') | 滑动到浏览器底部（可拖动高度）     |
| driver.save_sreenshot(‘1.png’)                               | 截图                               |

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



