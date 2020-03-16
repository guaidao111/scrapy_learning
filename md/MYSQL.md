# 数据库
DBMS -- Database management system
> * 关系型数据库--存储重要数据

Oracle
MySQL
MSSQL
PG

> * 非关系型数据库--NoSQL

MongoDB
ES
Redis

> * 云数据库

RDS,PolarDB
TDSQL

> * NewSQL

TiDB

#### MySQL
1. MySQL厂家
Oracle(官方)/MariaDB/Percona

2. MySQL企业版本选择

#### cmd登录客户端
mysql -u root -p
exit 退出

#### 常见命令

| command                | usage                |
| ---------------------- | -------------------- |
| show databases;        | 显示数据库表         |
| use 库名;              | 调用库               |
| show tables;           | 显示库里的表         |
| show tables from 库名; | 直接调用库里的表展示 |
| select database();     | 显示所在的库         |
| desc 表名              | 查看表结构           |


```sql
# 建表
create table testinfo(
  id int,
  name varchar(20)
   )；
# 查看整个表   
select * from testinfo；
# 插入数据（真插入）
insert into testinfo(id, name) values(1,'john');
# 更新数据
update testinfo set name='lilei' where id =1;
# 删除数据
delete from testinfo where id=1;
```

#### 语法规范
* 不区分大写小，建议关键字大写，表名、列明小写
* ;结尾
* 每条命令根据需要可以进行缩进或换行
* 注释
    1 .单行注释： # 注释文字
    2 .单行注释：-- 注释文字