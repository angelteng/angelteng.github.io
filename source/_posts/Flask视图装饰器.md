---
title: Flask视图装饰器
date: 2018-11-19 15:13:13
tags: 
- Python
- Flask
categories: Python
---
框架已有：
```
# 路由装饰器
@app.route

# 登陆装饰器
from flask_login import login_required, current_user
@app.route('/')
@login_required
def account():
    pass

# 缓存装饰器
from flask_cache import Cache
@app.route('/')
@cache.cached(timeout=60)
def index():
    pass
```
自定义：
```
# 定义一个装饰器
def check_expired(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # 一些逻辑
        return func(*args, **kwargs)
    return decorated_function

# 使用
@check_expired
def get_something():
    pass;

# 定义一个类装饰器
class Timeit(object):
    def __init__(self, func):
        self.func = func
    def __call__(self, *args, **kwargs):
        print("invoking Timer")
    def __get__(self, instance, owner):
        return lambda *args, **kwargs: self.func(instance, *args, **kwargs)

# 使用
class A(object):
    @Timeit
    def func(self):
        time.sleep(1)
        return "invoking method func"
```

[参考](https://spacewander.github.io/explore-flask-zh/6-advanced_patterns_for_views_and_routing.html)