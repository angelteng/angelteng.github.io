---
title: Flask中并发优化jMeter测试
date: 2018-11-15 17:13:18
tags: 
- Python
- Flask
categories: Python
---
1. Queue的使用
[参考](http://www.cnblogs.com/itogo/p/5635629.html)
in Python3.x should use 'pip install q' 
in Python2.x should use 'pip install queue'

2. 关于模块：除了包含函数定义外，模块也可以包含可执行语句。这些语句一般用来初始化模块。他们仅在 *第一次* 被导入的地方执行一次。所以如果有需要预初始化对象并共享，可以在模块执行语句中写。

3. 关于并发测试：
postman的runner是串行的，上一个请求结束后才开始下一个请求，只能算连续测试但不是并发测试。
推荐使用JMeter。
安装:
```
>>> brew install jmeter
# 如果提示没有安装java
>>> brew install brew cask
>>> brew cask install java
```
使用：
```
>>> open /usr/local/bin/jmeter
```
[入门教程](https://www.jianshu.com/p/0e4daecc8122)  
[固定qps压力测试](https://www.cnblogs.com/fnng/archive/2012/12/22/2829479.html)
![测试结果](https://upload-images.jianshu.io/upload_images/14827444-f9d76256d76fb2b9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

4. 使用htop查看服务器cpu使用情况
```
>>> yum install htop
>>> htop #打开
>>> q #退出
```
[入门教程](https://www.cnblogs.com/lazyfang/p/7650010.html)
![htop](https://upload-images.jianshu.io/upload_images/14827444-417ad4f5c30a3ba1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

 