---
tags: 
- Python/魔法方法
---

# python 的常用魔法方法

## 构造和初始化

`__init__` 我们很熟悉了,它在对象初始化的时候调用,我们一般将它理解为"构造函数".

实际上, 当我们调用 `x = SomeClass()` 的时候调用,`__init__` 并不是第一个执行的, `__new__` 才是。所以准确来说,是 `__new__` 和 `__init__` 共同构成了"构造函数".

`__new__` 是用来创建类并返回这个类的实例, 而 `__init__` 只是将传入的参数来初始化该实例.

`__new__` 在创建一个实例的过程中必定会被调用,但 `__init__` 就不一定，比如通过 `pickle.load` 的方式反序列化一个实例时就不会调用 `__init__`。

`__new__` 方法总是需要返回该类的一个实例，而 `__init__` 不能返回除了 None 的任何值。比如下面例子:

```python
classFoo(object):

    def__init__(self):
        print 'foo __init__'
        return None  # 必须返回None,否则抛TypeError

    def__del__(self):
        print 'foo __del__'
```

实际中,你很少会用到 `__new__`，除非你希望能够控制类的创建。
如果要讲解 `__new__`，往往需要牵扯到 `metaclass`(元类)的介绍。

对于 `__new__` 的重载， [Python 文档](https://www.python.org/download/releases/2.2/descrintro/#__new__) 中也有了详细的介绍。

在对象的生命周期结束时, `__del__` 会被调用,可以将 `__del__` 理解为"析构函数".
`__del__` 定义的是当一个对象进行垃圾回收时候的行为。

有一点容易被人误解, 实际上，`x.__del__()` 并不是对于 `del x` 的实现,但是往往执行 `del x` 时会调用 `x.__del__()`.

怎么来理解这句话呢? 继续用上面的 Foo 类的代码为例:

```python
foo = Foo()
foo.__del__()
print foo
del foo
print foo  # NameError, foo is not defined
```

如果调用了 `foo.__del__()`，对象本身仍然存在. 但是调用了 `del foo`, 就再也没有 foo 这个对象了.

请注意，如果解释器退出的时候对象还存在，就不能保证 `__del__` 被确切的执行了。所以 `__del__` 并不能替代良好的编程习惯。
比如，在处理 socket 时，及时关闭结束的连接。
