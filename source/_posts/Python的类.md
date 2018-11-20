---
title: Python的类
date: 2018-11-7 17:18:02
tags: Python
---
1. 作用域：一个定义于某模块中的函数的全局作用域是该模块的命名空间，而不是该函数的别名被定义或调用的位置
2. example
```
class MyClass:
    i = 12345
    # 类的实例化操作会自动为新创建的类实例调用 __init__() 方法
    def __init__(self,realpart, imagpart):
        self.data = []
        self.r = real part
        self.im = imagpart
    # 一般方法的第一个参数被命名为 self,这仅仅是一个约定
    def f(self):
        return 'hello world'

>>> x = MyClass('realpart','imagpart')
```
3. 继承
```
class DerivedClassName(BaseClassName):
    pass
class DerivedClassName(modname.BaseClassName):
    pass

# 多继承
class DerivedClassName(Base1, Base2, Base3):
    pass
```
- 派生类可能会覆盖其基类的方法。因为方法调用同一个对象中的其它方法时没有特权，基类的方法调用同一个基类的方法时，可能实际上最终调用了派生类中的覆盖方法。
- 检查继承类型：
```
# 函数 isinstance()用于检查实例类型
isinstance(obj, int)
# 函数 issubclass()用于检查类继承
issubclass(bool, int)
```
4. public: name
    protect : _name
    private: __name

5. 迭代器：
```
class Reverse:
  # 定义一个 __iter__()方法，使其返回一个带有 __next__()方法的对象。
    """Iterator for looping over a sequence backwards."""
    def __init__(self, data):
        self.data = data
        self.index = len(data)
    def __iter__(self):
        return self
    def __next__(self):
        if self.index == 0:
            raise StopIteration
        self.index = self.index - 1
        return self.data[self.index]
```
6. 生成器
```
def reverse(data):
    for index in range(len(data)-1, -1, -1):
        yield data[index]
for char in reverse('golf'):
     print(char)
````