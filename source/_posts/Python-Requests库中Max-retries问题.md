---
title: Python Requests库中Max retries问题
date: 2019-06-25 15:22:14
tags: 
- Python
- Requests
category: Python
---
查日志的时候发现如下报错：
```
    Traceback (most recent call last):
    File "./app/business_api/business_api.py", line 87, in callback_function
        response = requests.post('xxx'+json.dumps(results), timeout=self.timeout)
    File "/usr/lib/python3.6/site-packages/requests/api.py", line 116, in post
        return request('post', url, data=data, json=json, **kwargs)
    File "/usr/lib/python3.6/site-packages/requests/api.py", line 60, in request
        return session.request(method=method, url=url, **kwargs)
    File "/usr/lib/python3.6/site-packages/requests/sessions.py", line 524, in request
        resp = self.send(prep, **send_kwargs)
    File "/usr/lib/python3.6/site-packages/requests/sessions.py", line 637, in send
        r = adapter.send(request, **kwargs)
    File "/usr/lib/python3.6/site-packages/requests/adapters.py", line 516, in send
        raise ConnectionError(e, request=request)
    requests.exceptions.ConnectionError: HTTPSConnectionPool(host='xxx', port=8094): Max retries exceeded with url: xxx (Caused by NewConnectionError('<urllib3.connection.VerifiedHTTPSConnection object at 0x7f882011f390>: Failed to establish a new connection: [Errno -3] Try again',))
```
网上查了一下“Max retries” ，一般出现在爬虫的场景，http连接数过多，因为requests默认使用了keep-alive，所以要在header增加{"Connect":"close"}，但是出现问题的场景是后台服务，从阿里云监控上看该时段的tcp连接数也没有很大的波峰。
参考了[requests的高级功能-重试机制](https://fanchao01.github.io/blog/2016/07/30/pythonlib-request3/)这篇文章所说，requests是有重试机制的，使用重试会导致返回的错误为MaxRetriesError，而不是确切的异常。
网上暂时没查到[Errno -3] Try again 这个错误具体原因。


其他参考：
[关于python爬虫的深坑：requests抛出异常Max retries exceeded with url](https://www.jwlchina.cn/2016/10/29/关于python爬虫的深坑：requests抛出异常Max%20retries%20exceeded%20with%20url/)
[requests库的Failed to establish a new connection](https://eclipsesv.com/2017/01/29/requests库error/)