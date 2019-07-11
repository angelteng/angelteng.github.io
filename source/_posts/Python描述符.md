---
title: Python描述符
date: 2019-06-21 16:13:40
tags:
- Python
categories: Python
---
# 描述符
## 定义
1. 一个描述符是一个有“绑定行为”的对象属性(object attribute)，它的访问控制会被描述器协议方法重写。
2. 任何定义了 \__get__, \__set__ 或者 \__delete__ 任一方法的类称为描述符类，其实例对象便是一个描述符，这些方法称为描述符协议。
    - 同时定义了 \__get__ 和 \__set__ 的描述符称为 数据描述符(data descriptor)；仅定义了 \__get__ 的称为 非数据描述符(non-data descriptor) 。
    - 两者区别在于：如果 obj.\__dict__ 中有与描述符同名的属性，若描述符是数据描述符，则优先调用描述符，若是非数据描述符，则优先使用 obj.\__dict__ 中属性。
3. 当对一个实例属性进行访问时，Python 1、类属性，2、数据描述符，3、实例属性，4、非数据描述符，5、\__getattr__()顺序进行查找，如果查找到目标属性并发现是一个描述符，Python 会调用描述符协议来改变默认的控制行为。
4. 描述符是 @property，@classmethod，@staticmethod 和 super 的底层实现机制。

## 描述符方法
```
    __get__(self, instance, owner)
    __set__(self, instance, value)
    __delete__(self, instance)
```
### 1. 使用类方法创建描述符
```
    class Descriptor(object):
        def __init__(self):
            self._name = ''
    
        def __get__(self, instance, owner):
            print("Getting: %s" % self._name)
            return self._name
    
        def __set__(self, instance, name):
            print("Setting: %s" % name)
            self._name = name.title()
    
        def __delete__(self, instance):
            print("Deleting: %s" %self._name)
            del self._name
 
    class Person(object):
        name = Descriptor()
```
### 2. 使用属性类型创建描述符
```
    class Person(object):
        def __init__(self):
            self._name = ''
    
        def fget(self):
            print("Getting: %s" % self._name)
            return self._name
    
        def fset(self, value):
            print("Setting: %s" % value)
            self._name = value.title()

        def fdel(self):
            print("Deleting: %s" %self._name)
            del self._name

        # property() 的语法是 property(fget=None, fset=None, fdel=None, doc=None)
        name = property(fget, fset, fdel, "I'm the property.")
```

### 3. 使用属性修饰符（proprty）创建描述符
```
    class Person(object):
        def __init__(self):
            self._name = ''
    
        @property
        def name(self):
            print "Getting: %s" % self._name
            return self._name
    
        @name.setter
        def name(self, value):
            print "Setting: %s" % value
            self._name = value.title()
    
        @name.deleter
        def name(self):
            print ">Deleting: %s" % self._name
            del self._name
```

## staticMethod 原理
@staticmethod : when this method is called, we don't pass an instance of the class to it (as we normally do with methods). This means you can put a function inside a class but you can't access the instance of that class (this is useful when your method does not use the instance).
```
    class StaticMethod(object):
        def __init__(self, f):
            self.f = f
        
        def __get__(self, obj, objtype=None):
            return self.f


    class E(object):
        @StaticMethod
        def f( x):
            return x
            
    print(E.f('staticMethod Test'))
    ee = E()
    print(ee.f('ee static'))
```
## classmethod 原理
A class method receives the class as implicit first argument, just like an instance method receives the instance. To declare a class method, use this idiom.
A class method can be called either on the class (such as C.f()) or on an instance (such as C().f()). The instance is ignored except for its class. If a class method is called for a derived class, the derived class object is passed as the implied first argument.
```
    class ClassMethod(object):
        def __init__(self, f):
            self.f = f
        
        def __get__(self, obj, owner=None):
            if owner is None:
                owner = type(obj)
            
            def newfunc(*args):
                return self.f(owner, *args)
            
            return newfunc
    
    class E(object):
        name = 'name'
        @ClassMethod
        def f(cls,x):
            return x + cls.name

    print(E.f('classMethod Test'))
```


参考:
[Python 描述符简介](https://www.ibm.com/developerworks/cn/opensource/os-pythondescriptors/index.html)
[Python 描述符(Descriptor) 附实例](https://zhuanlan.zhihu.com/p/42485483)
[【案例讲解】Python为什么要使用描述符？](https://juejin.im/post/5cc4fbc0f265da0380437706)
[python描述符(descriptor)、属性(property)、函数（类）装饰器(decorator )原理实例详解](https://www.cnblogs.com/chenyangyao/p/python_descriptor.html)
[python装饰器、描述符模拟源码实现](https://segmentfault.com/a/1190000013425128)