---
title: 在eventlet的猴子补丁下sslsocket链接失败的问题
date: 2019-09-24 17:29:25
tags:
---
某项目有一个发邮件的需求，由于项目搭建的Web Server使用了eventlet的monkey patch为了多进程下使用websocket。
发现在建立ssl socket时会报错
```
    wrap_socket() got an unexpected keyword argument '_context'
```
在github查找eventlet的issue。发现[python 3.7 - wrap_socket() got an unexpected keyword argument '_context'](https://github.com/eventlet/eventlet/issues/526)这个bug还是open的。

解决：
起了新进程，用消息队列通讯，实现发送邮件需求。