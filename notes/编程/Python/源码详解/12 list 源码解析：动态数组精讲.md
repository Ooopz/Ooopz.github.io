---
tags:
- Python/源码详解
---

# [list 源码解析：动态数组精讲](../../../目录/目录-Python%20源码详解.md)

_list_ 对象是一种 **容量自适应** 的 **线性容器** ，底层由 **动态数组** 实现。动态数组结构决定了 _list_ 对象具有优秀的尾部操作性能，但头部操作性能却很差劲。研发人员只有对底层数据结构有足够的认识，才能最大限度避免问题代码。

现成的动态数组实现很多，除了我们正在研究的 _list_ 对象，_C++_ 中的 vector 也是众所周知。虽然在实际项目中需要自行实现动态数组的场景已经很少很少了，但是源码还是有必要研究一番。源码研究不仅能加深对数据结构的理解，还能进一步提升编程水平，裨益颇多。

本节，我们开始 _list_ 对象源码，深入学习 **动态数组** 实现的艺术。

## 容量调整

当我们调用 _append_ 、_pop_ 、_insert_ 等方法时，列表长度随之发生变化。当列表长度超过底层数组容量时，便需要对底层数组进行 **扩容** ；当列表长度远低于底层数组容量时，便需要对底层数组进行 **缩容** 。

_Objects/listobject.c_ 源码表明，_append_ 等方法依赖 _list_resize_ 函数调整列表长度，扩容缩容的秘密就藏在这里！_list_resize_ 函数在调整列表长度前，先检查底层数组容量，并在必要时重新分配底层数组。接下来，我们一起来解读 _list_resize_ 函数，该函数同样位于源文件 _Objects/listobject.c_ 中：

```c
static int
list_resize(PyListObject *self, Py_ssize_t newsize)
{
    PyObject **items;
    size_t new_allocated, num_allocated_bytes;
    Py_ssize_t allocated = self->allocated;

    /* Bypass realloc() when a previous overallocation is large enough
       to accommodate the newsize.  If the newsize falls lower than half
       the allocated size, then proceed with the realloc() to shrink the list.
    */
    if (allocated >= newsize && newsize >= (allocated >> 1)) {
        assert(self->ob_item != NULL || newsize == 0);
        Py_SIZE(self) = newsize;
        return 0;
    }

    /* This over-allocates proportional to the list size, making room
     * for additional growth.  The over-allocation is mild, but is
     * enough to give linear-time amortized behavior over a long
     * sequence of appends() in the presence of a poorly-performing
     * system realloc().
     * The growth pattern is:  0, 4, 8, 16, 25, 35, 46, 58, 72, 88, ...
     * Note: new_allocated won't overflow because the largest possible value
     *       is PY_SSIZE_T_MAX * (9 / 8) + 6 which always fits in a size_t.
     */
    new_allocated = (size_t)newsize + (newsize >> 3) + (newsize < 9 ? 3 : 6);
    if (new_allocated > (size_t)PY_SSIZE_T_MAX / sizeof(PyObject *)) {
        PyErr_NoMemory();
        return -1;
    }

    if (newsize == 0)
        new_allocated = 0;
    num_allocated_bytes = new_allocated * sizeof(PyObject *);
    items = (PyObject **)PyMem_Realloc(self->ob_item, num_allocated_bytes);
    if (items == NULL) {
        PyErr_NoMemory();
        return -1;
    }
    self->ob_item = items;
    Py_SIZE(self) = newsize;
    self->allocated = new_allocated;
    return 0;
}
```

在函数开头，有几个局部变量定义，对理解函数逻辑非常关键：

- _items_ 指针，用于保存新数组；
- _new_allocated_ ，用于保存新数组容量；
- _num_allocated_bytes_ ，用于保存新数组内存大小，以字节为单位；
- _allocated_ ，用于保存旧数组容量。

然后，代码第 _12_ 行，检查新长度与底层数组容量的关系。如果新长度不超过数组容量，且不小于数组容量的一半，则无需调整底层数组，直接更新 _ob_size_ 字段。换句话讲， _list_ 对象扩缩容的条件分别如下：

- **扩容条件** ，新长度大于底层数组长度；
- **缩容条件** ，新长度小于底层数组长度的一半；

扩容或缩容条件触发时，_list_resize_ 函数根据新长度计算数组容量并重新分配底层数组（第 _27-44_ 行）：

