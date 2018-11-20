---
title: Python的模块与包
date: 2018-11-7 10:18:29
tags: Python
---
Python模块
1. 引入模块
```
# 方式一
import module
module.function('xxx')
# 方式二
from module import *  #导入所有除了以下划线( _ )开头的命名
# from module import function,function1,function2
function('xxx')
```
2. 以脚本方式运行模块，__name__ 被设置为 "__main__"
```
>>> python module.py
if __name__ == "__main__":
    pass
```
3. 模块搜索路径
- 当前目录
- sys.path 变量中给出的目录列表
  - 输入脚本的目录（当前目录）
  - 环境变量 PYTHONPATH表示的目录列表中搜索
  - Python 默认安装路径中搜索
4. 模块编译：
- 为加快加载模块的速度，Python 会在 \__pycache\__ 目录下以 module.version.pyc 名字缓存每个模块编译后的版本
- Python 会检查源文件与编译版的修改日期以确定它是否过期并需要重新编译
- Python会永远重新编译而且不会存储直接从命令行加载的模块
- 如果没有源模块它不会检查缓存
5. 标准模块库，是一个依赖于底层平台的配置选项集合
6. 包
![包结构](https://upload-images.jianshu.io/upload_images/14827444-2af47c49f2897893.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
- 必须包含\__\_init\___.py
- \__\_all\___ = ["echo", "surround", "reverse"]  指定*导入的子模块集合
- 如果没有定义 \__\_all\___ ， from sound.effects import * 语句__不会__从 sound.effects 包中导入所有的子模块
- 导入方式
```
import sound.effects.echo
sound.effects.echo.echofilter(input, output, delay=0.7, atten=4)

from sound.effects import echo
echo.echofilter(input, output, delay=0.7, atten=4)
