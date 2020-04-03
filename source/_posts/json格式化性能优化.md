---
title: json格式化性能优化
date: 2020-03-06 14:15:10
tags: 
- python
---
1. 语言：python

2. 场景：由于history接口返回图片是base64编码，当limit较大时返回大json字符串。

3. 测试方式：在入口文件加入Profiler
```python
    from werkzeug.middleware.profiler import ProfilerMiddleware

    app, socketio = create_app()
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app)  
    socketio.run(app)
```
4. 测试结果：
{% asset_img 0.png%}

可见在 return jsonify({...})时候，simplejson encode耗时比较久，30ms左右。
5. 改进：使用ujson，并覆盖jsonify方法
```python
    import ujson as json
    def jsonify(*args, **kwargs):
        if args and kwargs:
            raise TypeError('jsonify() behavior undefined when passed both args and kwargs')
        elif len(args) == 1:  # single args are passed directly to dumps()
            data = args[0]
        else:
            data = args or kwargs


        return current_app.response_class(
            json.dumps(data) + '\n',
            mimetype=current_app.config['JSONIFY_MIMETYPE']
        )
```

性能提升大概2倍，耗时减少至15ms左右.

{% asset_img 1.png%}