1. 第 _27_ 行，新容量在长度加上 $\frac{1}{8}$  的裕量，再加上 _3_ 或 _6_ 的裕量；
2. 第 _28-31_ 行，如果新容量超过允许范围，返回错误；
3. 第 _33-34_ 行，如果新长度为 _0_ ，将新容量也设置为 _0_ ，因此空列表底层数组亦为空；
4. 第 _36-40_ 行，调用 _PyMem_Realloc_ 函数重新分配底层数组；
5. 第 _41-44_ 行，更新 _3_ 个关键字段，依次设置为 **新底层数组** 、 **新长度** 以及 **新容量** 。

注意到代码第 27 行，新容量的计算公式有点令人费解。为什么还要加上 _3_ 或者 _6_ 的裕量呢？试想一下，如果新长度小于 _8_ ，那么 $\frac{1}{8}$ 的裕量便是 _0_ ！这意味着，当 _list_ 对象长度从 _0_ 开始增长时，需要频繁扩容！

为了解决这个问题，必须在 $\frac{1}{8}$ 裕量的基础上额外加上一定的固定裕量。而 _3_ 和 _6_ 这两个特殊数值的选择，使得列表容量按照 _0_、_4_、_8_、 16、_25_、_35_、_46_、_58_、_72_、_88_…… 这样的序列进行扩张。这样一来，当 _list_ 对象长度较小时，容量翻倍扩展，扩容频率得到有效限制。

顺便提一下， _PyMem_Realloc_ 函数是 _Python_ 内部实现的内存管理函数之一，功能与 _C_ 库函数 _realloc_ 类似：

```c
PyAPI_FUNC(void *) PyMem_Realloc(void *ptr, size_t new_size);
```

_PyMem_Realloc_ 函数用于对动态内存进行扩容或者缩容，关键步骤如下：

1. 新申请一块尺寸为 _new_size_ 的内存区域；
2. 将数据从旧内存区域 _ptr_ 拷贝到新内存区域；
3. 释放旧内存区域 _ptr_ ；
4. 返回新内存区域。

![](../../../附件/python%20源码详解/PYS1201.png)

**内存管理** 是最考验研发人员编程功底的领域之一，鼓励大家到 _PyMem_Realloc_ 源码（_./Objects/obmalloc.c_）中进一步研究内存管理的技巧。学有余力的童鞋，可模仿着自己实现一个 _realloc_ 函数，假以时日编程内功将突飞猛进！

## 尾部追加

_append_ 方法在 _Python_ 内部由 _C_ 函数 _list_append_ 实现，而 _list_append_ 进一步调用 _app1_ 函数完成元素追加：

```c
static int
app1(PyListObject *self, PyObject *v)
{
    Py_ssize_t n = PyList_GET_SIZE(self);

    assert (v != NULL);
    if (n == PY_SSIZE_T_MAX) {
        PyErr_SetString(PyExc_OverflowError,
            "cannot add more objects to list");
        return -1;
    }

    if (list_resize(self, n+1) < 0)
        return -1;

    Py_INCREF(v);
    PyList_SET_ITEM(self, n, v);
    return 0;
}
```

1. 第 _4_ 行，调用 _PyList_GET_SIZE_ 取出列表长度，即 _ob_size_ 字段；
2. 第 _7-11_ 行，判断列表当前长度，如果已经达到最大限制，则报错；
3. 第 _13-15_ 行，调用 _list_resize_ 更新列表长度，必要时 _list_resize_ 对底层数组进行 **扩容** ；
4. 第 _16_ 行，自增元素对象 **引用计数** (元素对象新增一个来自列表对象的引用)；
5. 第 17 行，将元素对象指针保存到列表最后一个位置，列表新长度为 _n+1_ ，最后一个位置下标为 _n_ 。

我们看到，有了 _list_resize_ 这个辅助函数后， _app1_ 函数的实现就非常直白了。接下来，我们将看到 _insert_、_pop_ 等方法的实现中也用到这个函数，从中可体会到程序逻辑 **划分** 、 **组合** 的巧妙之处。

## 头部插入

_insert_ 方法在 _Python_ 内部由 _C_ 函数 _list_insert_impl_ 实现，而 _list_insert_impl_ 则调用 _ins1_ 函数完成元素插入：

