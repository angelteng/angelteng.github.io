---
title: 搭建Discuz论坛
date: 2018-11-8 17:17:20
tags: sPython
---
1. 下载包文件：[Discuz论坛](http://www.discuz.net/forum-2-1.html)
![选择UTF版本](https://upload-images.jianshu.io/upload_images/14827444-8c3726d4057def02.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
2. 解压文件，实际代码目录为 /upload
3. 配置Nginx
```
server {
    charset utf-8;
    client_max_body_size 128M;
    listen 80; 
    server_name bbs.local.com;
    root        /vagrant/bbs/upload/;
    index       index.php;  
  
    location ~ \.php$ {
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_pass 127.0.0.1:9000;   # 查看php-fpm.conf 文件 [www] listen 属性
        #fastcgi_pass unix:/var/run/php5-fpm.sock;
        try_files $uri =404;
    }
}
```
3.  如nginx报错 
```
#nging/error.log
2018/11/08 12:13:29 [error] 14591#14591: *339 FastCGI sent in stderr: "Primary script unknown" while reading response header from upstream, client: , server: wiki.ainnovation.com, request: "GET /shaAdmin/index.php HTTP/1.1", upstream: "fastcgi://unix:/var/run/php/php7.2-fpm.sock:", host: ""
检查fastcgi_pass属性配置
```
4. 如Nginx 报404
```
2018/11/08 08:41:49 [error] 13474#13474: *1 "/home/abc/bbs/index.php" is not found (2: No such file or directory), client: 106.120.83.206, server:, request: "GET / HTTP/1.1", host: ""
```
需要检查文件权限及nginx进程用户是否有权限访问该目录
- ps -aux|grep Nginx 查看work 进程所属用户
![nginx](https://upload-images.jianshu.io/upload_images/14827444-4cc4e7b70cfee588.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
- 查看代码文件所属目录是否同一个用户/有访问权限
如果你使用vagrant 环境，vagrant 共享目录默认用户是vagrant 可以通过vagrant配置文件修改
```
config.vm.synced_folder "./", "/vagrant",create:true, :owner=>"www", :group=>"www",:mount_options=>["dmode=775","fmode=775"]
```
- 修改nginx 进程使用用户
```
>>> vim /usr/local/nginx/conf/nginx.conf
user www;
```

5. 如你数据库使用阿里云/腾讯云，可能会出现报错
页面报错信息： discuz Table 'xxxxx.forum_post' doesn't exist
数据库报错信息： 报错：#1075 - Incorrect table definition; there can be only one auto column and it must be defined as a key
可按以下sql手动创建表
```
CREATE TABLE IF NOT EXISTS `pre_forum_post` (
  `pid` int(10) unsigned NOT NULL,
  `fid` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `tid` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `first` tinyint(1) NOT NULL DEFAULT '0',
  `author` varchar(15) NOT NULL DEFAULT '',
  `authorid` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `subject` varchar(80) NOT NULL DEFAULT '',
  `dateline` int(10) unsigned NOT NULL DEFAULT '0',
  `message` mediumtext NOT NULL,
  `useip` varchar(15) NOT NULL DEFAULT '',
  `port` smallint(6) unsigned NOT NULL DEFAULT '0',
  `invisible` tinyint(1) NOT NULL DEFAULT '0',
  `anonymous` tinyint(1) NOT NULL DEFAULT '0',
  `usesig` tinyint(1) NOT NULL DEFAULT '0',
  `htmlon` tinyint(1) NOT NULL DEFAULT '0',
  `bbcodeoff` tinyint(1) NOT NULL DEFAULT '0',
  `smileyoff` tinyint(1) NOT NULL DEFAULT '0',
  `parseurloff` tinyint(1) NOT NULL DEFAULT '0',
  `attachment` tinyint(1) NOT NULL DEFAULT '0',
  `rate` smallint(6) NOT NULL DEFAULT '0',
  `ratetimes` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `status` int(10) NOT NULL DEFAULT '0',
  `tags` varchar(255) NOT NULL DEFAULT '0',
  `comment` tinyint(1) NOT NULL DEFAULT '0',
  `replycredit` int(10) NOT NULL DEFAULT '0',
  `position` int(8) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`position`,`tid`),
  UNIQUE KEY `pid` (`pid`),
  KEY `fid` (`fid`),
  KEY `authorid` (`authorid`,`invisible`),
  KEY `dateline` (`dateline`),
  KEY `invisible` (`invisible`),
  KEY `displayorder` (`tid`,`invisible`,`dateline`),
  KEY `first` (`tid`,`first`)
) ENGINE=INNODB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;
```

5. 修改论坛首页头部
文件位于：/template/default/commom/header.htm
6. 修改论坛logo
文件位于：/static/image/common/logo.png
7. 技巧：
- 用户组编辑器控制/访问：界面-用户组-编辑-（论坛相关-帖子设置）