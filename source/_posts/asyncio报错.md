---
title: asyncio报错
date: 2018-11-14 17:13:57
tags: Python
---
在flask中使用
```
import asyncio
.....
 loop = asyncio.get_event_loop()
....
```
发现报错
RuntimeError: There is no current event loop in thread 'Thread-2'.

修改为
```
import asyncio
...
new_loop = asyncio.new_event_loop()
asyncio.set_event_loop(new_loop)
loop = asyncio.get_event_loop()
```
原因：
```
# 源码
def get_event_loop(self):
    """Get the event loop.
    This may be None or an instance of EventLoop.
    """
    if (self._local._loop is None and
            not self._local._set_called and
            isinstance(threading.current_thread(), threading._MainThread)):
        self.set_event_loop(self.new_event_loop())

    if self._local._loop is None:
        raise RuntimeError('There is no current event loop in thread %r.'
                            % threading.current_thread().name)

    return self._local._loop
```
在主线程中，调用get_event_loop总能返回属于主线程的event loop对象，如果是处于非主线程中，还需要调用set_event_loop方法指定一个event loop对象，这样get_event_loop才会获取到被标记的event loop对象：
```
def set_event_loop(self, loop):
    """Set the event loop."""
    self._local._set_called = True
    assert loop is None or isinstance(loop, AbstractEventLoop)
    self._local._loop = loop
```
[参考](https://juejin.im/entry/5b3d99565188251b134e5355) 
由于Flask工作流程：
如果启动app时将threaded参数设定为True,flask才会以多线程的方式去处理每一个请求，
否则，所有请求是在一个工作线程（非主线程）运行。[具体](https://www.cnblogs.com/jamespei/p/7158107.html)。此时与直接命令行运行脚本不同，请留意。