```c
static int
ins1(PyListObject *self, Py_ssize_t where, PyObject *v)
{
    Py_ssize_t i, n = Py_SIZE(self);
    PyObject **items;
    if (v == NULL) {
        PyErr_BadInternalCall();
        return -1;
    }
    if (n == PY_SSIZE_T_MAX) {
        PyErr_SetString(PyExc_OverflowError,
            "cannot add more objects to list");
        return -1;
    }

    if (list_resize(self, n+1) < 0)
        return -1;

    if (where < 0) {
        where += n;
        if (where < 0)
            where = 0;
    }
    if (where > n)
        where = n;
    items = self->ob_item;
    for (i = n; --i >= where; )
        items[i+1] = items[i];
    Py_INCREF(v);
    items[where] = v;
    return 0;
}
```

1. 第 _4_ 行，调用 _PyList_GET_SIZE_ 取出列表长度，即 _ob_size_ 字段；
2. 第 _10-14_ 行，判断列表当前长度，如果已经达到最大限制，则报错；
3. 第 _16-17_ 行，调用 _list_resize_ 更新列表长度，必要时 _list_resize_ 对底层数组进行 **扩容** ；
4. 第 _19-23_ 行，检查插入位置下标，如果下标为负数，加上 _n_ 将其转换为非负数；
5. 第 _21-22_、_24-25_ 行，检查插入位置下标是否越界，如果越界则设为开头或结尾；
6. 第 _26-28_ 行，将插入位置以后的所有元素逐一往后移一个位置，特别注意 _for_ 循环必须 **从后往前** 迭代；
7. 第 _29_ 行，自增元素对象 **引用计数** (元素对象新增一个来自列表对象的引用)；
8. 第 _30_ 行，将元素对象指针保存到列表指定位置。

_Python_ 序列 **下标很有特色** ，除了支持 _0~n-1_ 这样的惯例外，还支持 **倒数下标** 。倒数下标为负数，从后往前数：最后一个元素为 _-1_ ，倒数第二个为 _-2_ ；以此类推，第一个元素下标为： _-n_ 。

![](../../../附件/python%20源码详解/pys1202.png)

倒数下标非常实用，可以很方便地取出序列最后几个元素，而不用关心序列的长度。 _Python_ 内部处理倒数下标时，自动为其加上长度序列 _n_ ，便转化成普通下标了。

## 弹出元素

_pop_ 方法将指定下标的元素从列表中弹出，下标默认为 _-1_ 。换句话讲，如果未指定下标，_pop_ 弹出最后一个元素：

```python
>>> help(list.pop)
Help on method_descriptor:

pop(self, index=-1, /)
    Remove and return item at index (default last).

    Raises IndexError if list is empty or index is out of range.
```

_pop_ 方法在 _Python_ 内部由 _C_ 函数 _list_pop_impl_ 实现：

```c
static PyObject *
list_pop_impl(PyListObject *self, Py_ssize_t index)
{
    PyObject *v;
    int status;

    if (Py_SIZE(self) == 0) {
        /* Special-case most common failure cause */
        PyErr_SetString(PyExc_IndexError, "pop from empty list");
        return NULL;
    }
    if (index < 0)
        index += Py_SIZE(self);
    if (index < 0 || index >= Py_SIZE(self)) {
        PyErr_SetString(PyExc_IndexError, "pop index out of range");
        return NULL;
    }
    v = self->ob_item[index];
    if (index == Py_SIZE(self) - 1) {
        status = list_resize(self, Py_SIZE(self) - 1);
        if (status >= 0)
            return v; /* and v now owns the reference the list had */
        else
            return NULL;
    }
    Py_INCREF(v);
    status = list_ass_slice(self, index, index+1, (PyObject *)NULL);
    if (status < 0) {
        Py_DECREF(v);
        return NULL;
    }
    return v;
}
```

1. 第 _7-11_ 行，如果列表为空，没有任何元素可弹出，抛出 _IndexError_ 异常；
2. 第 _12-13_ 行，如果给定下标为 **倒数下标** ，先加上列表长度，将其转换成普通下标；
3. 第 _14-16_ 行，检查给定下标是否在合法范围内，超出合法范围同样抛出 _IndexError_ 异常；
4. 第 _18_ 行，从底层数组中取出待弹出元素；
5. 第 _19-25_ 行，如果待弹出元素为列表最后一个，调用 _list_resize_ 快速调整列表长度即可，无需移动其他元素；
6. 第 _26-31_ 行，其他情况下调用 _list_ass_slice_ 函数删除元素，调用前需要通过 _Py_INCREF_ 增加元素引用计数，因为 _list_ass_slice_ 函数内部将释放被删除元素；
7. 第 32 行，将待弹出元素返回。

