---
title: Flask vs Django
date: 2019-06-18 11:47:10
tags:
- Flask
- Python
- Django
categories: Python
---
两个框架同样都是Python web framework。

1. 项目规模
    - Flask是一个面向简单需求小型应用的“微框架（microframework）”。
    - Django更多面向大型应用。

2. SQL ORM
    - FLASK 不包含ORM，流行选用SQLAlchemy
    - Django包含ORM

3. bootstrapping
    - Flask没有，分离使用blurprint
    - Django有，内置在django-admin中.
    ```
        django-admin startproject hello_django
    ```
4. 易用性
    - Flask只要几行代码就能跑起一个demo，同样如果要扩展功能就要自己加库，更加灵活。
    - Django的demo 用脚手架生成也就好几个文件，setting更是多，但是基本功能都都自带，可以开箱即用。
