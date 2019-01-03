---
title: hmac加密算法
date: 2018-12-06 11:42:51
tags: 
- 后端
categories: 后端
---
密钥散列消息认证码(Keyed-hash message authentication code)
它是一种通过特别计算方式之后产生的消息认证码（MAC），使用密码散列函数，同时结合一个加密密钥。它可以用来保证数据的完整性，同时可以用来作某个消息的身份验证。

使用方法（Python)：
```
import hmac
# 传入的key和message都是bytes类型
message = b'Hello, world!'
key = b'secret'
h = hmac.new(key, message, digestmod='MD5')
# 如果消息很长，可以多次调用h.update(msg)
h.hexdigest()
# output: 'fa4ee7d173f2d97ee79022d1a7355bcf'
```
[参考](https://pythoncaff.com/docs/pymotw/hmac-cryptographic-message-signing-and-verification/134)