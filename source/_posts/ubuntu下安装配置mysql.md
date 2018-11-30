---
title: ubuntu下安装配置mysql、Redis
date: 2018-11-30 11:31:48
tags: Ubuntu
---
以下为Ubuntu 16.04环境
安装配置Mysql：
```
# 安装mysql
sudo apt-get install mysql-server
sudo apt install mysql-client
sudo apt install libmysqlclient-dev
# 测试安装mysql是否成功
sudo netstat -tap | grep mysql

# 修改root用户密码
>>> mysql -u root -p
# 进入到mysql
use mysql;
update user set authentication_string=PASSWORD('123') where User='root';
# 新增用户远程连接权限(指定具体ip地址)
grant all privileges on *.* to 'root'@'192.168.33.1' identified by '123';
flush privileges;

# 修改配置文件
vim /etc/mysql/mysql.conf.d/mysqld.cnf;
修改 bind-address=0.0.0.1

# 重启mysql服务
service mysql restart
```

安装配置Redis
```
# 安装
sudo apt-get update
sudo apt-get install redis-server
# 启动
sudo /etc/init.d/redis-server start
# 进入Redis
redis-cli
# 配置开机自启动
chmod +x /etc/init.d/redis-server 
update-rc.d redis-server defaults
# 操作
service redis-server start/stop/restart
```