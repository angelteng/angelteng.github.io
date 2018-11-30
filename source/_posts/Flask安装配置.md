---
title: Flask安装配置
date: 2018-11-12 17:15:50
tags: 
- Python
- Flask
categories: Python
---
1. 安装
```
pip install uwsgi
pip install flask
```
2. uwsgi
    WSGI（Web Server Gateway Interface），定义了web服务器（nginx、apache、iis等）和 web应用（或者将web框架，flask、django等）之间的接口规范。也就是说，只要 web服务器和 web应用都遵守WSGI协议，那么 web服务器和 web应用就可以随意的组合。
 
配置uwsgi启动文件
```
# uwsgi.ini
[uwsgi]
socket = 127.0.0.1:5051            # 使用socket 
# http = 127.0.0.1:8888            # 使用http协议
pythonpath = /vagrant/flask。# 根项目根目录
module = index
wsgi-file = /vagrant/flask/index.py
callable = app                            # flask应用实例的名称
processes = 4
threads = 2
daemonize = /vagrant/flask/uwsgi/uwsgi.log
python-autoreload=1
status=/vagrant/flask/uwsgi/uwsgi.status
pidfile=/vagrant/flask/uwsgi/uwsgi.pid
```
uwsgi命令
```
uwsgi --ini uwsgi.ini             # 启动
uwsgi --reload uwsgi.pid     # 重启
uwsgi --stop uwsgi.pid        # 关闭
```
3. nginx配置
```
server {
    charset utf-8;
    client_max_body_size 128M;
    listen 80;
    server_name flask.local.com;
    root        /vagrant/flask;
    index       index.py;

    # 如果使用socket协议
    location / {
        include uwsgi_params;
        uwsgi_pass 127.0.0.1:5051;   # 配置uwsgi端口
    }
    # 如果使用http协议，则要配置方向代理
    location / {
        proxy_pass  http://127.0.0.1:8888;
    }
}
```
4. 业务代码例子
```
# index.py
from flask import Flask,request
import json

app = Flask(__name__)
app.debug = True

@app.route("/")
def helloWorld():
    return json.dumps({
        'code':200,
        'msg':123
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
```
5. 配置host ，访问即可