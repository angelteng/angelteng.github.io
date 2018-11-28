---
title: HTTP2改造实践
date: 2018-11-21 10:59:37
tags: HTTP
---
HTTP2特点：
1.  新的二进制格式：HTTP1.x的解析是基于文本，HTTP2.0的协议解析决定采用二进制格式
2.  多路复用

![image.png](https://upload-images.jianshu.io/upload_images/14827444-a9336eb314e24f99.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

3.  header压缩
4.  服务端推送
5.  HTTP2.0其实可以支持非HTTPS的，但是现在主流的浏览器像chrome，firefox表示还是只支持基于 TLS 部署的HTTP2.0协议，所以要想升级成HTTP2.0还是先升级HTTPS为好

http1.1问题：

1.  链接安全性
2.  建立链接消耗
3.  header内容过大
4.  keep－alive（与http2区别：线头阻塞）浪费

[参考](https://imququ.com/post/http2-and-wpo-2.html)

实践：
为了升级图片域域名到HTTP2新域名，可选方案要不就统一后端接口处理匹配替换，要不就前端拿到数据后匹配替换。
由于考虑到后端接口分布比较零散，本次采用前端替换方案。

步骤：
1. 需要获取所有接口数据后，替换图片域名：扩展了jquery的ajax，ajaxsetting.dataFilter处理返回是json的数据，ajaxsetting.beforeSend重写callback方法，先处理图片域名，再执行用户callback
2. 增加了dns-prefetch属性，预解析图片域dns
3. 增加了图片容错处理，MutationObserve监听dom结构