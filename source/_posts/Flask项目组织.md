---
title: Flask项目组织
date: 2018-11-16 16:42:57
tags: 
- Python
- Flask
categories: Python
---
1. 一个基于 WSGI 的 Python web 应用必须有一个实现实际的应用的中心调用对象。在 Flask 中，中心调用对象是一个 Flask类的实例
```
app = Flask(__name__)
```
- 保证实例的唯一性 
- 当进行单元测试的时候，创建一个最小应用用于测试特定的功能，会用到多应用
- 使用显式对象时，可以继承基类Flask， 以便于修改特定的功能
- Flask 需要包的名称。当你创建一个 Flask 实例时， 通常会传递 \__\_name\__\_ 作为包的名称。 Flask 根据包的名称来载入也模块相关的正确资源。
- “显式比隐式更好”
[Flask设计思路]（https://dormousehole.readthedocs.io/en/latest/design.html）

2. 使用[蓝图](http://docs.jinkan.org/docs/flask/blueprints.html)进行模块化组织
Flask 用 蓝图（blueprints） 的概念来在一个应用中或跨应用制作应用组件和支持通用的模式。蓝图很好地简化了大型应用工作的方式，并提供给 Flask 扩展在应用上注册操作的核心方法。
例子：
```
# routes/identify.py
from flask import Blueprint

identify = Blueprint('identify', __name__)

@identify.route('/check-pics-quality',methods=['POST', 'GET'])
def check_pics_quality():
    pass;


# routes/__init__.py
from .identify import identify
def init_app(app):
    app.register_blueprint(identify, url_prefix='/identify')   
```
