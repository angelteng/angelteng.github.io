---
title: Python PIL docker 环境部署问题
date: 2019-01-10 11:02:58
tags:
- Python
categories: Python
---
1. Python3中需要pip install Pillow
2. docker 部署中 dockerfile 文件需要添加
```
    RUN apk add --no-cache libjpeg-turbo
    RUN apk add --no-cache --virtual ... jpeg-dev zlib-dev ... 
```
如果不add jped-dev 在docker build 时会报错
```
    Command "/usr/bin/python3.6 -u -c "import setuptools, tokenize;__file__='/tmp/pip-build-7he1rs0x/Pillow/setup.py';f=getattr(tokenize, 'open', open)(__file__);code=f.read().replace('\r\n', '\n');f.close();exec(compile(code, __file__, 'exec'))" install --record /tmp/pip-jfoplyfd-record/install-record.txt --single-version-externally-managed --compile" failed with error code 1 in /tmp/pip-build-7he1rs0x/Pillow/
    You are using pip version 9.0.3, however version 18.1 is available.
    You should consider upgrading via the 'pip install --upgrade pip' command.
```
成功打包后，如果不add libgjpeg-turbo
会在import PIL时报错
```
    libjpeg.so.8: cannot open shared object file: No such file or directory
```