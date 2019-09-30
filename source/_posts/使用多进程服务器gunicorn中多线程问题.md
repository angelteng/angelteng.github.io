---
title: 使用多进程服务器gunicorn中多线程问题
date: 2019-04-28 14:49:15
tags: 
- Python
- Gunicorn
categories: 后端
---
# 问题描述：
场景：
gunicorn + flask
gunicorn.conf:
```
    worker = 1  # 1个工作进程
    worker_class = "geventwebsocket.gunicorn.workers.GeventWebSocketWorker" # 因为使用了websocket
```
在flask 入口处新增了一个子线程做redis的监听工作
```
    import threading
    def listen_redis():
        while True:
            print(threading.currentThread())
            .....
            print('get redis')
    t = threading.Thread(target=listen_redis)
    t.start()
```
问题1: 在使用gunicron运行的时候，发现子进程也运行了listen_redis的循环。
问题2: 同时由两个线程进行while true的操作，发现有时候一个while true断了再也不工作了。

# 问题跟踪：
在查看gunicron的源码可以发现：
/venv/lib/python3.x/site-packages/gunicorn/arbiter.py
```
    # line: 575
    def spawn_worker(self):
        self.worker_age += 1
        worker = self.worker_class(self.worker_age, self.pid, self.LISTENERS,
                                   self.app, self.timeout / 2.0,
                                   self.cfg, self.log)
        self.cfg.pre_fork(self, worker)
        pid = os.fork()  #是在fork之后出现的“多余的子线程”
        if pid != 0:
            worker.pid = pid
            self.WORKERS[pid] = worker
            return pid
```
通过print(threading.currentThread())可以看到log：
主进程的循环打印出来：
```
    <Thread(Thread-2, started 140048726495560)>
```
而子进程的循环打印出来的是：
```
    <_DummyThread(DummyThread-4, started daemon 140048726495560)>
```
可以确定的是，多了一个不是由threading创建的“虚拟线程”

然后查看gunicron对线程做了什么的时候发现[这个问题](https://github.com/benoitc/gunicorn/issues/1836)
虽然不是同一个问题，但是这个说到了 monkey_patch对threading做了补丁
然后发现在 \__init\__.py 使用了猴子补丁，是为了websocket，使用了multiple workers时需要共享client connect，详情可以看[flask-socketio文档](https://flask-socketio.readthedocs.io/en/latest/#Using Multiple Workers¶)Using Multiple Workers这一章。
```
    If eventlet or gevent are used, then monkey patching the Python standard library is normally required to force the message queue package to use coroutine friendly functions and classes.
```
然后把猴子补丁改成：
```
    from gevent import monkey
    monkey.patch_all(thread=False)
```
之后，发现“虚拟线程”没有被创建了。
但是偶尔会有下面报错，不影响正常功能，暂时不知道原因：
```
Exception ignored in: <module 'gevent.threading' from '/demo/venv/lib/python3.5/site-packages/gevent/threading.py'>
AttributeError: module 'gevent.threading' has no attribute '_after_fork'
```

# 解析
1. 首先明确的是，os.fork()创建出来对子进程并不会继承父进程的子线程。在[fork(2)-Linux Man Page](http://linux.die.net/man/2/fork)，中的描述：
```
    The child process is created with a single thread--the one that called fork(). The entire virtual address space of the parent is replicated in the child, including the states of mutexes, condition variables, and other pthreads objects; the use of pthread_atfork(3) may be helpful for dealing with problems that this can cause.
```
也就是说，在Linux中，fork的时候只复制当前线程到子进程。
2. 那么，monkey_patch究竟做了什么?
monkeypatch修改了threading标准库中的_start_new_thread方法, Condition类等，创建了一个greenlet而不是真正的线程，然后就会在fork的时候被复制了。因此，也可以在gunicron的配置文件中，在on_starting的hook中创建真正的线程。
gevent是第三方库，通过greenlet实现协程，其基本思想是：当一个greenlet遇到IO操作时，比如访问网络，就自动切换到其他的greenlet，等到IO操作完成，再在适当的时候切换回来继续执行。由于IO操作非常耗时，经常使程序处于等待状态，有了gevent为我们自动切换协程，就保证总有greenlet在运行，而不是等待IO。
事实上，gunicron在使用gevent的时候，已经monkey patch了一次，如果patch多次，将会求多次中参数为True的并集。
```
    # venv/lib/python3.5/site-packages/gunicorn/workers/ggevent.py:65
    def patch(self):
    from gevent import monkey
    monkey.noisy = False

    # if the new version is used make sure to patch subprocess
    if gevent.version_info[0] == 0:
        monkey.patch_all()  # 默认值socket=True, dns=True, time=True, select=True, thread=True, os=True, ssl=True， httplib=False, subprocess=True, sys=False, aggressive=True, Event=False, builtins=True, signal=True
    else:
        monkey.patch_all(subprocess=True)
```
3. 问题2: 从gevent的[文档](http://sdiehl.github.io/gevent-tutorial/)，可以知道，同一时间，只能有一个greenlet在运行，所以如果一个greenlet阻塞了，另一个greentlet就不可能运行，可以通过在while true末尾添加gevent.sleep(0.1)，把控制权（有可能）交给另外一个greenlet。

# 最终方案：
```
    # 方案一：阻塞事件使用线程
    from gevent import monkey
    monkey.patch_all(thread=False)

    from threading
    ta = threading.Thread(target=task)
    ta.start

    while true:
        ....
        # gevent.sleep(0.1)

    # 方案二：阻塞事件使用进程
    from gevent import monkey
    monkey.patch_all()

    from multiprocess import Process
    p = Process(target=task)
    p.start()

    while true:
        ...
```

参考:
[谨慎使用多线程中的fork](https://www.cnblogs.com/liyuan989/p/4279210.html)
[eventlet 之 monkeypatch 带来的若干兼容性问题实例分析](https://segmentfault.com/a/1190000013096677)
[monkey.patch_all and gunicorn with more than 1 worker](https://github.com/benoitc/gunicorn/issues/1056)
[源码分析之gevent monkey.patch_all实现原理](http://xiaorui.cc/2016/04/27/源码分析之gevent-monkey-patch_all实现原理/)
[python异步 I/O模块gevent](http://www.361way.com/python-gevent/5329.html)
[gevent-廖雪峰](https://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001407503089986d175822da68d4d6685fbe849a0e0ca35000)
[gunicorn源码解析](https://github.com/Junnplus/blog/issues/9)
[深入理解uwsgi和gunicorn网络模型[上]](http://xiaorui.cc/2017/02/16/深入理解uwsgi和gunicorn网络模型上/)