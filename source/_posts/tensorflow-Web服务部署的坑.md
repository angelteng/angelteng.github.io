---
title: tensorflow Web服务部署的坑
date: 2019-04-30 14:13:32
tags:
---
# 问题场景：
由于需要部署一个基于tensorflow的算法Web服务，使用了uwsgi+flask去部署。
uwsgi 使用了多进程，参数为：
```
    [uwsgi]
    socket = 0.0.0.0:5051
    chdir = /vagrant/images_check
    wsgi-file = /vagrant/images_check/uwsgi_entry.py
    callable = app
    processes = 4
    ;harakiri = 30
    log-format = %(addr) - %(user) [%(ltime)] "%(method) %(uri) %(proto)" %(status) %(size) "%(referer)" "%(uagent)" %(msecs)ms
```
而算法服务初始化，在入口出使用了queue去初始化，本来的目的是使多个进程都去同一个queue里获取算法服务的实例
```
    q = Queue() 
    for i in range(multiprocessing.cpu_count()):
        bqc = CheckImage()
        q.put(bqc)
```
然而发现，运行之后，只有一个进程是能正确运行的，其他进程会阻塞在tf.session.run无法返回

# 问题跟踪
1. 因为在uwsgi中，工作进程是fork()主进程，获得了一个主进程“拷贝”的内存，所以每个进程都会有一个queue。
2. tensorflow不是进程安全的，所以上面“拷贝”内存的操作，可能倒是tensorflow hang了。
在tensorflow issue有类似的提问，[Session got stuck after fork](https://github.com/tensorflow/tensorflow/issues/2448)
```
The in-process session (i.e. tf.Session() with no arguments) is not designed to be fork()-safe. If you want to share a set of devices between multiple processes, create a tf.train.Server in one process, and create sessions that connect to that server (with tf.Session("grpc://...")) in the other processes.
```
3. 这篇文章中提到[机器学习web服务化实战：一次吐血的服务化之路](https://www.cnblogs.com/haolujun/p/9778939.html)，的方法，在gunicorn的配置中实例化算法服务，gunicorn可以保证配置文件中的代码只运行一次。同时利用gc.freeze()把截止到当前的所有对象放入持久化区域，不进行回收，从而model占用的内存不会被copy-on-write。但是按照这个方法发现这个实例依然在fork的时候被copy了。

# 问题解决 
1. 方案一：改成了在每个进程初始化之后，初始化一个算法服务实例，根据cpu核数配置uwsgi工作进程数量
```
    @app.before_first_request
    def first_quest():
        q = Queue()
        for i in range(1):
        bqc = CheckImage()
        q.put(bqc)
```
2. 方案二；
    使用redis/mc等中间件。但是有可能有序列化失败的问题。
3. 使用tensorflow server

# 最后
在gunicron中，配置preload_app = True是可以预加载资源的，但是fork工作进程还是可能出现坑。

参考:
[Session got stuck after fork](https://github.com/tensorflow/tensorflow/issues/2448)
[How to serve tensorflow model using flask+uwsgi?](https://stackoverflow.com/questions/49227958/how-to-serve-tensorflow-model-using-flaskuwsgi)
[机器学习web服务化实战：一次吐血的服务化之路](https://www.cnblogs.com/haolujun/p/9778939.html)
[fork-safe和thread-safe简介](http://timd.cn/fork-safety-and-thread-safety/)
[【已解决】Flask的gunicorn中多进程多worker如何共享数据或单实例](https://www.crifan.com/flask_gunicorn_multiple_process_worker_share_data_or_singleton/)


