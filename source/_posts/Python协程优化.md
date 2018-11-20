---
title: Python协程优化
date: 2018-11-06 17:19:45
tags: Python
---
1. 协程增加超时处理 ：https://www.jianshu.com/p/0efdc952e8ca
 - 报错信息
```
aiohttp.client_exceptions.ServerDisconnectedError
```
- 处理
```
import async_timeout
# The event loop will ensure to cancel the waiting task when that timeout is reached and the task hasn't completed yet.
with async_timeout.timeout(0.001):  
# 捕捉timeout错误
        try:
            async with session.get('https://github.com') as r:
       exception Exception as e:
            print(repr(e))
```
2. 实测处理3k张图片（下载、识别、存储）开50协程比普通循环快200s，100以上速度无明显变化，但超时概率增加，与下载服务器性能有关。