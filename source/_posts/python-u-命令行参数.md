---
title: python -u 命令行参数
date: 2019-04-11 14:13:41
tags: 
- Python
category: Python
---
关闭stdin/stdout/stderr缓冲区.
-u :
- unbuffered binary stdout and stderr; also PYTHONUNBUFFERED=x. 
- Force  stdin,  stdout and stderr to be totally unbuffered.  On systems where it matters, also put stdin, stdout and stderr in binary mode.  Note that there is internal buffering  in  xreadlines(),  readlines() and  file-object  iterators  ("for  line in sys.stdin") which is not influenced by this option.  To work around this, you will want to use "sys.stdin.readline()" inside a "while 1:" loop.

[参考](https://stackoverflow.com/questions/14258500/python-significance-of-u-option)