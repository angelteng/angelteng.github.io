---
title: 'Python项目相关路径配置'
date: 2018-11-14 09:14:37
tags: Python
---
1. python相关环境变量
- PYTHONPATH : PYTHONPATH是Python搜索路径，默认我们import的模块都会从PYTHONPATH里面寻找。
- PYTHONSTARTUP: Python启动后，先寻找PYTHONSTARTUP环境变量，然后执行此变量指定的文件中的代码。
- PYTHONCASEOK: 加入PYTHONCASEOK的环境变量, 就会使python导入模块的时候不区分大小写.
- PYTHONHOME: 另一种模块搜索路径。它通常内嵌于的PYTHONSTARTUP或PYTHONPATH目录中，使得两个模块库更容易切换。

2. 配置LD_LIBRARY_PATH
[LD_LIBRARY_PATH is used by your program to search for directories containing the libraries after it has been successfully compiled and linked.](https://www.cnblogs.com/icxy/p/7943996.html)
执行二进制文件时的动态库搜索路径
```
>>> vim  ~/.bashrc
......
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib
>>> source ~/.bashrc
>>> 重启进程
````
3. 配置PYTHONPATH
Python模块路径
```
>>> vim /etc/profile
.......
source /apps/sh/flask_local_com.sh
>>> vim /apps/sh/flask_local_com.sh
.......
export FLASK_DEBUG=1;
export PYTHONPATH=/vagrant/project/libs:$PYTHONPATH;
>>> source /etc/profile
```