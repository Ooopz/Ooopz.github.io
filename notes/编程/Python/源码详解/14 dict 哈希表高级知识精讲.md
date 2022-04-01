---
tags:
- Python/源码详解
---

# [dict 哈希表高级知识精讲](../../../目录/目录-Python%20源码详解.md)

上一小节，我们通过源码学习，研究了 _dict_ 对象的内部结构，并找到隐藏其中的秘密—— **哈希表** 。**关联式容器** 一般由 **平衡搜索树** 或 **哈希表** 来实现，_dict_ 选用 **哈希表** ，主要考虑 **搜索效率** 。但哈希表 **稀疏** 的特性，意味着巨大的内存开销。为优化内存使用，_Python_ 别出心裁地将哈希表分成两部分来实现：**哈希索引** 以及 **键值对存储** 数组。

尽管如此，由于篇幅关系，很多细节我们还没来得及讨论。本节，我们再接再厉，继续研究 **哈希函数** 、**哈希冲突**、**哈希攻击** 以及 **删除操作** 等高级知识点，彻底掌握哈希表设计精髓。

## 哈希值

_Python_ 内置函数 _hash_ 返回对象 **哈希值** ，**哈希表** 依赖 **哈希值** 索引元素：

![](../../../附件/python%20源码详解/pys1401.png)

根据哈希表性质， **键对象** 必须满足以下两个条件，否则哈希表便不能正常工作：

- 哈希值在对象整个生命周期内不能改变；
- 可比较，且比较相等的对象哈希值必须相同；

满足这两个条件的对象便是 **可哈希** ( _hashable_ )对象，只有可哈希对象才可作为哈希表的键。因此，诸如 dict 、set 等底层由哈希表实现的容器对象，其键对象必须是可哈希对象。

_Python_ 内建对象中的 **不可变对象** ( _immutable_ )都是可哈希对象；而诸如 _list_ 、_dict_ 等 **可变对象** 则不是：

```python
>>> hash([])
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unhashable type: 'list'
```

不可哈希对象不能作为 _dict_ 对象的键，显然 _list_ 、 _dict_ 等均不是合法的键对象：

```python
>>> {
...     []: 'list is not hashable'
... }
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
TypeError: unhashable type: 'list'
>>>
>>> {
...     {}: 'dict is not hashable either'
... }
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
TypeError: unhashable type: 'dict'
```

而用户自定义的对象默认便是可哈希对象，对象哈希值由对象地址计算而来，且任意两个不同对象均不相等：

```python
>>> class A:
...     pass
...
>>>
>>> a = A()
>>> b = A()
>>>
>>> hash(a), hash(b)
(-9223372036573452351, -9223372036573452365)
>>>
>>> a == b
False
```

那么，哈希值如何计算呢？答案是—— **哈希函数** 。在对象模型部分，我们知道对象行为由类型对象决定。 **哈希值** 计算作为对象行为中的一种，秘密也隐藏在类型对象中—— _tp_hash_ 函数指针。而内置函数 _hash_ 则依赖类型对象中的 _tp_hash_ 函数，完成哈希值计算并返回。

以 _str_ 对象为例，其哈希函数位于 _Objects/unicodeobject.c_ 源文件，_unicode_hash_ 是也：

```c
PyTypeObject PyUnicode_Type = {
    PyVarObject_HEAD_INIT(&PyType_Type, 0)
    "str",              /* tp_name */
    sizeof(PyUnicodeObject),        /* tp_size */
    // ...

    (hashfunc) unicode_hash,        /* tp_hash*/

    // ...
    unicode_new,            /* tp_new */
    PyObject_Del,           /* tp_free */
};
```

对于用户自定义的对象，可以实现 _**hash**_ 魔术方法，重写默认哈希值计算方法。举个例子，假设标签类 _Tag_ 的实例对象由 _value_ 字段唯一标识，便可以根据 value 字段实现 **哈希函数** 以及 **相等性** 判断：

```python
class Tag:

    def __init__(self, value, title):
        self.value = value
        self.title = title

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return self.value == other.value
```

