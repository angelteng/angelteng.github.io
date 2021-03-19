---
title: 从一次kswapd0占用cpu过高问题讲起
date: 2020-10-26 15:54:25
tags:
---
    最近在线上机器碰到kswapd0占用cpu过高（1100%），几乎吃满的所有cpu，所以这台机器其他服务都异常退出了。借此机会学习一下。
{% asset_img 2.png%}
1. 问题1: free -m 查看mem free是真的内存耗完了吗？buffer/cache是什么？  
查看free -m 命令。
{% asset_img 1.png%}
    - Buffers 是对原始磁盘块的临时存储，也就是用来缓存磁盘的数据，通常不会特别大（20MB 左右）。这样，内核就可以把分散的写集中起来，统一优化磁盘的写入，比如可以把多次小的写合并成单次大的写等等。
    - Cached 是从磁盘读取文件的页缓存，也就是用来缓存从文件读取的数据。这样，下次访问这些文件数据时，就可以直接从内存中快速获取，而不需要再次访问缓慢的磁盘。SReclaimable 是 Slab 的一部分。Slab 包括两部分，其中的可回收部分，用 SReclaimable 记录；而不可回收部分，用 SUnreclaim 记录。  
    - Buffer 是对磁盘数据的缓存，而 Cache 是文件数据的缓存，它们既会用在读请求中，也会用在写请求中。
    - 因此，free中看到的buffer/cache，实际也是可用的，一般看available是比较准确的可用内存值。

2. 什么是swap？为什么会swap？
    - swap space是磁盘上的一块区域，可以是一个分区，也可以是一个文件，或者是他们的组合。简单点说，当系统物理内存吃紧时，Linux会将内存中不常访问的数据保存到swap上，这样系统就有更多的物理内存为各个进程服务，而当系统需要访问swap上存储的内容时，再将swap上的数据加载到内存中，这就是我们常说的swap out和swap in。

3. kswapd0是什么？
    - kswapd0进程的作用：它是虚拟内存管理中，负责换页的，操作系统每过一定时间就会唤醒kswapd ，看看内存是否紧张，如果不紧张，则睡眠，在 kswapd 中，有2 个阀值，pages_hige 和 pages_low，当空闲内存页的数量低于 pages_low 的时候，kswapd进程就会扫描内存并且每次释放出32 个free pages，直到 free page 的数量到达pages_high。通过阻止kswapd0进程过渡活跃地消耗CPU的方法是设置大页内存。

4. 第一次尝试  
    - 调整/proc/sys/vm/swappiness 参数，默认60，调整为10，表示内存剩下10%的时候才触发swap。
    - 但是遗留了一个问题：为什么kswapd0进程一直驻留，但从vmstat看si so 为0？为什么这个进程的cpu是user使用不是sys？

5. 继续查找：
    - 后来找到了一篇文章《kswapd0挖矿病毒查杀过程》，通过netstat -antlp 发现了一个同样荷兰的ip 45.9.148.99通过rsync在/root/.configrc/a 植入了kswapd0文件。初步判断是这个假装swap的进程其实值挖矿病毒。

6. 解决：
    - kill调病毒进程。
    - 删除可疑文件。
    - 删除病毒创建的计划任务。


7. 参考连接：
    - [kswapd0挖矿病毒查杀过程](https://codenie.github.io/post/kswapd0-wa-kuang-bing-du-cha-sha-guo-cheng/)
    - [Linux交换空间（swap space）](https://segmentfault.com/a/1190000008125116)
    - [内存篇 | 02 | 怎么理解内存中的Buffer和Cache？](https://zhuanlan.zhihu.com/p/146877464)