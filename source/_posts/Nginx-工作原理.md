---
title: Nginx 工作原理
date: 2019-04-24 15:49:01
tags:
- Nginx
categories: 服务器
---
# Nginx 模块结构
![image.png](https://upload-images.jianshu.io/upload_images/14827444-b1321442e1909834.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# Nginx 工作流程
Nginx的IO通常使用epoll，epoll函数使用了I/O复用模型。
1. master进程一开始根据配置，来建立需要listen的网络socket fd，然后fork出多个worker进程。根据进程的特性，新建立的worker进程，也会和master进程一样，具有相同的设置。因此，其也会去监听相同ip端口的套接字socket fd。
2. 当一个请求进来的时候，所有的worker都会感知到。这样就会产生所谓的“惊群现象”。为了保证只会有一个进程成功注册到listenfd的读事件，nginx中实现了一个“accept_mutex”类似互斥锁，只有获取到这个锁的进程，才可以去注册读事件。其他进程全部accept 失败。
3. 监听成功的worker进程，读取请求，解析处理，响应数据返回给客户端，断开连接。即nginx用一个独立的worker进程来处理一个请求，一个worker进程可以处理多个请求。
因此，一个请求，完全由worker进程来处理，而且只在一个worker进程中处理。采用这种方式的好处：
    - 节省锁带来的开销。对于每个worker进程来说，独立的进程，不需要加锁，所以省掉了锁带来的开销，同时在编程以及问题查上时，也会方便很多。
    - 独立进程，减少风险。
    - 采用独立的进程，可以让互相之间不会影响，一个进程退出后，其它进程还在工作，服务不会中断，master进程则很快重新启动新的worker进程。
    - 在一次请求里无需进程切换。

# Nginx的配置
- worker_processes：worker角色的进程个数
- worker_connections：每一个worker进程能并发处理（发起）的最大连接数（包含所有连接数）
- Nginx作为http服务器的时候：max_clients（最大连接数） = worker_processes * worker_connections
- Nginx作为反向代理服务器的时候：max_clients（最大连接数） = worker_processes * worker_connections/4 （/4原因：因为浏览器默认会开启2个连接到nginx server，而且nginx还会为每个连接使用fds（file descriptor）从连接池建立connection到upstream后端。）


参考：
[nginx快速入门之基本原理篇](https://zhuanlan.zhihu.com/p/31196264)
[理解Nginx工作原理](https://www.jianshu.com/p/6215e5d24553)