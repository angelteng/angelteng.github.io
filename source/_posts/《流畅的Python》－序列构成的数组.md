---
title: 《流畅的Python》笔记
date: 2019-07-11 21:35:29
tags: 
- Python
categories: Python
---
# 序列构成的数组
1. 序列类型
    - 容器序列（可以存放不同数据类型）：list、tuple、collection.deque
    - 扁平序列： str、bytes、bytearray、memeryview、array.array

2. 按是否能被修改
    - 可变序列： list、bytearray、array.array、collection.deque 、memoryview
    - 不可变序列: tuple、str、bytes

3. 具名元组 collections.nametuple
```
    City = nametuple('City','name size population')
    tokyo = City('Tokyo','199999','36.9')
```
4. 切片
    - 切片总是忽略最后一个元素
    - s[a:b:c] c是间隔
    － 切片时调用__getitem__(slice(start,end,step))
5. \+ *
    - 都不修改原有对象
    - ＊是个浅复制，因此如果序列里含有对象的话，复制出来的是同一个对象的引用，比如[[]]*3
6. += 使用__iadd__（不改变原有对象） 如果不存在，则会调用__add__（创建了新对象）。*= 对应 __imul__同理。
7. 如果元组含有可变对象（eg. (1,2,[1,2]) ），改变了可变对象会抛出错误但是仍会执行。
8.  排序
    - list.sort 就地排序
    - sorted 创建一个新列表
9. bisect 管理已排序的列表
    ```python
        # 搜索
        bisect(hystack,needle)
        # 插入
        bisect.insert
        bisect.insort
    ```
10. 数组 array.array
11. 内存视图 memoryview：不复制内容的情况下操作同一个数组的不同切片
12. 双向队列 collection.deque

# 字典和集合
1. 标准库所有的映射类型都是利用dict，dict要求键必须是可散列的数据类型。
2. update 批量更新
3. setdefault处理找不到的值
    ```python
        my_dict.setdefault(key,[]).append(new_value)
    ```
4. collection.defaultdict 为找不到的键创建默认值
5. 所有映射类型在处理找不到的键时，会涉及__missing__方法，该方法只会被__getitem__调用
6. 创建自定义映射类型的时候，继承collections.UserDict比继承dict更好。
7. 不可变映射类型 types.MappingProxyType,创建了一个只读的映射视图.
8. 集合实现了很多中缀运算
9. 散列表是个稀疏数组，里面的单元叫说表元，每个表元包含键的引用、值的引用，表元大小一致，可以通过偏移量读取某个表元。
8. 计算键的散列值－> 利用散列值的一部分定位散列表中的一个表元，如果散列冲突，再使用另一个部分定位表元。
    因此：
    - 键必须是可散列的
    - 字典在内存上开销巨大
    - 键查询很快
    - 键的次序是乱的
    - 新增键有可能导致扩容，从而改变键的顺序