哈希值 **使用频率** 较高，而且在对象生命周期内均不变。因此，可以在对象内部对哈希值进行缓存，避免重复计算。以 _str_ 对象为例，内部结构中的 _hash_ 字段便是用于保存哈希值的。

理想的哈希函数必须保证哈希值尽量均匀地分布于整个哈希空间，越是相近的值，其哈希值差别应该越大。

## 哈希冲突

一方面，不同的对象，哈希值有可能相同，另一方面，与哈希值空间相比，哈希表的槽位是非常有限的。因此，存在多个键被映射到哈希索引的同一槽位的可能性，这便是 **哈希冲突** ！

![](../../../附件/python%20源码详解/pys1402.png)

解决哈希冲突的常用方法有两种：

- **分离链接法** ( _separate chaining_ ) ；
- **开放地址法** ( _open addressing_ )；

### 分离链接法

**分离链接法** 为每个哈希槽维护一个链表，所有哈希到同一槽位的键保存到对应的链表中：

![](../../../附件/python%20源码详解/pys1403.png)

如上图，**哈希索引** 每个槽位都接着一个 **链表** ，初始状态为空；哈希到某个槽位的 **键** 则保存于对应的链表中。例如，_key1_ 和 _key3_ 都哈希到下标为 3 的槽位，依次保存于槽位对应的链表中。

### 开放地址法

_Python_ 采用 **开放地址法** ( _open addressing_ )，将数据直接保存于哈希槽位中，如果槽位已被占用，则尝试另一个。

![](../../../附件/python%20源码详解/pys1404.png)

如上图，_key3_ 哈希到槽位 _3_ ，但已被 _key1_ 占用了；接着尝试槽位 _5_ 并成功保存。那么，槽位 _5_ 是如何决定的呢？一般而言，第 $i$ 次尝试在首槽位基础上加上一定的偏移量 $d_i$ 。因此，探测方式因函数 $d_i$ 而异。常见的方法有 **线性探测** ( _linear probing_ )以及 **平方探测** ( _quadratic probing_ )。

**线性探测** ，顾名思义， $d_i$ 是一个线性函数，例如 $d_i = 2 * i$：

![](../../../附件/python%20源码详解/pys1405.png)

**平方探测** ，顾名思义， $d_i$ 是一个平方函数，例如 $d_i = i^2$：

![](../../../附件/python%20源码详解/pys1406.png)

**线性探测** 和 **平方探测** 很简单，平方探测似乎更胜一筹。如果哈希表存在局部热点，探测很难快速跳过热点区域，而 **平方探测** 则好很多。然而，这两种方法都不够好——因为固定的探测序列加大了冲突的概率。

![](../../../附件/python%20源码详解/pys1407.png)

如图 _key_ 和 _key2_ 等都哈希到槽位 _1_ ，由于探测序列式相同的，因此冲突概率很高。_Python_ 对此进行了优化，探测函数参考对象哈希值，生成不同的探测序列，进一步降低哈希冲突的可能性：

![](../../../附件/python%20源码详解/pys1408.png)

_Python_ 探测方法在 _lookdict_ 函数中实现，位于 _Objects/dictobject.c_ 源文件内。关键代码如下：

```c
static Py_ssize_t _Py_HOT_FUNCTION
lookdict(PyDictObject *mp, PyObject *key,
         Py_hash_t hash, PyObject **value_addr)
{
    size_t i, mask, perturb;
    PyDictKeysObject *dk;
    PyDictKeyEntry *ep0;

top:
    dk = mp->ma_keys;
    ep0 = DK_ENTRIES(dk);
    mask = DK_MASK(dk);
    perturb = hash;
    i = (size_t)hash & mask;

    for (;;) {
        Py_ssize_t ix = dk_get_index(dk, i);
        // 省略键比较部分代码

        // 计算下个槽位
        // 由于参考了对象哈希值，探测序列因哈希值而异
        perturb >>= PERTURB_SHIFT;
        i = (i*5 + perturb + 1) & mask;
    }
    Py_UNREACHABLE();
}
```

## 哈希攻击

_Python_ 在 _3.3_ 以前， **哈希算法** 只根据对象本身计算哈希值。因此，只要 _Python_ 解释器相同，对象哈希值也肯定相同。我们执行 _Python 2_ 解释器启动一个交互式终端，并计算字符串 _fasion_ 的哈希值：

