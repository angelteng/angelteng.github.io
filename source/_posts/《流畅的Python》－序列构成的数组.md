---
title: 《流畅的Python》－序列构成的数组
date: 2019-07-11 21:35:29
tags:
---
1. 序列类型
    - 容器序列（可以存放不同数据类型）：list、tuple、collection.deque
    - 扁平序列： str、bytes、bytearray、memeryview、array.array

2. 按是否能被修改
    - 可变序列： list、bytearray、array.array、collection.deque 、memeryview
    - 不可变序列: tuple、str、bytes

3. 具名元组 collections.nametuple
```
    City = nametuple('City','name size population')
    tokyo = City('Tokyo','199999','36.9')
```
4. 切片
    - 切片总是忽略最后一个元素
    - s[a:b:c] c是间隔
    － 切片时调用 __getitem__(slice(start,end,step))
5. + *
    - 都不修改原有对象
    - ＊是个浅复制，因此如果序列里含有对象的话，复制出来的是同一个对象的引用，比如[[]]*3
6. += 使用 __iadd__（不改变原有对象） 如果不存在，则会调用 __add__（创建了新对象）。*= 对应 __imul__同理。
7. 如果元组含有可变对象（eg. (1,2,[1,2]) ），改变了可变对象会抛出错误但是仍会执行。
8.  排序
    - list.sort 就地排序
    - sorted 创建一个新列表
9. bisect 管理已排序的列表
    ```
        # 搜索
        bisect(hystack,needle)
        # 插入
        bisect.insert
        bisect.insort
    ```
10. 数组 array.array
11. 内存视图 memoryview：不复制内容的情况下操作同一个数组的不同切片
12. 双向队列 collection.deque