---
title: 利用hexo搭建个人blog
date: 2018-11-20 15:13:48
tags: hexo, node
---
1. 安装
```
>>> npm install -g hexo
>>> cd /blog-project
>>> hexo init
>>> npm install
>>> hexo g
>>> hexo server #启动一个本地服务器
```
2. 修改配置
```
#修改 _config.yml
....
# URL
## If your site is put in a subdirectory, set url as 'http://yoursite.com/child' and root as '/child/'
url: https://angelteng.github.io/blog/  # git仓库地址
root: /blog/   #根目录
permalink: :year/:month/:day/:title/
permalink_defaults:
.....
deploy:
  type: git
  repo: git@github.com:angelteng/blog.git
  branch: gh-pages #发布分支
  name: 
  email:

server:
  port: 8080  #本地服务器端口
```
3. 去git新增一个仓库
修改git page选项
![git page](0.png)
新增一个ssh key

4. 管理：建议源代码根目录 git init 之后放在master分支，发布代码放在gh-pages分支

5. 新增及发布
```
# 新增 
>>> hexo new post "blog title"
# 发布
>>> hexo g
>>> hexo d
```
6. 静态资源引用
```
# 将图片放在 /source/_post/blogTitle 文件夹下
{% asset_img hexoLocal.png 图片描述 %}
```

[参考](https://www.jianshu.com/p/1519f22aff24)