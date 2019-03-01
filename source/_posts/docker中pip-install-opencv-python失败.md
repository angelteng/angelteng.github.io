---
title: docker部署uwsgi+flask问题
date: 2019-01-30 11:04:47
tags: 
- docker 
categories: docker
---
问题：
docker中pip install opencv-python失败.

dockerFile中
```
From Alpine
....

RUN pip3 install opencv-python
```
docker build 时出现报错，即使升级了pip之后:
Could not find a version that satisfies the requirement opencv-python (from version: ) 
No matching distribution found for opencv-python

原因：
[from stackoverflow](https://stackoverflow.com/questions/50950588/trouble-installing-opencv-in-docker-container-using-pip)
I've just run into this issue as well. It turns out that this is not working because opencv-python does not have any prebuilt wheels for Alpine (the distribution you're using as your base docker image).

The conversation in this issue on the opencv-python package explains why this happens in greater detail. The TL;DR is: if you really need to use Alpine, you can try forcing the installation of the manylinux wheel for opencv-python, but this can break. Your best option if you need to keep Alpine is to build the module from source. Since you are running this on OpenFAAS, I suspect you will want to keep your size low, so building from source may be a good option for you.

If you're not attached to Alpine, I would suggest moving to a different base docker image. If you're not sure which image to use as your base, I would recommend python:3.7-slim, since it will come with Python already installed (substitute 3.7 for whichever version you are using, but really. . . 3.7 is nice). With this container, you can simply run pip install opencv-python numpy scipy to have all three of your desired packages installed. The rest of your Dockerfile should work mostly unmodified; you will just need to install/uninstall curl using apt instead of apk.

简单来说就是，Alpine中没有prebuild opencv-python,如果一定要用Alpine，可以强制下载编译，但是有可能出错。也可以更换使用 python:3.x-slim镜像。
最后Dockerfile:
```
    FROM python:3.5.6-slim-stretch
    WORKDIR /app
    ADD ....

    RUN apt-get update && apt-get install -y --no-install-recommends apt-utils && \
    apt-get install -y \
            libc6-dev \
            gcc \
            mime-support vim libtiff5 libglib2.0-0 libsm6 libxext6 libxrender1 libxext-dev libpcre3 libpcre3-dev && \
    pip3 install --no-cache-dir uWSGI \
        && apt-get remove -y \
            gcc \
            libc6-dev \
        && rm -rf /var/lib/apt/lists/* && \
    pip3 install setuptools==39.1.0 && \ 
    pip3 install -r requirements.txt 

    ENV LD_LIBRARY_PATH=/app/project/services/libs
    ENV PYTHONPATH=/app/project/services/libs

    CMD ["uwsgi", "--ini", "uwsgi_docker.ini"]
```
在部署docker过程中会遇到：
![error](https://upload-images.jianshu.io/upload_images/14827444-c750540543c5fc4a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
此时需要删掉uwsgi的配置 plugin=python
最后uwsgi.ini配置：
```
    [uwsgi]
    socket = 0.0.0.0:5051
    chdir = /app
    wsgi-file = /app/app.py
    callable = app
    processes = 4
    threads = 2
```
nginx配置：
```
    server {
        charset utf-8;
        client_max_body_size 128M;

        listen 80;

        server_name xxx.local.com;
        root        /vagrant/xxx;
        index       index.py;

        location / {
            include         uwsgi_params;
            uwsgi_pass      127.0.0.1:5051;
        }
    }
```