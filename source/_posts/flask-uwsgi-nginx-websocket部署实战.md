---
title: nginx+gunicorn+flask-sockerio docker部署实战
date: 2019-03-01 16:49:35
tags:
- Python
- Docker 
categories: Python
---
部署方案：flask+uwsgi服务部署一个容器（服务使用flask-socketio实现websocket)、nginx部署一个容器
## 如何配置：
### nginx
```
    server {
        listen 80;
        server_name test.local.com;
        error_log /apps/logs/error_nginx.log ;
        access_log /apps/logs/access_log.log ;

        location / {
            include proxy_params;
            ;;; 如果include proxy_params 没找到 替换成
            ; proxy_set_header Host $http_host;
            ; proxy_set_header X-Real-IP $remote_addr;
            ; proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            ; proxy_set_header X-Forwarded-Proto $scheme;

            proxy_pass http://host_ip:8002;
        }

        location /socket.io {
            include proxy_params;
            proxy_http_version 1.1;
            proxy_buffering off;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "Upgrade";
            proxy_pass http://host_ip:8002/socket.io;
        }
    }
```
注意：host_ip为宿主机ip
### uwsgi 
```
    [uwsgi]
    # uwsgi 启动时所使用的地址与端口
    http-socket = :8001

    master = true
    ;lazy-apps = true
    # 指向网站目录
    chdir = /app

    # python 启动程序文件
    wsgi-file = uwsgi_entry.py
    # python 程序内用以启动的 application 变量名
    callable = app

    # 处理器数
    processes = 8
    ;listen = 1024
    gevent = 100
    http-websockets = true 
```
### uwsgi_entry.py
```
    from config import app_config
    from app import create_app
    from flask_socketio import SocketIO
    from app.services.message_push import MessagePush

    app = create_app(app_config)
    # 初始化socket 注意async_mode
    socketio = SocketIO(app, async_mode="threading")
    # nameSpace以类形式初始化
    MessagePushHelper = MessagePush('/test')
    socketio.on_namespace(MessagePushHelper)

    # 实际nginx转发的端口是socket运行的端口 注意host配置0.0.0.0
    socketio.run(app, host="0.0.0.0", port=8002, use_reloader=False)
```
### 后续改用gunicorn
后面发现这个方案其实只是利用uwsgi起了个嵌入式服务器，所有请求根本没有经过uwsgi服务器。
后面看官方文档，改成
```
    [uwsgi]
    # uwsgi 启动时所使用的地址与端口
    http-socket = :8001

    master = true
    ;lazy-apps = true
    # 指向网站目录
    chdir = /app

    # python 启动程序文件
    wsgi-file = uwsgi_entry.py
    # python 程序内用以启动的 application 变量名
    callable = app

    # 处理器数
    processes = 1
    ;listen = 1024
    gevent = 100
    http-websockets = true 

    ........
    uwsgi_entry.py
    
    from config import app_config
    from app import create_app
    from flask_socketio import SocketIO
    from app.services.message_push import MessagePush

    # 初始化socket 注意async_mode
    socketio = SocketIO()
    app = create_app(app_config,socketio)
    # nameSpace以类形式初始化
    MessagePushHelper = MessagePush('/test')
    socketio.on_namespace(MessagePushHelper)

    .....
    def create_app(app,socketio):
    ....
    socketio.init_app(app, message_queue='redis://'+ config.HOST_IP) #mutil thread
    return app
```
测试发现，还是有间隔400出现，前端不断的connect,disconnect
尝试n个方法无果，改用gunicorn服务器
gunicorn配置
```
    #  -*- coding: utf-8 -*-
    # 预加载资源
    preload_app = True
    # 绑定
    bind = "0.0.0.0:8002"
    # 进程数
    workers = 1
    # 线程数
    threads = 10
    # 等待队列最大长度,超过这个长度的链接将被拒绝连接
    backlog = 100
    # 工作模式
    # worker_class = "egg:meinheld#gunicorn_worker"
    worker_class = "geventwebsocket.gunicorn.workers.GeventWebSocketWorker"
    # 最大客户客户端并发数量,对使用线程和协程的worker的工作有影响
    worker_connections = 100
``` 
因为websocket需要粘性会话，所以worker只能设为1
[gunicorn不同woker type](https://medium.com/@genchilu/淺談-gunicorn-各個-worker-type-適合的情境-490b20707f28)
其余代码跟上面一样，目前测试稳定。

## 如何访问
1. 容器间通讯，目前通过docker run -p 3306:3306 暴露端口给宿主机，容器内部服务访问通过 宿主机ip+暴露的端口进行访问，[其他方法](https://birdben.github.io/2017/05/02/Docker/Docker实战（二十七）Docker容器之间的通信/)
2. mysql 持久化：通过 -v /home/data/mysql_data/:/var/lib/mysql/ 保存数据文件 默认路径可以查看 /etc/my.cnf里的datadir配置
3. 由于uwsgi_entry.py 直接运行了 socketio.run命令，实际上所有的服务是通过这个命令的端口访问的，-p暴露的也是这里的端口
4. uwsgi_docker.ini 要配置http-socket模式

## 问题与方案
1. 逻辑在子线程进行websocket的emit时，参考flask-socketio的文档：
```
    In all the examples shown until this point the server responds to an event sent by the client. But for some applications, the server needs to be the originator of a message. This can be useful to send notifications to clients of events that originated in the server, for example in a background thread. The socketio.send() and socketio.emit() methods can be used to broadcast to all connected clients:

    def some_function():
        socketio.emit('some event', {'data': 42})

    Note that socketio.send() and socketio.emit() are not the same functions as the context-aware send() and emit(). Also note that in the above usage there is no client context, so broadcast=True is assumed and does not need to be specified.
```
注意需要使用 socketio.emit方法，默认是广播的。
socketio 是flask-socketio初始化的实际，注意初始化时配置 async_mode="threading" 参数，否则emit不成功
```
    async_mode – The asynchronous model to use. See the Deployment section in the documentation for a description of the available options. Valid async modes are threading, eventlet, gevent and gevent_uwsgi. If this argument is not given, eventlet is tried first, then gevent_uwsgi, then gevent, and finally threading. The first async mode that has all its dependencies installed is then one that is chosen

    有效的异步模式参数是 threading, eventlet, gevent, gevent_uwsgi。
```
2. 时区： 在docker run 时增加参数 -v /etc/localtime:/etc/localtime
[其他方法](https://brickyang.github.io/2017/03/16/Docker%20中如何设置%20container%20的时区/)

3. async_mode=eventlet 有问题，[see this](https://stackoverflow.com/questions/34581255/python-flask-socketio-send-message-from-thread-not-always-working)