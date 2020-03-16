# Redis



### Redis常用命令



| 命令                                         | 作用                                           |
| -------------------------------------------- | ---------------------------------------------- |
| redis-server.exe（redis-s）                  | 启动服务器（需保持开启使用，已设置快进捷代码） |
| redis-cli.exe -h 127.0.0.1 -p 6379 redis-c） | 进入命令行启动服务器（已设置快进捷代码）       |
| KEYS *                                       | 查看所有键                                     |
| del key                                      | 删除键                                         |
| get key                                      | 获取string类型键值                             |
| smember key                                  | 获取set类型键值                                |
| set key value                                | 设置一个键值                                   |
| lpush listname value                         | 对一个列表赋值                                 |