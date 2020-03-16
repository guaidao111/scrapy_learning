# 中间件的调用规则



## 基本结构图



![img](https://img-blog.csdn.net/20180502174530976)



### Scrapy Engine

引擎负责控制数据流在系统中所有组件中流动，并在相应动作发生时触发事件。

### 调度器(Scheduler)

调度器从引擎接受request并将他们入队，以便之后引擎请求他们时提供给引擎。

### 下载器(Downloader)

下载器负责获取页面数据并提供给引擎，而后提供给spider。

### Spiders

Spider是Scrapy用户编写用于分析response并提取item(即获取到的item)或额外跟进的URL的类。 每个spider负责处理一个特定(或一些)网站。 更多内容请看 [Spiders](http://scrapy-chs.readthedocs.io/zh_CN/stable/topics/spiders.html#topics-spiders) 。

### Item Pipeline

Item Pipeline负责处理被spider提取出来的item。典型的处理有清理、 验证及持久化(例如存取到数据库中)。 更多内容查看 [Item Pipeline](http://scrapy-chs.readthedocs.io/zh_CN/stable/topics/item-pipeline.html#topics-item-pipeline) 。

### 下载器中间件(Downloader middlewares)

下载器中间件是在引擎及下载器之间的特定钩子(specific hook)，处理Downloader传递给引擎的response（也包括引擎传递给下载器的Request）。 其提供了一个简便的机制，通过插入自定义代码来扩展Scrapy功能。更多内容请看 [下载器中间件(Downloader Middleware)](http://scrapy-chs.readthedocs.io/zh_CN/stable/topics/downloader-middleware.html#topics-downloader-middleware) 。

一句话总结就是：处理下载请求部分

### Spider中间件(Spider middlewares)

Spider中间件是在引擎及Spider之间的特定钩子(specific hook)，处理spider的输入(response)和输出(items及requests)。 其提供了一个简便的机制，通过插入自定义代码来扩展Scrapy功能。



## 基本逻辑

## process_request



> 在request对象传往downloader的过程中调用。当返回不同类型的值的时候，行为也不一样:



| 返回值        | 行为                                                         |
| ------------- | ------------------------------------------------------------ |
| None          | 一切行为正常，继续执行其他中间件链                           |
| Response      | 停止调用其他process_request和process_exception函数，也不再继续下载该请求，然后走调用process_response的流程 |
| Request       | 不再继续调用其他的process_request函数，交由调度器重新安排下载。 |
| IgnoreRequest | process_exception函数会被调用，如果没有此方法，则request.errorback会被调用，如果errorback也没有，则此异常会被忽略，甚至连日志都没有。 |





### process_response



> 在将下载结果返回给引擎过程中调用。



| 返回值        | 行为                                                         |
| ------------- | ------------------------------------------------------------ |
| Response      | 继续调用其他中间件的process_response                         |
| Request       | 不再继续调用其他的process_request函数，交由调度器重新安排下载。 |
| IgnoreRequest | request.errorback会被调用，如果errorback也没有，则此异常会被忽略，甚至连日志都没有。 |





### process_exception



> 在下载过程中出现异常或者在process_request中抛出IgnoreRequest异常的时候调用



| 返回值        | 行为                                                         |
| ------------- | ------------------------------------------------------------ |
| Response      | 开始中间件链的process_response流程处理                       |
| Request       | 不再继续调用其他的process_request函数，交由调度器重新安排下载。 |
| IgnoreRequest | process_exception函数会被调用，如果没有此方法，则request.errorback会被调用，如果errorback也没有，则此异常会被忽略，甚至连日志都没有。 |





### from_crawler(cls, crawler)



> 用于传递参数，如果存在该函数，则调用该函数创建中间件的实例，如果要写该函数，一定要返回一个中间件的对象。





# 内置中间件

------



**（scrapy.downloadmiddlewares.部分已省略）**



| 中间件                                    | 作用                              |
| ----------------------------------------- | --------------------------------- |
| robotstxt.RobotsTxtMiddleware             | 请求robots.txt文件，并解析规则    |
| httpauth.HttpAuthMiddleware               | 请求带Basic-auth验证的请求        |
| downloadtimeou.DownloadTimeoutMiddleware  | 下载请求超时最大时长              |
| defaultheaders.DefaultHeadersMiddleware   | 默认的请求头信息                  |
| useragent.UserAgentMiddleware             | 设置请求头里的User-Agent          |
| retry.RetryMiddleware                     | 如果下载失败，是否重试，重试次数  |
| redirect.MetaRefreshMiddleware            | 实现Meta标签重定向（状态码是200） |
| httpcompression.HttpCompressionMiddleware | 实现压缩内容的解析（例如gzip）    |
| redirect.RedirectMiddleware               | 实现30x的HttpCode的重定向         |
| cookies.CookiesMiddleware                 | 实现对cookies的设置管理           |
| httpproxy.HttpProxyMiddleware             | 实现IP代理                        |
| stats.DownloaderStats                     | 下载信息的统计                    |
| httpcache.HttpCacheMiddleware             | 下载结果的缓存                    |

