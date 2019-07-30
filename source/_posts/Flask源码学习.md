---
title: Flask源码学习
date: 2019-07-25 14:01:39
tags: 
- Flask
- Python
---
# WSGI规范
WSGI(Web Server Gateway Interface):proposes a simple and universal interface between web servers and web applications or frameworks
[PEP_333](https://legacy.python.org/dev/peps/pep-0333/)有这个标准的详细说明
规定：
1. 每个Application必须是个可调用对象，接收两个参数environ（包含了环境信息的字典）、start_response（开始响应请求的函数），并且返回 iterable。
```python
    # environ 和 start_response 由 HTTP Server 提供并实现
    def application(environ, start_response):
        # Application 内部在返回前调用 start_response
        start_response('200 OK', [('Content-Type', 'text/html')])
        return '<h1>Hello, web!</h1>'
```
2. Server需要准备environ参数、定义start_response函数、调用Application的可调用对象。
```python
    import os, sys
    def run_with_cgi(application):
        environ = dict(os.environ.items())
        environ['wsgi.input']        = sys.stdin
        environ['wsgi.errors']       = sys.stderr
        environ['wsgi.version']      = (1, 0)
        environ['wsgi.multithread']  = False
        environ['wsgi.multiprocess'] = True
        environ['wsgi.run_once']     = True
        environ['wsgi.url_scheme'] = 'http'

        headers_set = []
        headers_sent = []

        def write(data):
            sys.stdout.write(data)
            sys.stdout.flush()

        def start_response(status, response_headers, exc_info=None):
            headers_set[:] = [status, response_headers]
            return write

        result = application(environ, start_response)
```
3. Middleware: Middleware 对服务器程序和应用是透明的，它像一个代理/管道一样，把接收到的请求进行一些处理，然后往后传递，一直传递到客户端程序，最后把程序的客户端处理的结果再返回。比如：
    - 根据 url 把请求给到不同的客户端程序（url routing）
    - 允许多个客户端程序/web 框架同时运行，就是把接到的同一个请求传递给多个程序。
    - 负载均衡和远程处理：把请求在网络上传输
    - 应答的过滤处理

# 从Flask run 开始
在 app.py 中
```python
    def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
        ........

        _host = "127.0.0.1"
        _port = 5000
        server_name = self.config.get("SERVER_NAME")
        sn_host, sn_port = None, None

        if server_name:
            sn_host, _, sn_port = server_name.partition(":")

        host = host or sn_host or _host
        port = int(next((p for p in (port, sn_port) if p is not None), _port))

        from werkzeug.serving import run_simple

        try:
            # 注意第三个参数是self,也就是这个Flask的实例对象
            run_simple(host, port, self, **options) #<<<<<<<<
        finally:
            self._got_first_request = False
    
    .....
    def run_simple(hostname, port, application, use_reloader=False, use_debugger=False, use_evalex=True, extra_files=None, reloader_interval=1, reloader_type="auto", threaded=False, processes=1, request_handler=None, static_files=None, passthrough_errors=False, ssl_context=None,):
        .......

        def inner():
            try:
                fd = int(os.environ["WERKZEUG_SERVER_FD"])
            except (LookupError, ValueError):
                fd = None
            srv = make_server(
                hostname,
                port,
                application,
                threaded,
                processes,
                request_handler,
                passthrough_errors,
                ssl_context,
                fd=fd,
            )                   # <<<<<<<<<<<<<<<<<<<<<<<<
            if fd is None:
                log_startup(srv.socket)
            srv.serve_forever()

        inner()

    .......
    def make_server(host=None, port=None, app=None, threaded=False, processes=1, request_handler=None, passthrough_errors=False, ssl_context=None, fd=None,):
       # 省略多线程/ 多进程情况

        return BaseWSGIServer(   #<<<<<<<<<<<<<
            host, port, app, request_handler, passthrough_errors, ssl_context, fd=fd
        )
    ..........
    # 调用了Python的HTTPServer模块
    class BaseWSGIServer(HTTPServer, object):
        .........
        
        def serve_forever(self):
            self.shutdown_signal = False
            try:
                HTTPServer.serve_forever(self)   # 最终调用HTTPServer.serve_forever方法
            except KeyboardInterrupt:
                pass
            finally:
                self.server_close()

```
整体流程为：
flask.run --> app.run --> werkzeug.run_simple  --> werkzeug.BaseWSGIServer --> Python.HTTPServer.serve_forever

# 路由匹配
使用 @app.route装饰器与app.add_url_rule是一样的
```python
    def route(self, rule, **options):
        def decorator(f):
            endpoint = options.pop("endpoint", None)
            self.add_url_rule(rule, endpoint, f, **options)
            return f
        return decorator
    
    def add_url_rule(self, rule, endpoint=None, view_func=None, provide_automatic_options=None, **options):
        # endpoint是视图函数的名字
        if endpoint is None:
            endpoint = _endpoint_from_view_func(view_func)
        
        methods = options.pop("methods", None)
        # url_rule_class 是werkzeug.routeing.Rule的实例
        rule = self.url_rule_class(rule, methods=methods, **options)
        rule.provide_automatic_options = provide_automatic_options
        # url_map 是werkzeug.routeing.Map的实例
        self.url_map.add(rule)
        if view_func is not None:
            # view_functions是一个字典
            old_func = self.view_functions.get(endpoint)
            if old_func is not None and old_func != view_func:
                raise AssertionError(
                    "View function mapping is overwriting an "
                    "existing endpoint function: %s" % endpoint
                )
            self.view_functions[endpoint] = view_func

```
werkzeug 的 url_map类似：
```python
    m = Map([
        Rule('/', endpoint='index'),
        Rule('/downloads/', endpoint='downloads/index'),
        Rule('/downloads/<int:id>', endpoint='downloads/show')
    ])
```
view_functions就是个字典：
```
    {
        "end_point_1" : view_function_1,
        "end_point_2" : view_function_2
    }
```
因此endpoint是一个连接rule跟view_function的重要的桥梁
上面说明了路由添加管理，下面来看路由分发过程：
```python
    class Flask:
        def __call__(self, environ, start_response):
            return self.wsgi_app(environ, start_response)
            
        def wsgi_app(self, environ, start_response):
            ctx = self.request_context(environ)
            error = None
                    
            ctx.push() # 先推送一个请求上下文
            response = self.full_dispatch_request() #<<<<<<<<<<<<
            
            return response(environ, start_response)
            ctx.auto_pop(error)

        def full_dispatch_request(self):
            self.try_trigger_before_first_request_functions()
            try:
                request_started.send(self)
                rv = self.preprocess_request()
                if rv is None:
                    rv = self.dispatch_request()  #<<<<<<<<<<<<<<
            except Exception as e:
                rv = self.handle_user_exception(e)
            return self.finalize_request(rv)

        def dispatch_request(self):
            # 先取请求上下文的信息
            req = _request_ctx_stack.top.request
            if req.routing_exception is not None:
                self.raise_routing_exception(req)
            # 从上下文中获取url_rule
            rule = req.url_rule
            # if we provide automatic options for this URL and the
            # request came with the OPTIONS method, reply automatically
            if (
                getattr(rule, "provide_automatic_options", False)
                and req.method == "OPTIONS"
            ):
                return self.make_default_options_response()
            # otherwise dispatch to the handler for that endpoint
            # 从view_functions字典中取对应url_rule.endpoint的方法运行
            return self.view_functions[rule.endpoint] (**req.view_args)
```
然后来看看请求上下文做了什么，在flask/ctx.py
```python
    class RequestContext(object):    
        def __init__(self, app, environ, request=None, session=None):
            self.app = app
            if request is None:
                request = app.request_class(environ)
            self.request = request
            self.url_adapter = None
            try:
                # 创建了url_adapter
                self.url_adapter = app.create_url_adapter(self.request) #<<<<<<<<<<<<<<<
            except HTTPException as e:
                self.request.routing_exception = e
            self.flashes = None
            self.session = session

        def push(self):
            """Binds the request context to the current context."""
            top = _request_ctx_stack.top
            # Before we push the request context we have to ensure that there
            # is an application context.
            app_ctx = _app_ctx_stack.top
            if app_ctx is None or app_ctx.app != self.app:
                app_ctx = self.app.app_context()
                app_ctx.push() #如果没有app上下文，推送一个
                self._implicit_app_ctx_stack.append(app_ctx)
            else:
                self._implicit_app_ctx_stack.append(None)
            # 把当前请求上下文推送到栈
            _request_ctx_stack.push(self) 
            if self.url_adapter is not None:
                # 匹配路由
                self.match_request() #<<<<<<<<<<<<<<<<<<

        def match_request(self):
            """Can be overridden by a subclass to hook into the matching
            of the request.
            """
            try:
                result = self.url_adapter.match(return_rule=True) #<<<<<<<<<<<<<<<<
                self.request.url_rule, self.request.view_args = result
            except HTTPException as e:
                self.request.routing_exception = e

    def create_url_adapter(self, request):
        if request is not None:
            # If subdomain matching is disabled (the default), use the
            # default subdomain in all cases. This should be the default
            # in Werkzeug but it currently does not have that feature.
            subdomain = (
                (self.url_map.default_subdomain or None)
                if not self.subdomain_matching
                else None
            )
            # 把url_map绑定到wsgi到environ变量上
            return self.url_map.bind_to_environ(  #<<<<<<<<<<<<<
                request.environ,
                server_name=self.config["SERVER_NAME"],
                subdomain=subdomain,
            )
```
werkzeug.routeing.match的方法注释里就有很简单的例子,逻辑是用compile的正则表达式去匹配给出的真实路径信息，把所有的匹配组件转换成对应的值，保存在字典中（这就是传递给视图函数的参数列表）并返回。
```python
    m = Map([
        Rule('/', endpoint='index'),
        Rule('/downloads/', endpoint='downloads/index'),
        Rule('/downloads/<int:id>', endpoint='downloads/show')
        ])
    urls = m.bind("example.com", "/")
    urls.match("/", "GET")
    >>> ('index', {})
    urls.match("/downloads/42")
    >>> ('downloads/show', {'id': 42})
```
整体流程：
1. 通过@app.route或者app.add_url_rule注册应用url对应的处理函数
2. 每次请求过来的时候，推送请求上下文到栈，然后调用路由匹配的逻辑，把路由结果保存起来
3. dispatch_request分发保存的路由结果，调用对应的视图函数

# 上下文
在拿request信息的时候，我们会像这样引入一个全局变量
```
    from flask import request
```
但是在不同的进程/线程/协程中，request的值是不一样的。
1. 进程比较好理解，进程间本来就是资源独立的。
2. 在线程/协程中，可以实现类似thread.local，实现一个字典，然后不同的线程id对应不同的值
flask/global.py 这里保存了这些上下文的信息
```python
    from functools import partial

    from werkzeug.local import LocalProxy
    from werkzeug.local import LocalStack

    def _lookup_req_object(name):
        top = _request_ctx_stack.top
        if top is None:
            raise RuntimeError(_request_ctx_err_msg)
        return getattr(top, name)


    def _lookup_app_object(name):
        top = _app_ctx_stack.top
        if top is None:
            raise RuntimeError(_app_ctx_err_msg)
        return getattr(top, name)


    def _find_app():
        top = _app_ctx_stack.top
        if top is None:
            raise RuntimeError(_app_ctx_err_msg)
        return top.app

    # context locals
    _request_ctx_stack = LocalStack()   #<<<<<<<<<<<<<
    _app_ctx_stack = LocalStack()       #<<<<<<<<<<<<<
    current_app = LocalProxy(_find_app)
    request = LocalProxy(partial(_lookup_req_object, "request"))
    session = LocalProxy(partial(_lookup_req_object, "session"))
    g = LocalProxy(partial(_lookup_app_object, "g"))

```
LocalStack是werkzegu.local的一个栈实现，提供了隔离的栈访问。
```python
    class LocalStack(object):
        def __init__(self):
            self._local = Local()

        def __call__(self):
            def _lookup():
                rv = self.top
                if rv is None:
                    raise RuntimeError("object unbound")
                return rv

            return LocalProxy(_lookup)
```
Local主要实现了线程id/协程id对应字典，提供了多线程或者多协程隔离的属性访问。
```python
    try:
        from greenlet import getcurrent as get_ident
    except ImportError:
        try:
            from thread import get_ident
        except ImportError:
            from _thread import get_ident

    class Local(object):
        __slots__ = ("__storage__", "__ident_func__")

        def __init__(self):
            # 变量的值的值都存在__storage__里
            object.__setattr__(self, "__storage__", {})  
            object.__setattr__(self, "__ident_func__", get_ident)

        def __iter__(self):
            return iter(self.__storage__.items())

        def __call__(self, proxy):
            """Create a proxy for a name."""
            return LocalProxy(self, proxy)

        def __release_local__(self):
            self.__storage__.pop(self.__ident_func__(), None)

        # 取值、设值、删值的时候，都是通过__ident_func__获取线程/协程对象id，再在这个id字典下对变量进行操作
        def __getattr__(self, name):
            try:
                return self.__storage__[self.__ident_func__()][name]
            except KeyError:
                raise AttributeError(name)

        def __setattr__(self, name, value):
            ident = self.__ident_func__()
            storage = self.__storage__
            try:
                storage[ident][name] = value
            except KeyError:
                storage[ident] = {name: value}

        def __delattr__(self, name):
            try:
                del self.__storage__[self.__ident_func__()][name]
            except KeyError:
                raise AttributeError(name)
```
LocalProxy是一个Local对象的代理，负责把所有对自己的操作转发给内部的Local对象。
```python
    class LocalProxy(object):
        __slots__ = ('__local', '__dict__', '__name__')

        def __init__(self, local, name=None):
            # 把通过参数传递进来的 Local 实例保存在 __local 属性中
            object.__setattr__(self, '_LocalProxy__local', local)  
            object.__setattr__(self, '__name__', name)
       
        # 通过_get_current_object() 方法获取当前线程或者协程对应的对象。
        def _get_current_object(self):
            """Return the current object."""
            if not hasattr(self.__local, '__release_local__'):
                return self.__local()
            try:
                return getattr(self.__local, self.__name__)
            except AttributeError:
                raise RuntimeError('no object bound to %s' % self.__name__)

        def __getattr__(self, name):
            if name == '__members__':
                return dir(self._get_current_object())
            return getattr(self._get_current_object(), name)
```
因此，
1. 每次有请求过来的时候，flask会先创建当前线程或者进程需要处理的两个重要上下文对象，把它们保存到隔离的栈里面，这样视图函数进行处理的时候就能直接从栈上获取这些信息。
2. 为什么区分app上下文、请求上下文：一个请求对应一个app上下文、一个请求上下文，但是在测试或者 python shell 中运行的时候，用户可以单独创建 请求上下文或者app上下文，这种灵活度方便用户的不同的使用场景。
3. 为什么用栈结构：在多个App的时候，无论有多少个App，只要主动去Push它的app context，context stack就会累积起来，这样，栈顶永远是当前操作的 App Context。当一个 App Context 结束的时候，相应的栈顶元素也随之出栈。如果在执行过程中抛出了异常，对应的 App Context 中注册的 teardown函数被传入带有异常信息的参数。因此，只有栈结构才能保存多个 Context 并在其中定位出哪个才是“当前”。


参考：
[flask 源码解析](https://cizixs.com/2017/01/13/flask-insight-context/)
[Flask的Context(上下文)学习笔记](https://www.jianshu.com/p/7a7efbb7205f)