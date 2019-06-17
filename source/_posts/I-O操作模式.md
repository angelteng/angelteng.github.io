---
title: I/O操作模式
date: 2019-04-24 15:18:15
tags: 
- 底层
categories: 底层
---
# 概念 
- 流：一个流可以是文件，socket，pipe等等可以进行I/O操作的内核对象
- I/O操作：流的操作（读/写）。缓存 I/O 又被称作标准 I/O，大多数文件系统的默认 I/O 操作都是缓存 I/O。在 Linux 的缓存 I/O 机制中，操作系统会将 I/O 的数据缓存在文件系统的页缓存（ page cache ）中，也就是说，数据会先被拷贝到操作系统内核的缓冲区中，然后才会从操作系统内核的缓冲区拷贝到应用程序的地址空间。
- 文件描述符fd：是一个用于表述指向文件的引用的抽象化概念。文件描述符在形式上是一个非负整数。实际上，它是一个索引值，指向内核为每一个进程所维护的该进程打开文件的记录表。

## IO模式
一次IO访问（以read举例），数据会先被拷贝到操作系统内核的缓冲区中，然后才会从操作系统内核的缓冲区拷贝到应用程序的地址空间。所以说，当一个read操作发生时，它会经历两个阶段：
1. 等待数据准备 (Waiting for the data to be ready)
2. 将数据从内核拷贝到进程中 (Copying the data from the kernel to the process)

正式因为这两个阶段，linux系统产生了下面五种网络模式的方案。
- 阻塞 I/O（blocking IO）
- 非阻塞 I/O（nonblocking IO）
- I/O 多路复用（ IO multiplexing）
- 信号驱动 I/O（ signal driven IO）
- 异步 I/O（asynchronous IO）

![image.png](0.png)


### I/O多路复用
select，poll，epoll都是IO多路复用的机制。一个进程可以监视多个描述符，一旦某个描述符就绪（一般是读就绪或者写就绪），能够通知程序进行相应的读写操作。但select，poll，epoll本质上都是同步I/O。

与阻塞I/O相比，多路复用需要使用两个system call (select 和 recvfrom)，而blocking IO只调用了一个system call (recvfrom)。但是，用select的优势在于它可以同时处理多个connection。

epoll 操作
```
    int epoll_create(int size)；//创建一个epoll的句柄，size用来告诉内核这个监听的数目一共有多大
    int epoll_ctl(int epfd, int op, int fd, struct epoll_event *event)；//对指定描述符fd执行op操作
    int epoll_wait(int epfd, struct epoll_event * events, int maxevents, int timeout);//等待epfd上的io事件，最多返回maxevents个事件。
```

在 select/poll中，进程只有在调用一定的方法后，内核才对所有监视的文件描述符进行扫描，而epoll事先通过epoll_ctl()来注册一 个文件描述符，一旦基于某个文件描述符就绪时，内核会采用类似callback的回调机制，迅速激活这个文件描述符，当进程调用epoll_wait() 时便得到通知。(此处去掉了遍历文件描述符，而是通过监听回调的的机制。)

优点：
1. 监视的描述符数量不受限制，它所支持的FD上限是最大可以打开文件的数目。
2. IO的效率不会随着监视fd的数量的增长而下降。epoll不同于select和poll轮询的方式，而是通过每个fd定义的回调函数来实现的。只有就绪的fd才会执行回调函数。


参考：
[我读过的最好的epoll讲解--转自”知乎“](https://blog.51cto.com/yaocoder/888374)
[Linux IO模式及 select、poll、epoll详解](https://segmentfault.com/a/1190000003063859)
[文件描述符和流的关系？](https://blog.csdn.net/qq_28090573/article/details/50863779)