_list_ass_slice_ 函数其实有两种不同的语义，具体执行哪种语义由函数参数决定，函数接口如下：

```c
/* a[ilow:ihigh] = v if v != NULL.
 * del a[ilow:ihigh] if v == NULL.
 *
 * Special speed gimmick:  when v is NULL and ihigh - ilow <= 8, it's
 * guaranteed the call cannot fail.
 */
static int
list_ass_slice(PyListObject *a, Py_ssize_t ilow, Py_ssize_t ihigh, PyObject *v);
```

- **删除语义** ，如果最后一个参数 _v_ 值为 _NULL_ ，执行删除语义，即：_del a[ilow: ihigh]_ ；
- **替换语义** ，如果最后一个参数 _v_ 值不为 _NULL_ ，执行替换语义，即 _a[ilow: ihigh] = v_ 。

因此，代码第 _27_ 行中， _list_ass_slice_ 函数执行删除语义，将 _[index, index+1)_ 范围内的元素删除。由于半开半闭区间 _[index, index+1)_ 中只包含 _index_ 一个元素，效果等同于将下标为 _index_ 的元素删除。

执行删除语义时， _list_ass_slice_ 函数将被删元素后面的元素逐一往前移动，以便重新覆盖删除操作所造成的空隙。由此可见，_pop_ 方法弹出元素，时间复杂度跟弹出位置有关：

- 最好时间复杂度 ( **尾部弹出** )，$O(1)$ ；
- 最坏时间复杂度 ( **头部弹出** )，$O(n)$；
- 平均时间复杂度， $O(\frac{n}{2})$ ，亦即 $O(n)$ 。

![](../../../附件/python%20源码详解/pys1203.png)

因此，调用 _pop_ 方法弹出非尾部元素时，需要非常谨慎。

## 删除元素

_remove_ 方法将给定元素从列表中删除。与 _pop_ 略微不同，_remove_ 方法直接给定待删除元素，而不是元素下标。_remove_ 方法在 _Python_ 内部由 _C_ 函数 _list_remove_ 实现：

```c
static PyObject *
list_remove(PyListObject *self, PyObject *value)
/*[clinic end generated code: output=f087e1951a5e30d1 input=2dc2ba5bb2fb1f82]*/
{
    Py_ssize_t i;

    for (i = 0; i < Py_SIZE(self); i++) {
        int cmp = PyObject_RichCompareBool(self->ob_item[i], value, Py_EQ);
        if (cmp > 0) {
            if (list_ass_slice(self, i, i+1,
                               (PyObject *)NULL) == 0)
                Py_RETURN_NONE;
            return NULL;
        }
        else if (cmp < 0)
            return NULL;
    }
    PyErr_SetString(PyExc_ValueError, "list.remove(x): x not in list");
    return NULL;
}
```

_list_remove_ 函数先遍历列表中每个元素（第 _7_ 行），检查元素是否为待删除元素 _value_ （第 _8_ 行），以此确定下标。然后， _list_remove_ 函数调用 _list_ass_slice_ 函数进行删除。注意到，如果给定元素不存在， _list_remove_ 将抛出 _ValueError_ 异常。

由此可见，_remove_ 方法在删除前有一个时间复杂度为 O(n)O(n) 的查找过程，性能不甚理想，须谨慎使用。

## 小结

_list_ 对象是一种 **容量自适应** 的 **线性容器** ，底层由 **动态数组** 实现。_Python_ 内部由函数 _list_resize_ 调整列表长度， _list_resize_ 自动为列表进行 **扩容** 或者 **缩容** ：

- 底层数组容量不够时，需要进行 **扩容** ；
- 扩容时， _Python_ 额外分配大约 1/81/8 的容量裕量，以控制扩容频率；
- 底层数组空闲位置超过一半时，需要进行 **缩容** 。

动态数组的特性决定了 _list_ 对象相关操作性能有好有坏，使用时须特别留意：

- _append_ 向尾部追加元素，时间复杂度为 $O(1)$ ，放心使用；
- _insert_ 往列表插入元素，最坏时间复杂度是 $O(n)$ ，平均时间复杂度也是 $O(n)$，须谨慎使用；
- _pop_ 从列表中弹出元素，最好时间复杂度为 $O(1)$ ，平均时间复杂度为 $O(n)$ ，弹出非尾部元素时需谨慎；
- _remove_ 从列表中删除元素，时间复杂度为 $O(n)$，同样须谨慎使用。