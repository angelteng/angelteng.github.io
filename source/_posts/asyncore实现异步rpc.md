---
title: asyncore实现异步rpc
date: 2020-04-16 15:29:32
tags:
- python
---
SERVER 端
``` python
    import json
    import struct
    import socket
    import asyncore
    from io import BytesIO


    class RPCHandler(asyncore.dispatcher_with_send):  # 客户套接字处理器必须继承 dispatcher_with_send

        def __init__(self, sock, addr):
            asyncore.dispatcher_with_send.__init__(self, sock=sock)
            self.addr = addr
            self.handlers = {
                "ping": self.ping
            }
            self.rbuf = BytesIO()  # 读缓冲区由用户代码维护，写缓冲区由 asyncore 内部提供

            
        def handle_connect(self):  # 新的连接被 accept 后回调方法
            print(self.addr, 'comes')

        def handle_close(self):  # 连接关闭之前回调方法
            print(self.addr, 'bye')
            self.close()

        def handle_read(self):  # 有读事件到来时回调方法
            while True:
                content = self.recv(2)
                # print('read 2', content)
                if content:
                    self.rbuf.write(content)
                if len(content) < 1024:
                    break
            self.handle_rpc()

        def handle_rpc(self):  # 将读到的消息解包并处理
            while True:  # 可能一次性收到了多个请求消息，所以需要循环处理
                self.rbuf.seek(0)
                length_prefix = self.rbuf.read(4)
                if len(length_prefix) < 4:  # 不足一个消息
                    break
                length = int.from_bytes(length_prefix, byteorder='big') 
                body = self.rbuf.read(length)
                if len(body) < length:  # 不足一个消息
                    break
                try:
                    request = json.loads(body.decode("utf-8"))
                except:
                    break
                in_ = request['in']
                params = request['params']
                handler = self.handlers[in_]
                handler(params)  # 处理消息
                left = self.rbuf.getvalue()[length + 4:]  # 消息处理完了，缓冲区要截断
                self.rbuf = BytesIO()
                self.rbuf.write(left)
            self.rbuf.seek(0, 2)  # 将游标挪到文件结尾，以便后续读到的内容直接追加

        def ping(self, params):
            self.send_result("pong", params)

        def send_result(self, out, result):
            response = {"out": out, "result": result}
            print("out",response)
            body = json.dumps(response).encode("utf-8")
            length_prefix = len(body).to_bytes(4, byteorder='big')
            self.send(length_prefix)  # 写入缓冲区
            self.send(body)  # 写入缓冲区


    class RPCServer(asyncore.dispatcher):  # 服务器套接字处理器必须继承 dispatcher

        def __init__(self, host, port):
            asyncore.dispatcher.__init__(self)
            self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
            self.set_reuse_addr()
            self.bind((host, port))
            self.listen(1)

        def handle_accept(self):
            pair = self.accept()
            if pair is not None:
                sock, addr = pair
                RPCHandler(sock, addr)

    if __name__ == '__main__':
        RPCServer("localhost", 8080)
        asyncore.loop()
```
CLIENT 端
``` python
    import socket
    import sys 
    import os
    import time
    import json


    def clientSocket():
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # if sock < 0:
            #         print('socket error')

            try:
                    sock.connect(("127.0.0.1",8080))
            except:
                    print("exception")
                    sys.exit(1)

            message = {"in":"ping","params":"sha params"}
            message = json.dumps(message).encode('utf-8')
            encode_bytes = len(message).to_bytes(4, byteorder='big') + message
            sock.sendall(encode_bytes)

            while True:
                data = sock.recv(100)
                print('received "%s"' %data)

            sock.close()

    if __name__ == "__main__":
            clientSocket()
```
使用epoll实现
SERVER端
```python
    import socket
    import select
    import queue
    import time
    
    #创建socket对象
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #设置IP地址复用
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #ip地址和端口号
    server_address = ("127.0.0.1", 8080)
    #绑定IP地址
    serversocket.bind(server_address)
    #监听，并设置最大连接数
    serversocket.listen(10)
    print("服务器启动成功，监听IP：" , server_address)
    #服务端设置非阻塞
    serversocket.setblocking(False)  
    #超时时间
    timeout = 10
    #创建epoll事件对象，后续要监控的事件添加到其中
    epoll = select.epoll()
    #注册服务器监听fd到等待读事件集合
    epoll.register(serversocket.fileno(), select.EPOLLIN)
    #保存连接客户端消息的字典，格式为{}
    message_queues = {}
    #文件句柄到所对应对象的字典，格式为{句柄：对象}
    fd_to_socket = {serversocket.fileno():serversocket,}


    def run():
        while True:
            print("等待活动连接......")
            #轮询注册的事件集合，返回值为[(文件句柄，对应的事件)，(...),....]
            events = epoll.poll(timeout)
            if not events:
                print("epoll超时无活动连接，重新轮询......")
                continue
            print("有" , len(events), "个新事件，开始处理......")
            
            for fd, event in events:
                socket = fd_to_socket[fd]
                #如果活动socket为当前服务器socket，表示有新连接
                if socket == serversocket:
                    connection, address = serversocket.accept()
                    print("新连接：" , address)
                    #新连接socket设置为非阻塞
                    connection.setblocking(False)
                    #注册新连接fd到待读事件集合
                    epoll.register(connection.fileno(), select.EPOLLIN)
                    #把新连接的文件句柄以及对象保存到字典
                    fd_to_socket[connection.fileno()] = connection
                    #以新连接的对象为键值，值存储在队列中，保存每个连接的信息
                    message_queues[connection]  = queue.Queue()
                #关闭事件
                elif event & select.EPOLLHUP:
                    print('client close')
                    #在epoll中注销客户端的文件句柄
                    epoll.unregister(fd)
                    #关闭客户端的文件句柄
                    fd_to_socket[fd].close()
                    #在字典中删除与已关闭客户端相关的信息
                    del fd_to_socket[fd]
                #可读事件
                elif event & select.EPOLLIN:
                    print('client in')
                    #接收数据
                    data = socket.recv(1024)
                    if data:
                        print("收到数据：" , data , "客户端：" , socket.getpeername())
                        #将数据放入对应客户端的字典
                        message_queues[socket].put(data)
                        #修改读取到消息的连接到等待写事件集合(即对应客户端收到消息后，再将其fd修改并加入写事件集合)
                        data_handler(fd)
                        # g1.join()
                    else:
                        #在epoll中注销客户端的文件句柄
                        epoll.unregister(fd)
                        #关闭客户端的文件句柄
                        fd_to_socket[fd].close()
                        #在字典中删除与已关闭客户端相关的信息
                        del fd_to_socket[fd]
                #可写事件
                elif event & select.EPOLLOUT:
                    print('client out')
                    try:
                        #从字典中获取对应客户端的信息
                        msg = message_queues[socket].get_nowait()
                    except queue.Empty:
                        print(socket.getpeername() , " queue empty")
                        #修改文件句柄为读事件
                        epoll.modify(fd, select.EPOLLIN)
                    else :
                        print("发送数据：" , data , "客户端：" , socket.getpeername())
                        #发送数据
                        socket.send(msg)
        #在epoll中注销服务端文件句柄
        epoll.unregister(serversocket.fileno())
        #关闭epoll
        epoll.close()
        #关闭服务器socket
        serversocket.close()


    def data_handler(fd):
        socket = fd_to_socket[fd]
        msg = message_queues[socket].get_nowait()
        if msg == b"ping":
            message_queues[socket].put("ok.......pong!".encode())
            epoll.modify(fd, select.EPOLLOUT)

    if __name__ == "__main__":
        run()
        

```


参考：
- [【RPC-Python】单进程异步模型](https://blog.csdn.net/gx864102252/article/details/82155834)
- [字节到大整数到解包与打包](https://python3-cookbook.readthedocs.io/zh_CN/latest/c03/p05_pack_unpack_large_int_from_bytes.html)