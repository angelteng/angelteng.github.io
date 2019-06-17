---
title: flask 使用
date: 2018-11-13 17:15:19
tags: 
- Python
- Flask
categories: Python
---
1. 开启debug模式
- 使用uswgi
```
from werkzeug.debug import DebuggedApplication
app.wsgi_app = DebuggedApplication( app.wsgi_app, True )

if __name__ == '__main__':
    app.run(debug=True)
```
- 不使用uswgi
```
>>> export FLASK_DEBUG=1 && flask run
>>>  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
Nginx 改为反向代理到127.0.0.1:5000
```

2. 目录结构
![目录](0.png)
[作者参考](https://lepture.com/en/2018/structure-of-a-flask-project)
[论坛参考](https://www.v2ex.com/t/467423)
图灵《 Flask Web 开发》董伟明《 Flask Web 开发实战》

3. 绝对路径 './'
相对路径 '../'