```python
>>> import os
>>> os.getpid()
2878
>>> hash('fasion')
3629822619130952182
```

我们再次执行 _Python 2_ 解释器启动另一个交互式终端，发现字符串 _fasion_ 的哈希值保存不变：

```python
>>> import os
>>> os.getpid()
2915
>>> hash('fasion')
3629822619130952182
```

如果一些别有用心的人构造出大量哈希值相同的 _key_ ，并提交给服务器，会发生什么事情呢？例如，向一台 _Python 2 Web_ 服务器 _post_ 一个 _json_ 数据，数据包含大量的 _key_ ，所有 _key_ 的哈希值相同。这意味着哈希表将频繁发生哈希冲突，性能由 O(1)O(1) 急剧下降为 O(N)O(N)，被活生生打垮！这就是 **哈希攻击** 。

问题很严重，好在应对方法却很简单——为对象加把 **盐** ( _salt_ )。具体做法如下：

1. _Python_ 解释器进程启动后，产生一个随机数作为 **盐** ；
2. 哈希函数同时参考 **对象本身** 以及 **随机数** 计算哈希值；

这样一来，攻击者无法获悉解释器内部的随机数，也就无法构造出哈希值相同的对象了！_Python_ 自 _3.3_ 以后，哈希函数均采用加盐模式，杜绝了 **哈希攻击** 的可能性。_Python_ 哈希算法在 _Python/pyhash.c_ 源文件中实现，有兴趣的童鞋可以学习一下，这里就不再展开了。

执行 _Python 3.7_ 解释器，启动一个交互式终端，并计算字符串 _fasion_ 的哈希值：

```python
>>> hash('fasion')
7411353060704220518
```

再次执行 _Python 3.7_ 解释器，启动另一个交互式终端，发现字符串 _fasion_ 的哈希值已经变了：

```python
>>> hash('fasion')
1784735826115825426
```

## 删除操作

现在回过头来讨论 _dict_ 哈希表的 **删除** 操作，以下图这个场景为例：

![](../../../附件/python%20源码详解/pys1409.png)

_key1_ 最先插入，使用了哈希槽位 _5_ 以及存储单元 _0_ ；紧接着插入 _key2_ ，使用了哈希槽位 _1_ 以及存储单元 _1_ ；最后插入 _key3_ 时，由于哈希槽位被 _key2_ 占用，改用槽位 _6_ 。

如果需要删除 _key2_ ，该如何操作呢？假设我们在将哈希槽位设置为 _EMPTY_ ，并将存储单元标记为删除：

![](../../../附件/python%20源码详解/pys1410.png)

这样一来，由于 _key3_ 哈希到的槽位 _1_ 是空的，便误以为 _key3_ 不存在。换句话讲，_key3_ 不翼而飞了！因此，删除元素时，必须将对应的哈希槽设置为一个特殊的标识 _DUMMY_ ，避免中断哈希探测链：

![](../../../附件/python%20源码详解/pys1411.png)

哈希槽位状态常量在 _Objects/dict-common.h_ 头文件中定义：

```c
#define DKIX_EMPTY (-1)
#define DKIX_DUMMY (-2)  /* Used internally */
#define DKIX_ERROR (-3)
```

那么，被删除的存储单元如何复用呢？_Python_ 压根就没想费这个劲，直接使用新的不就好了吗？假设现在新插入 _key4_ ，_Python_ 并不理会已删除存储单元 _1_ ，直接使用新的存储单元 _3_ ：

![](../../../附件/python%20源码详解/pys1412.png)

是的，存储单元中可能有一些是浪费的，但却无伤大雅。如果存储单元已用完，_Python_ 则执行一次容量调整操作，重新分配一个哈希表，并将所有元素搬过去，简单粗暴：

![](../../../附件/python%20源码详解/pys1413.png)

新哈希表规模由当前 _dict_ 当前元素个数决定，因此容量调整有可能是 **扩容** 、**缩容** 或者 **保持不变** 。无论怎样，新哈希表创建后，便有新存储单元可用了！