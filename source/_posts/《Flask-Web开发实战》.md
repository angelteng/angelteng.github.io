---
title: 《Flask Web开发实战》笔记
date: 2019-07-24 10:26:27
tags: 
- Python
- Flask
---
# 基础
1. pipenv 使用
``` python
    pipenv install #创建.venv/ pipfile pipfile.lock
    pipenv install flask
    pipenv shell # source .venv/bin/activate
```
2. 动态路由
```python
    @app.route('/greet',defaluts = {"name":"defaultname"})
    @app.route('/greet/<name>')
    def greet(name):
        return "welcome %s" % name
```
3. Flask内置了简单的开发服务器（由Werkzeug提供），旧的app.run()方法已不建议使用。
```python
    flask run
    """"
    查找规则：
    1. 当前目录下寻找app.py wsgi.py，并从中寻找名为app/application的实例
    2. 从环境变量读取FLASK_APP的模块名/导入路径，寻找名为app/application的实例
    3. 如果安装了python-dotenv，启动时会从.flaskenv .env加载环境变量
```
4. 检测文件变化 watchdog
5. flask的扩展包 falsk_xxxx
6. flask自定义命令
```python
    # flask hello
    @app.cli.command()
    def hello():
        click.echo('Hello')
```
