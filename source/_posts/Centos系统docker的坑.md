---
title: Centos系统docker的坑
date: 2018-11-30 15:12:20
tags: 
- docker
- 系统
categories: 系统
---
环境：CentOS Linux release 7.1.1503 (Core) 
dockerfiles 中有
```
RUN mv /app/docker/localtime /etc/localtime
......
RUM rm /app/docker
```
docker build 过程中发现报错
```
mv: can't rename '/app/docker/localtime': Invalid argument
The command '/bin/sh -c mv /app/docker/localtime /etc/localtime' returned a non-zero code: 1
```
而同样的脚本在另外一个Ubuntu系统下没有这样的报错
从 docker info中可以看到
![不正常系统](0.png)
Centos7
![正常系统](1.png)
Ubuntu16.04
并且可以看到报错信息
```
WARNING: overlay: the backing xfs filesystem is formatted without d_type support, which leads to incorrect behavior.
         Reformat the filesystem with ftype=1 to enable d_type support.
         Running without d_type support will not be supported in future releases.
```
Centos7 发行版默认的Kernel版本是3.10，但是Overlay2存储驱动需要4.0以上的kernel版本支持，所以默认使用overlay 并且不支持d_type， 才导致这个报错。
[具体](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/7.2_release_notes/technology-preview-file_systems)
解决方法一：
格式化 XFS 系统，添加ftype=1

```
# 查看当前系统xfs
xfs_info /
如果 ftype =0 表示不支持d_type
省略具体格式化方法
```
解决方法二：
修改 storage driver 为 devicemapper
```
vim /etc/docker/daemon.json
增加
{
    ...
    "storage-driver": "devicemapper"
}
```


[docker疑难杂症](http://blog.51cto.com/foxhound/1841487)
[docker文件系统参考](https://www.jianshu.com/p/00ffd8df6010)
[github上的讨论](https://github.com/moby/moby/issues/15314)

