---
title: 《Head First Java》笔记
date: 2019-06-24 10:35:24
tags:
- JAVA
categories: JAVA 
---
# 基本概念
1. 实例变量有默认值，局部变量没有默认值。
2. JAVA中都是值的（拷贝）传递。
3. 引用到对象的变量并不是对象的容器，而是类似指向对象的指针／地址。所有引用的大小都一样。

# 类与对象
1. ArrayList&一般数组区别：
    - 一般数组创建时确定大小、以索引存放、使用特殊语法［］
    - ArrayList是参数化的 ArrayList<String>
2. final：
    - final的变量代表你不能改变它的值。
    - final的Method代表你不能覆盖这个方法
    - final的类代表你不能继承它
3. 方法的重载与多态无关，两个方法名称相同但参数不同。
4. 抽象类代表类必须要被extent，抽象方法代表方法必须要被覆盖。抽象方法没有实体。必须实现所有的抽象方法。
5. 编译器是根据引用类型（定义变量时指定的类型）判断哪个方法可以调用，而不是根据对象的实际类型。
6. extent只能有1个，implement（接口）可以有多个。
7. 一个类可以有多个构造函数，但参数必须不一样。
8. 函数构造链：创建新对象时，所有继承下来的构造函数都会执行。
9. 调用父类构造函数super().使用this()调用对象本身的其他构造函数。两者不能同时使用。
10. 静态变量：所有实例都共享的，且只会在类第一次载入的时候初始化。
    - 静态变量 == Python类变量， 非静态变量即实例变量。
    - 静态变量会在该类的任何对象创建之前就完成初始化
    - 静态变量会在该类的任何静态方法执行之前就初始化
    - 常量：静态的final变量 （常量名应全大写）

# 变量
1. 所有对象存活于可垃圾回收的堆（heap）中。
2. 变量存活空间：
    - 如果在方法体内定义的，这时候就是在栈上分配的
    - 如果是类的成员变量，这时候就是在堆上分配的
    - 如果是类的静态成员变量，在[方法区](https://blog.csdn.net/top_code/article/details/51288529)(堆，各个线程共享的内存区域)上分配的

# 异常处理
1. JAVA虚拟机只会从头开始往下找到第一个符合范围的异常处理块
2. 可以抛出多重异常 
```
    public void function name () throw PantException, LionException{}
```

# 序列化与反序列化
1. 序列化保存对象的状态
```
    FileOutputStream fileStream = new FileOutputStream (“TEST.ser”);
    ObjectOutputStream os = new ObjectOutputStream(fileStream);
    os.writeObject(characterOne);
    os.close();
```
2. 反序列化
```
    FileInputStream fileStream = new FileInputStream(“TEST.ser”);
    ObjectInputStream os = new ObjectInputStream(fileStream);
    Object one = os.readObject();
    GameChara one = (GameChara) one;
```
3. 类如果可序列化，必须implements Serializable。如果某实例变量不应该被序列化，定义为transient。

# 网络编程
1. 网络 java.net
2. 建立socket
```
    Socket s = new Socket(’127.0.0.0’,8888);
    InputStream steam = new InputStream(s.getInputStream());
    BufferReader reader = new BufferReader(stream);
    String msg = reader.readLine();
```
3. 建立socket Server
```
    ServerSocket ser = new ServerSocket(8888)
    Socket s = ser.accept()
```
4. 线程Thread 需要一个实现Runnable接口的类，类需要实现run()方法
5. 线程命名 setName()
6. synchronized修饰方法使其每次只能被一个线程存取。锁是在对象上。没有处理死锁机制。

# 集合
1. 集合
    - TreeSet:有序防重复 
    - HashMap 
    - LinkedList：针对经常插入删除 
    - HashSet 
    - LinkedHaskMap:记住元素插入顺序

# 泛型
1. 泛型的类代表类的声明用到类型函数，泛型的方法代表方法的声明特征用到类型函数。
```
    public class GenericTest {
        // 这个类是个泛型类
        public class Generic<T>{     
            private T key;

            public Generic(T key) {
                this.key = key;
            }
        }
        // 这是一个泛型方法。
        // 首先在public与返回值之间的<T>必不可少，这表明这是一个泛型方法，并且声明了一个泛型T
        // 这个T可以出现在这个泛型方法的任意位置.
        // 泛型的数量也可以为任意多个 
        public <T,K> K showKeyName(Generic<T> container){
           ...
        }
    }
```
    [Java 泛型](https://www.runoob.com/java/java-generics.html)
2. 相等
    - 引用的相等性 ＝＝
    - 对象的相等性 equals() ，必须要覆盖hashCode()方法保证两个对象有相同的hashcode
3. TreeSet集合中的元素必须实现comparable类型，或者使用重载，取用comparator参数构造函数创建TreeSet
4. 万用字符 <?>
```
    public void takeThing(ArrayList<? extent Animal> list)
    // 相当于
    public <T extent Animal> void takeThing (ArrayList<T> list)
```
5. <> 使编译器验证类型安全，不用到运行时才去验证




参考：
《Head First JAVA》
[重学Java-一个Java对象到底占多少内存](https://juejin.im/post/5d0fa403f265da1bb67a2335)