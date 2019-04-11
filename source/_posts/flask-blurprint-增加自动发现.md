---
title: flask blurprint 增加路由自动发现
date: 2019-03-05 16:53:53
tags:
- Python
categories: Python
---
路由自动发现基于约定代码结构及命名规范实现的。
例子：
约定 [name]_api.py 输出对象名：[name]_bp
目录结构:
----- view
    - __init__.py
    - user_api.py
    - history_api.py
    - type_api.py

在文件\__init\__.py中，原本写法
```
    from .user_api import user_bp
    from .history_api import history_bp
    from .type_api import type_api

    blue_print = [user_bp, history_bp, type_api]
    ......
    ......
    for bp in blue_prints:
        app.register_blueprint(bp)
```
现在改成
```
    import os
    import re
    path = os.getcwd() + '/app/views'

    # 路由自动查找
    blue_prints = []
    for root, dirs, files in os.walk(path):
        for f in files:
            if re.match('(.*?)_api.py', f):
                name = f.replace('_api.py', '')
                _temp = __import__('app.views.'+name+'_api', fromlist=[name+'_bp']) 
                if(hasattr(_temp,name+'_bp')):
                    blue_prints.append(getattr(_temp,name+'_bp'))
    ......
    ......
    for bp in blue_prints:
        app.register_blueprint(bp)
```

