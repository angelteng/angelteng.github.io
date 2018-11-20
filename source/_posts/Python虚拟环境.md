---
title: Python虚拟环境
date: 2018-11-9 17:16:24
tags: Python
---
1. 函数 str() 用于将值转化为适于人阅读的形式
    repr() 转化为供解释器读取的形式（如果没有等价的语法，则会发生SyntaxError异常）

2. 虚拟环境
```
# 创建虚拟环境
virtualenv --no-site-package venv
# 启用
source ./venv/bin/activate
# 停用
deactivate
```
3. 可执行python脚本 
```
#!/usr/bin/env python3.5
```
4. 记录依赖变更
requirements.txt是一个常常被许多Flask应用用于列出它所依赖的包的文本文件。它是通过pip freeze > requirements.txt生成的。 使用pip install -r requirements.txt，你就能安装所有的包。