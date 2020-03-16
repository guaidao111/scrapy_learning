# Scrapy



### Create Project



| command                                     | usage                                                        |
| ------------------------------------------- | ------------------------------------------------------------ |
| scrapy startproject xpc                     | create project                                               |
| cd xpc                                      | get into the directory                                       |
| virtualenv ENV                              | 创建使用的虚拟环境                                           |
| cd env/scripts                              | 进入scripts                                                  |
| activate.bat                                | 激活并进入虚拟环境                                           |
| .\activate.ps1                              | powershell进入虚拟环境                                       |
| pi -r requirements.txt                      | 写完文档后安装txt内的包                                      |
| scrapy genspider discovery xinpianchang.com | 生成spider，spidername需和创建的projectname不同，后接爬取的域名 |
| scrapy shell url                            | 分析使用某个网址内容，返回的是一个response                   |
| import re re.findall                        | 对返回的response做测试                                       |



scrapy_redis 

 lpush discovery:start_urls https://www.xinpianchang.com/channel/index/sort-like?from=navigator

可以设置等待传入网页参数，这样可以同时进行多个页面爬取（但只使用于相同类型的页面设置）