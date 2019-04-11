---
title: tcp socket 与unix domain socket
date: 2019-03-23 14:58:46
tags: socket
---
# 什么是Socket

在网络上的两个程序通过一个双向的通信连接实现数据的交换，这个连接的一端称为一个Socket。Socket可以被定义描述为两个应用通信通道的端点，一个Socket 端点可以用Socket地址（地址IP、端口、协议组成）来描述。Socket作为一种进程通信机制，操作系统会分配唯一一个Socket标识，这个标识与通讯协议有关（不仅限于TCP或UDP）。

# Unix Domain Socket

Unix Domain Socket并不是一个实际的协议，它只在同客户机和服务器通信时使用的API，且一台主机与在不同主机间通信时使用相同的API。

Unix Domain Socket有以下特点:
- Unix Domain Socket使用的地址通常是一个文件 xxx.sock
- 在同一主机通讯时，传输速率是不同主机间的两倍
- Unix Domain Socket套接字描述符可以在同一主机不同进程间传递
- Unix Domain Socket套接字可以向服务器提供用户认证信息

# TCP Socket与Unix Domain Socket

无论时TCP Socket套接字还是Unix Domain Socket套接字，每个套接字都是唯一的。TCP Socket通过IP和端口描述，而Unix Domain Socket描述。
TCP属于传输层的协议，使用TCP Socket进行通讯时，需要经过传输层TCP/IP协议的解析。
而Unix Domain Socket可用于不同进程间的通讯和传递，使用Unix Domain Socket进行通讯时不需要经过传输层，也不需要使用TCP/IP协议。所以，理论上讲Unix Domain Socket具有更好的传输效率。

# socket缓冲区
![TCP套接字的I/O缓冲区示意图](https://upload-images.jianshu.io/upload_images/191918-36ec0344bae9d79e.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/697)

每个 socket 被创建后，都会分配两个缓冲区，输入缓冲区和输出缓冲区。write()/send() 并不立即向网络中传输数据，而是先将数据写入缓冲区中，再由TCP协议将数据从缓冲区发送到目标机器。一旦将数据写入到缓冲区，函数就可以成功返回，不管它们有没有到达目标机器，也不管它们何时被发送到网络，这些都是TCP协议负责的事情。TCP协议独立于 write()/send() 函数，数据有可能刚被写入缓冲区就发送到网络，也可能在缓冲区中不断积压，多次写入的数据被一次性发送到网络，这取决于当时的网络情况、当前线程是否空闲等诸多因素，不由程序员控制。read()/recv() 函数也是如此，也从输入缓冲区中读取数据，而不是直接从网络中读取。
大小：socket默认的是1024×8=8192字节
特性：
- I/O缓冲区在每个TCP套接字中单独存在；
- I/O缓冲区在创建套接字时自动生成；
- 即使关闭套接字也会继续传送输出缓冲区中遗留的数据；
- 关闭套接字将丢失输入缓冲区中的数据。

实时性：
- TCP socket的send缓冲区有自己的timeout，因为默认开启Nagle算法，所以缓冲区没满的话要等到超时再发送。对实时性有要求可以用setsockopt关闭Nagle算法。
- 设置合适的缓存区的大小。

## Nagle算法
Nagle算法由John Nagle在1984年提出，这个算法可以减少网络中小的packet的数量，从而降低网络的拥塞程度。
为了减小网络开销，Nagle算法指出，当TCP发送了一个小的segment(小于MSS)，它必须等到接收了对方的ACK之后，才能继续发送另一个小的segment。那么在等待的过程中(一个RTT时间)，TCP就能尽量多地将要发送的数据收集在一起，从而减少要发送的segment的数量。
默认情况下，TCP开启了Nagle算法，然而Nagle算法并不是灵丹妙药，它会增加TCP发送数据的延迟。在一些要求低延迟的应用程序中(例如即时通讯应用)，则需要禁用Nagle算法。

Nagle算法的规则:
- 如果包长度达到MSS，则允许发送；
- 如果该包含有FIN，则允许发送；
- 设置了TCP_NODELAY选项，则允许发送；
- 未设置TCP_CORK选项时，若所有发出去的小数据包（包长度小于MSS）均被确认，则允许发送；
- 上述条件都未满足，但发生了超时（一般为200ms），则立即发送。

禁用：
```
int optval = 1;
setsockopt(sockfd, IPPROTO_TCP, TCP_NODELAY, &optval, sizeof(optval));
```
## Delayed ACK
TCP的 Delayed ACK 与Nagle算法有异曲同工之妙，Delayed ACK很好理解，当TCP接收到数据时，并不会立即发送ACK给对方，相反，它会等待应用层产生数据，以便将ACK和数据一起发送(在Linux最多等待40ms)。
为避免这种延迟的出现，需要做两件事：
- 设置TCP_NODELAY选项。
- 将客户端的两次write()合并成一个，避免服务端的Delayed ACK。

## TCP_CORK
Linux提供了TCP_CORK选项，如果在某个TCP socket上开启了这个选项，那就相当于在这个socket的出口堵上了塞子，往这个socket写入的数据都会聚集起来。下面几种情况都会导致这个塞子打开，这样TCP就能继续发送segment出来了。
- 程序取消设置TCP_CORK这个选项。
- socket聚集的数据大于一个MSS的大小。
- 自从堵上塞子写入第一个字节开始，已经经过200ms。
- socket被关闭了。

# 提高socket性能
- 禁用 Nagle 算法来减少传输延时
- 通过设置缓冲区的大小来提高 socket 带宽的利用
- 通过最小化系统调用的个数来降低系统调用的负载
- 以及使用可调节的内核参数来优化 Linux 的 TCP/IP 栈。

# 参考：
1. [参考](https://itbilu.com/nodejs/core/EJd85BikZ.html)
2. [Unix domain socket 的一些小结](https://blog.csdn.net/wlh_flame/article/details/6358795#)
3. [Nagle 算法与 TCP socket 选项 TCP_CORK](http://senlinzhan.github.io/2017/02/10/Linux的TCP-CORK/)
4. [提高 Linux 上 socket 性能-IBM](https://www.ibm.com/developerworks/cn/linux/l-hisock.html)