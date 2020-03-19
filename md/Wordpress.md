# WordPress



### phpstudy



* 安装目录中的WWW目录为网站根目录

* 访问方式为在浏览为输入

http://localhost/index.html

or

http://127.0.0.1/index.html

这是通过路径映射的方式制定了对应路径（apache服务）

直接输入localhost/由于没制定访问文件，会访问根目录的index.html（apache制定的默认首页文件）

![apache设置](Wordpress.assets/image-20200317225828427.png)

可以看到设置的最高优先级文件是index.php

安装好phpMyAdmin

localhost/phpMyAdmin4.8.5打开网页服务端管理mysql数据库



### 安装wordpress

1. 将文件夹解压放入WWW文件夹，修改wordpress文件夹名

2. 访问初始化界面：

   localhost/wordpress01/index.php

3. 在phpMyAdmin界面创建数据库用于连接

4. 登录管理员后台：

   ![管理员后台目录](Wordpress.assets/image-20200317232716230.png)

5. 访问管理员后台路径：http://localhost/wordpress01/wp-login.php 或 http://localhost/wordpress01/wp-admin/

6. 前台地址：http://localhost/wordpress01/index.php