---
title: Python数据结构
date: 2018-11-05 17:20:10
tags: 
- Python
categories: Python
---
1. Python手册： https://docs.python.org/3/reference/index.html#reference-index
2. 数据结构：列表[]、元组()、集合{}、字典{k:v}
3. 循环技巧：
```
# 列表循环技巧：
for index, value in enumerate(['tic', 'tac', 'toe']):

# 字典循环技巧：
knights = {'gallahad': 'the pure', 'robin': 'the brave'}
for key, value in knights.items():

#列表打包
questions = ['name', 'quest', 'favorite color']
answers = ['lancelot', 'the holy grail', 'blue']
for q, a in zip(questions, answers):
    print('What is your {0}?  It is {1}.'.format(q, a))
```
4. 推导式
```
# 列表推导式
squares = [x**2 for x in range(10)]
mutiSquares = [[row[i] for row in matrix] for i in range(4)]    #嵌套的列表推导式

# 集合推导式
a = {x for x in 'abracadabra' if x not in 'abc'}
# >>> {'r', 'd'}

# 字典推导式
a = {x: x**2 for x in (2, 4, 6)}
# >>> {2: 4, 4: 16, 6: 36}
```
5. 操作符：
- not 
- and, or : 参数从左向右解析，一旦结果可以确定就停止
```
string1, string2, string3 = '', 'Trondheim', 'Hammer Dance'
non_null = string1 or string2 or string3
# non_null  -> 'Trondheim'
```
- in, not in
- is, is not 