9. set、frozenset也依赖散列表
10. PHP的数组其实是个有序的映射
11. Python3.6之后字典的底层数据结构发生了变化，[参考](https://juejin.im/post/5d296e2af265da1bb31c6609)

# 文本和字节序列
1. Python3中的str对象获取的元素是Unicode字符
2. Unicode标准中，字符的标志（码位），字符的具体表述取决于所用的编码。把码位转换成字节序列的过程是编码，反之则为解码。
3. 二进制序列的切片始终是同一类型的二进制序列。
4. 二进制的方法与str的方法类似，特别的有 fromhex()
5. struct模块，把打包的字节序列转换程不同类型字段组成的元组。
6. memoryview用于共享内存，memory对象的切片是一个新的memoryview对象，不会复制字节序列。
7. 错误
    - UnicodeEncodeError：目标编码没有定义某个字符
    - UnicodeDecodeError：无法转换字节序列
    - SyntaxError：加载的.py模块中含有UTF－8之外的数据，而且没有声明编码。
8. BOM：字节序标记，指明编码时使用Intel CPU的小字节序。
9. unicodedata.normalize：规范化Unicode. NFC是最好的规范。
10. 大小写折叠：str.casefold() str.lower()

# 一等函数
1. 高阶函数：接受函数作为参数，或者把函数作为结果返回。
2. 匿名函数Lambda
3. 实现__call__实例方法，可以使任何对象表现得像函数。
4. 函数使用__dict__属性存储赋予它的用户属性。\_\_defaults__保存定位参数和关键字参数的默认值，\_\_kwdefaults__保存关键字参数默认值。\_\_code__保存参数的名称。\_\_annotation__保存注释。
5. 定义函数时，如果想指定仅限关键字参数，要把它们放在前面有＊的参数后面.
   ```python
    def f(a,*,b)
   ```
6. 提取函数的信息：inspect.signature
7. 冻结参数: functools.partial
8. 设计模式：
   - 对接口编程，而不是对实现编程
   - 优先使用对象组合，而不是类继承

# 装饰器与闭包
1. 装饰器的特点：
   - 能把被装饰的函数替换成别的函数
   - 装饰器在加载模块时立即执行
2. 变量作用域
   ```python
        b=6
        def f2(a):
            global b
            print(a)
            print(b)
            b = 9 # Python在编译函数时，发现b被赋值了，如果没有定义global，会判断b时局部变量而报错
   ```
3. 自由变量：未在本地作用域中绑定的变量。闭包会保留定义函数时存在的自由变量的绑定。只有嵌套在其他函数中的函数才可能需要处理不在全局作用域中的外部变量。
4. nonlocal：把变量标记为自由变量
    ```python
        def make_averager():
            count = 0
            total = 0
            def averager(new_value):
                nonlocal count,total
                count = count +1
                total = total + new_value
                return total / count
            return averager
    ```
5. functools.wraps，把相关属性从真实被装饰函数复制到装饰后返回的函数中，从而保持__name__和__doc__等不变。
6. functools.lru_cache: 实现LRU缓存，把耗时的函数结果保存起来。
7. functools.singledispatch 实现单分派泛函数
    ```python
        @singledispatch
        def htmlize(obj):
            pass
        @htmlize.register(str):
        def _(text):
            pass
        @htmlize.register(tuple):
        def _(tup):
            pass
    ```

# 对象引用、可变性、垃圾回收
1. Python中的变量类似JAVA引用变量。是一个标识。
2. is比较对象的标识，＝＝比较对象的值。is更快因为不能重载。
3. 默认做浅复制，比如构造方法或[:]，深复制用deepcopy
4. Python中唯一支持的参数传递模式是共享传参(call by share)，各个形式参数获得实参中各个引用的副本。因此，函数可能会改变参数传入的可变对象。
5. 不要使用可变类型作为参数的默认值，因为默认值在定义时计算，因此默认值成为了函数的属性，会被后续的函数调用中共享。
6. del删除名称，而不是对象。
7. CPython中垃圾回收使用引用计算算法。
8. 弱引用(weakref WeakValueDictionary)不会增加对象的引用数量
9. 对于不可变类型（比如元组），使用t[:]，不创建副本，而是返回同一个对象的引用。
10. 对于字符串字面量，会有“驻留”去共享字符串字面量。即字符串值相同的两个变量，共享了一个对象引用。
11. 对于*= +=，如果左边的变量绑定了不可变对象，会创建新对象，如果是可变对象，就就地修改。

# 符合Python风格的对象
1. classmethod常用于定义备选构造方法。
2. staticmethod可有可无。
3. 私有属性 __mood，实际做了名称改写，变成了 _Dog__mood
4. __slots__类属性让解释器以元组存储实例而不用字典，以节省内存。
   - 每个子类都要定义__slots__属性
   - 实例只能拥有__slots__定义了的属性，除非把__dict__加入__slots__
   - 如果不把__weakref__加入__slots__，无法被弱引用
5. 类属性可以为实例属性提供默认值
6. 类属性是公开，会被继承，经常用于创建一个子类，定制类的数据属性。

# 序列的修改、散列、切片
1. 使类表现得像序列：实现__getitem__和__len__方法。
2. 动态存取属性：__getattr__和__setattr__
3. zip拆包元组并重新组合

# 接口：从协议到抽象基类
1. 从鸭子类型代表动态协议。－－让动态类型语言实现多态
2. 虽然没有interface关键字，每个类都有接口，类的实现或继承公开的属性（方法／数据属性），包括特殊方法。
3. 使用猴子补丁在运行时实现协议：
    - 猴子补丁：在运行时修改类／模块，而不改动源码。
    - 内置类型不能打猴子补丁。
    ```python
        def set_cart(deck,position,card):
            deck._cards[position]=card
        FrenchDeck.__setitem = set_card  #Monkey Patch
    ```
4. 协议是动态的，只要对象部分实现了协议，就可以当成是该类型那样使用。
5. 白鹅类型：只要cls是抽象基类，即cls的元类是abc.ABCMeta，就可以使用isinstance(obj,cls)
   - 即便不继承，也有办法把一个类注册为抽象基类的虚拟子类。只要实现了抽象基类定义的接口。
   - 注册虚拟子类的方式实在抽象基类上调用register方法。但是注册的类不会从抽象基类中继承任何方法或属性。
6. 大部分标准库中的抽象基类在collection.abc模块中国年定义。
7. 抽象基类可以有实现代码，即使实现了，子类也必须覆盖抽象方法，但可以通过super()调用抽象方法。
8. 声明抽象基类最简单的方式是继承abc.ABC或其他抽象基类。
    ```python
        class Tombola(metaclass=abc.ABCMeta):
            @abstractmentd
            def methoss():
                pass
    ```
9. 动态识别子类__subclasshook__

# 继承的优缺点
1. 子类化内置类型时，内置类型不会调用用户定义的类覆盖的特殊方法。这种行为违背了面向对象编程的其中一个原则：始终应该从实例所属的类开始搜索方法。
2. 内置类型的方法调用的其他类的方法，如果被覆盖，也不会被调用。
3. 多重继承中，确定使用哪个类的方法，必须使用类名限定方法调用来避免歧义。
    ```python
        class D(B,C):
            def function(self):
                B.method1(self)
    ```
4. 解析顺序__mro__，该顺序即考虑继承图也考虑子类声明时列出的超类的顺序。
5. 处理继承建议：
    - 区分接口继承、实现继承。
      - 继承接口，创建子类型，实现“是什么”关系
      - 继承实现，通过重用避免代码重复。
    - 使用抽象基类显式表示接口
    - 通过混入重用代码，混入类mixin class
    - 在名称中明确指明混入 XViewMixin
    - 抽象基类可以作为混入，反过来不成立
    - 不要子类化多个具体类
    - 为用户提供聚合类
    - 优先使用对象组合，而不是继承
  
# 正确重载运算符
1. 规定：
   1. 不能重载内置类型运算符
   2. 不能新建运算符
   3. 某些运算符不能重载，包括is and or not
2. 一元运算符
   1. － \_\_neg__
   2. \+ \_\_pos__
   3. ~ \_\_invert__
   4. \* \_\_mul__和__rmul__
   5. += \_\_iadd__(就地计算）或__add__
3. 反向方法:\_\_add__和__radd__ 
4. 如果由于类型不兼容倒是运算符特殊方法无法返回有效结果，应该返回NotImplemented，这样Python会尝试使用反向方法。
5. __eq__正向反向都一样，只是参数顺序对调

# 可迭代的对象、迭代器、生成器
1. 对比：迭代器用于从集合取出元素。生成器用于凭空生成元素，所有的生成器都是迭代器。
2. 序列可以迭代的原因：实现iter函数。如果没有__iter__，则会调用__getitem__方法。
3. 检查对象x能否迭代：iter(x,stop),stop是哨符，当可调用对象返回这个值时，触发迭代器抛出StopInteration异常。
4. Python从可迭代对象获取迭代器。标准迭代器有__iter__和__next__方法。
5. 迭代器：实现了无参数的__next__方法，返回序列中下一个元素，如果没有元素了，抛出StopIteration异常。
6. 可迭代对象的__iter__方法，每次都实例化一个新的迭代器，迭代器本身实现__next__方法返回单个元素，__iter__方法返回自身。
7. 生成器，只要函数定义体中有yield关键字
8. re.finditer时re.findall惰性版本，返回了一个生成器。
9. yield from创建了通道，把内层生成器直接与外层生成器的客户端联系起来。

# 上下文管理器和else
1. with：设置一个临时上下文，交给上下文管理器对象控制，并负责清理上下文。上下文管理器对象协议包括__enter__和__exit__
2. for/else, while/else, try/else，这里的else类似于then的用法。
3. 如果__exit__返回None，True以外的值，with中任何异常会向上冒泡。
4. 模块contextlib中，@contextmanager把简单的生成器函数变成上下文管理器，yield前所有的代码在with开始时调用，yield后代码在with结束时调用。此时yield与迭代无关。
   
# 协程
1. yield作为控制流程的方法。
    ```python
        def x():
            print(1)
            x = yield
            print(x)
        y = X() 
        next(y) # 预激协程
        y.send(42)
    ```
2. 异常处理：generator.throw 终止协程generator.close
3. 协程的返回值捕捉需要被except中获取err.value
4. yield from 主要功能是打开双向通道
   1. 子生成器产出的值都直接传给委派生成器的调用方
   2. 使用send（）方法发给委派生成器的值都直接传给子生成器。如果值时None，会调用子生成器的__next__方法，如果不是None，会调用子生成器的send（）
   3. 生成器退出时，生成器／子生成器中的return expr表达式触发StopInteration(expr)异常抛出
   4. yield from表达式的值时子生成器终止时传给StopIteration异常的第一个参数

# 使用future处理并发
1. concurrent.future模块主要有ThreadPoolExcutor、ProcessPoolExcutor类。
2. future类有concurrent.future.Future和asyncio.Future。两者都有
   1. .done() 
   2. .add_done_callback() 
   3. .result(),但 concurrent.future.Future会阻塞直到有返回值，asyncio.Future则会抛出异常。
3. concurrent.future。as_completed返回迭代器，在future运行结束后产出future
4. CPython本身不是线程安全，因此有全局解释锁GIL，一次只允许使用一个线程执行Python字节码
5. Excutor.map可以并发运行多个可调用对象

# 使用asyncio处理并发
1. asyncio API协程在定义体必须使用yield from
2. @asyncio.coroutine装饰器定义协程函数
3. Task对象可以取消，取消后在协程当前yield处抛出asyncio.CancelledError，协程可以捕获异常，延迟取消，拒绝取消。
4. Task对象用于驱动协程 
    ```python
        task = asyncio.async(methos('think'))
    ```
5. 线程与协程区别：调度程序在任何时候都可能中断线程，但协程默认做好全方位保护。
6. asycio只支持TCP、UDP，HTTP使用aiohttp
7. 避免阻塞的方法：
   1. 在单独线程中运行各个阻塞操作 －－ 内存问题
   2. 把每个阻塞型操作转换成非阻塞的异步调用
      1. callback
      2. 协程：必须使用事件循环显式排定协程的执行时间，或者在其他排定了执行时间的协程中使用yield from把它激活。
8. 访问本地文件会阻塞，调用asyncio.run_in_excutor，底层时用线程处理了。
9. 异步框架：tornado
    
# 元编程
1. 特性：在不改变类接口的前提下，使用存取方法修改数据属性。管理实例属性的类属性。
2. 是否有效标识符：s.isidentifier()
3. 构造实例的特殊方法__new__，该方法返回一个实例，作为第一个参数传给__init__。
4. 使用装饰器 @property, @[prop_name].setter, @[prop_name].getter
5. property构造方法，可以使用函数调用而不是装饰器。
    ```python
        property(fget=None, fset=None, fdel=None, doc=None)
    ```
6. 特例都是类属性，但是特例管理的是实例属性的存取，
   1. 实例和类有同名属性，实例会覆盖类属性。
   2. 实例属性不会覆盖类特性
   3. 新添的类特性会覆盖实例属性
7. 特性工厂
    ```python
        def factory(prop_name):
            def prop_getter(instance):
                return instance.__dict__[prop_name]
            def prop_setter(instance):
                pass
            return property(prop_getter,prop_setter)
    ```
8. 属性的内置函数
   1. dir
   2. getattr
   3. setattr
   4. hasattr
   5. vars:返回__dict__属性
9.  直接通过__dict__属性读写的属性不会触发这些特殊方法。
    
# 属性描述符
1. 描述符是实现类特定协议的类，包括__get__,\_\_set__,\_\_delete__
2. 描述符的作用：创建一个实例，作为另一个类的类属性。
    ```python
        class Factory:
            def __init__(self,prop_name):
                self.prop_name = prop_name
            # self是描述符实例，instance是托管实例
            def __set__(self,instance,values):
                pass
            # owner是托管类的引用
            def __get__(self,instance,owner):
                pass
    ```
3. 描述符与特性工厂
   1. 描述符可以用子类扩展
   2. 相比于闭包，类属性、实例属性保持状态更容易理解
4. 实现__set__方法的描述符是覆盖性描述符，会覆盖实例属性的复制操作。
5. 没有__get__方法的覆盖性描述符，只有读操作时，实例属性会覆盖描述符。
6. 没有实现__set__方法的描述符是非覆盖性描述符。
7. 读类属性可以由依附在托管类上定义的__get__方法的描述符处理，但是写操作不会。
8. 描述符使用
   1. 使用特性以保持简单
   2. 只读描述符必须有__set__
   3. 用于验证的描述符可以只有__set__
   4. 仅用__get__方法的描述符实现高效缓存
   5. 非特殊方法可以被实例属性遮盖
   
# 类元编程
1. 类元编程是指在运行时创建或定制类的操作。
2. type是一个类，传入三个参数可以创建一个类，type的实例也是类。
    ```python
        MyClass= type('MyClass',(MySuperClass,MyMin),{'x':42,'y':50})
    ```
3. 类装饰器与函数装饰器类似，但子类不会继承类装饰器
4. 类的定义体属于“顶层代码”在导入时运行。包括嵌套类。
5. object是type的实例，type是object的子类。
6. 元类的特殊方法__prepare__，在__new__前被调用，使用类定义体中的属性创建映射。