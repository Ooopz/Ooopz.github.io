---
tags:
- Python/源码详解
---

上一小节，我们重新考察了 **生成器** ( _generator_ ) 的运行时行为，发现了它神秘的一面。生成器函数体代码可以通过 _yield_ 关键字暂停和恢复执行，这个特性可以用来实现 **协程** 。

那么，生成器诸多神奇特性是如何实现的呢？为了更好地理解生成器协程，我们有必要深入研究它的运行机制。

## 生成器的创建

我们对上节中的 _co_process_ 生成器略加修改后作为研究对象，继续深入字节码，力求洞察生成器执行的原理：

```python
def co_process(arg):
    print('task with argument {} started'.format(arg))
    
    data = yield 1
    print('step one finished， got {} from caller'.format(data))
    
    data = yield 2
    print('step two finished， got {} from caller'.format(data))
    
    data = yield 3
    print('step three finished， got {} from caller'.format(data))
```

_co_process_ 是一个特殊的函数对象，它被调用后并不会立刻执行函数体，而是得到一个生成器对象：

```python
>>> co_process
<function co_process at 0x109768f80>
>>> genco = co_process('foo')
>>> genco
<generator object co_process at 0x109629450>
>>> genco.__class__
<class 'generator'>
```

在函数机制部分，我们知道函数调用由 _CALL_FUNCTION_ 字节码负责：

```python
>>> import dis
>>> dis.dis(compile("co_process('foo')", '', 'exec'))
  1           0 LOAD_NAME                0 (co_process)
              2 LOAD_CONST               0 ('foo')
              4 CALL_FUNCTION            1
              6 POP_TOP
              8 LOAD_CONST               1 (None)
             10 RETURN_VALUE
```

那么，什么情况下函数调用会返回生成器呢？顺着 _CALL_FUNCTION_ 字节码处理逻辑，不难找到答案。

_CALL_FUNCTION_ 字节码在 _Python/ceval.c_ 中处理，它主要是调用 _call_function_ 函数完成工作。_call_function_ 函数根据被调用对象类型区别处理，可分为 **类方法** 、 **函数对象** ， **普通可调用对象** 等等。

在这个例子中，被调用对象是函数对象。因此，_call_function_ 函数调用位于 _Objects/call.c_ 中的 __PyFunction_FastCallKeywords_ 函数，而它则进一步调用位于 _Python/ceval.c_ 的 __PyEval_EvalCodeWithName_ 函数。

__PyEval_EvalCodeWithName_ 函数先为目标函数 _co_process_ 创建 **栈帧** 对象 _f_，然后检查代码对象标识。若代码对象带有 _CO_GENERATOR_ 、_CO_COROUTINE_ 或 _CO_ASYNC_GENERATOR_ 标识，便创建生成器并返回：

```c
    /* Handle generator/coroutine/asynchronous generator */
    if (co->co_flags & (CO_GENERATOR | CO_COROUTINE | CO_ASYNC_GENERATOR)) {
        PyObject *gen;
        PyObject *coro_wrapper = tstate->coroutine_wrapper;
        int is_coro = co->co_flags & CO_COROUTINE;
        
        // 省略

        /* Create a new generator that owns the ready to run frame
         * and return that as the value. */
        if (is_coro) {
            gen = PyCoro_New(f, name, qualname);
        } else if (co->co_flags & CO_ASYNC_GENERATOR) {
            gen = PyAsyncGen_New(f, name, qualname);
        } else {
            gen = PyGen_NewWithQualName(f, name, qualname);
        }
        if (gen == NULL) {
            return NULL;
        }
        
        // 省略

        return gen;
    }
```

代码对象标识 _co_flags_ 在编译时由语法规则确定，通过 _co_process_ ，我们可以找到其代码对象标识：

```python
>>> co_process.__code__.co_flags
99
```

_CO_GENERATOR_ 宏定义于 _Include/code.h_ 头文件，它的值是 _0x20_ ，_co_process_ 代码对象确实带有该标识：

```python
>>> co_process.__code__.co_flags & 0x20
32
```

注意到，用于保存 _co_process_ 函数执行上下文的栈帧对象 _f_ ，作为一个重要字段保存于生成器对象 _gen_ 中：

![图片描述](../../../附件/python%20源码详解/pys3801.png)

至此，生成器对象的创建过程已经浮出水面。与普通函数一样，当 _co_process_ 被调用时，_Python_ 将为其创建栈帧对象，用于维护函数执行上下文 —— **代码对象** 、 **全局名字空间** 、 **局部名字空间** 以及 **运行栈** 都在其中。

与普通函数不同的是，_co_process_ 代码对象带有生成器标识。_Python_ 不会立即执行代码对象，栈帧对象也不会被接入调用链，因此 _f_back_ 字段是空的。相反，_Python_ 创建了一个生成器对象，并将其作为函数调用结果返回。

生成器对象底层由 _PyGenObject_ 结构体表示，定义于 _Include/genobject.h_ 头文件中。生成器类型对象同样由 _PyTypeObject_ 结构体表示，全局只有一个，以全局变量的形式定义于 _Objects/genobject.c_ 中，也就是 _PyGen_Type_ 。

_PyGenObject_ 结构体中的字段也很好理解，顾名即可思义，这也体现了变量名的作用：

- _ob_refcnt_ ，**引用计数** ，这是任何对象都包含的公共字段；
- _ob_type_ ，**对象类型** ，指向其类型对象，这也是任何对象都包含的公共字段；
- _gi_frame_ ，生成器执行时所需的 **栈帧对象** ，用于保存执行上下文信息；
- _gi_running_ ，标识生成器是否运行中；
- _gi_code_ ，**代码对象** ；
- _gi_weakreflist_ ，弱引用相关，不深入讨论；
- _gi_name_ ，生成器名；
- _gi_qualname_ ，同上；
- _gi_exec_state_ ，生成器执行状态；

最后，可以在 _Python_ 中访问生成器对象 _genco_ ，进一步印证我们在源码中得到的结论：

```python
# 生成器创建后，尚未开始执行
>>> genco.gi_running
False

# 栈帧对象
>>> genco.gi_frame
<frame at 0x110601c90, file '<stdin>', line 1, code co_process>

# 生成器和栈帧的代码对象，均来自 co_process 函数对象
>>> genco.gi_code
<code object co_process at 0x11039c4b0, file "<stdin>", line 1>
>>> genco.gi_frame.f_code
<code object co_process at 0x11039c4b0, file "<stdin>", line 1>
>>> co_process.__code__
<code object co_process at 0x11039c4b0, file "<stdin>", line 1>
```

## 生成器的执行

在前面例子中，_co_process_ 函数被调用后，返回生成器 _genco_ 。这时，函数体尚未开始执行。

```python
>>> genco.gi_frame.f_lasti
-1
```

栈帧对象 _f_lasti_ 字段记录当前字节码执行进度，_-1_ 表示尚未开始执行。

经过前一小节学习，我们知道：借助 _next_ 内建函数或者 _send_ 方法可以启动生成器，并驱动它不断执行。这意味着，生成器执行的秘密可以通过这两个函数找到。

我们先从 _next_ 函数入手，作为内建函数，它定义于 _Python/bltinmodule.c_ 源文件，_C_ 语言函数 _builtin_next_ 是也。_builtin_next_ 函数逻辑非常简单，除了类型检查等样板式代码，最关键的是这一行：

```c
res = (*it->ob_type->tp_iternext)(it);
```

这行代码表明，_next_ 函数实际上调用了生成器类型对象的 _tp_iternext_ 函数完成工作。这听上去有些拗口，用 _Python_ 的语言来描述就清晰多了 —— _next(genco)_ 等价于：

```python
>>> genco.__class__.__next__(genco)
task with argument foo started
1
```

还记得 _Python_ **对象模型** 部分内容吗？类型对象决定实例对象的行为，实例对象相关操作函数的指针都保存在类型对象中。生成器作为 _Python_ 对象中的一员，当然也遵守这一法则。

顺着生成器类型对象的肉身 _PyGen_Type_ ( _Objects/genobject.c_ )，很快就可以摸到 _gen_iternext_ 函数。

另一方面， _genco.send_ 也可以启动并驱动生成器的执行，根据 _Objects/genobject.c_ 中的方法定义，它底层调用 __PyGen_Send_ 函数：

```c
static PyMethodDef gen_methods[] = {
    {"send",(PyCFunction)_PyGen_Send, METH_O, send_doc},
    {"throw",(PyCFunction)gen_throw, METH_VARARGS, throw_doc},
    {"close",(PyCFunction)gen_close, METH_NOARGS, close_doc},
    {NULL, NULL}        /* Sentinel */
};
```

不管 _gen_iternext_ 函数还是 __PyGen_Send_ 函数，都是直接调用 _gen_send_ex_ 函数完成工作的：

![图片描述](../../../附件/python%20源码详解/pys3802.png)

因此，不管是执行 _next(genco)_ 还是 _genco.send(None)_ ，最终都由 _gen_send_ex_ 函数处理，_next_ 和 _send_ 的等价性也源于此。经过千辛万苦，我们终于找到了理解生成器运行机制的关键所在。

_gen_send_ex_ 函数同样位于 _Objects/genobject.c_ 源文件，函数挺长，但最关键的代码只有两行：

```c
f->f_back = tstate->frame;

// ...

result = PyEval_EvalFrameEx(f, exc);
```

首先，第一行代码将生成器栈帧挂到当前调用链上；然后，第二行代码调用 _PyEval_EvalFrameEx_ 开始执行生成器栈帧；生成器栈帧对象保存着生成器执行上下文，其中 _f_lasti_ 字段跟踪生成器代码对象的执行进度。

![图片描述](../../../附件/python%20源码详解/pys3803.png)

_PyEval_EvalFrameEx_ 函数最终调用 __PyEval_EvalFrameDefault_ 函数执行 _frame_ 对象上的代码对象。这个函数我们在虚拟机部分学习过，对它并不陌生。虽然它体量巨大，超过 _3_ 千行代码，逻辑却非常直白 —— 内部由无限 _for_ 循环逐条遍历并处理字节码，每执行完一条字节码就自增 _f_lasti_ 字段。

## 生成器的暂停

我们知道，生成器可以利用 _yield_ 语句，将执行权归还给调用者。因此，生成器暂停执行的秘密就隐藏在 _yield_ 语句中。我们先来看看 _yield_ 语句编译后，生成什么字节码：

```python
>>> import dis
>>> dis.dis(co_process)
```

可以看到，_co_process_ 每个 _yield_ 语句编译后，都得到这样 _3_ 条字节码指令：

```python
  4          14 LOAD_CONST               2 (1)
             16 YIELD_VALUE
             18 STORE_FAST               1 (data)
```

首先，_LOAD_CONST_ 将需要带给调用者的值 ( _yield_ 右边的表达式值) 加载到运行栈栈顶：

![图片描述](../../../附件/python%20源码详解/pys3804.png)\
接着，_YIELD_VALUE_ 开始放大招，它先从栈顶弹出 _yield_ 值作为 __PyEval_EvalFrameDefault_ 函数返回值，然后一个 _goto_ 语句跳出 _for_ 循环，干净利落：

```c
        TARGET(YIELD_VALUE) {
            retval = POP();

            if (co->co_flags & CO_ASYNC_GENERATOR) {
                PyObject *w = _PyAsyncGenValueWrapperNew(retval);
                Py_DECREF(retval);
                if (w == NULL) {
                    retval = NULL;
                    goto error;
                }
                retval = w;
            }

            f->f_stacktop = stack_pointer;
            why = WHY_YIELD;
            goto fast_yield;
        }
```

紧接着，__PyEval_EvalFrameDefault_ 函数将当前栈帧 (也就是生成器的栈帧) 从调用链中解开。注意到，_yield_ 值被 __PyEval_EvalFrameDefault_ 函数返回，并最终被 _send_ 方法或 _next_ 函数返回给调用者。

![图片描述](../../../附件/python%20源码详解/pys3805.png)

## 生成器的恢复

当我们再次调用 _send_ 方法时，生成器将恢复执行：

```python
>>> genco.send('hello')
step one finished， got hello from caller
2
```

注意到，通过 _send_ 发送的数据作为 _yield_ 语句的值，被生成器获取并保存在局部变量 _data_ ，进而被输出。这一切是如何做到的呢？我们接着分析。

我们知道，_send_ 方法被调用后，_Python_ 先把生成器栈帧对象挂到调用链，并最终调用 _PyEval_EvalFrameEx_ 函数逐条执行字节码。在这个过程中，_send_ 发送的数据会被放在生成器栈顶：

![图片描述](../../../附件/python%20源码详解/pys3806.png)

生成器执行进度被保存在 _f_lasti_ 字段，生成器将从下一条字节码指令 _STORE_FAST_ 继续执行。_STORE_FAST_ 指令从栈顶取出 _send_ 发来的数据，并保存到局部变量 _data_ ：

![图片描述](../../../附件/python%20源码详解/pys3807.png)

再接着，生成器将按照正常的逻辑，有条不紊地执行，直到遇到下一个 _yield_ 语句或者生成器函数返回。

至此，生成器执行、暂停、恢复的全部秘密皆已揭开！

- 生成器函数编译后代码对象带有 _CO_GENERATOR_ 标识；
- 如果函数代码对象带 _CO_GENERATOR_ 标识，被调用时 _Python_ 将创建生成器对象；
- 生成器创建的同时，_Python_ 还创建一个栈帧对象，用于维护代码对象执行上下文；
- 调用 _next_/_send_ 驱动生成器执行，_Python_ 将生成器栈帧对象接入调用链，开始执行字节码；
- 执行到 _yield_ 语句时，_Python_ 将 _yield_ 右边的值放入栈顶，并结束字节码执行循环，执行权回到上一个栈帧；
- _yield_ 值最终作为 _next_ 函数或 _send_ 方法的返回值，被调用者取得；
- 再次调用 _next/__send_ ，_Python_ 重新将生成器栈帧对象接入调用链恢复执行，通过 _send_ 发送的值被放在栈顶；
- 生成器函数重新启动后，从 _YIELD_VALUE_ 后的字节码恢复执行，可从栈顶获得调用者发来的值；
- 代码执行权就这样在调用者和生成器间来回切换，而生成器栈顶被用来传值；

生成器运行机制全面解密后，我们便可以利用这些特性来实现协程。下一节，我们将通过自己的双手，实现一个完整的协程库！这个玩具代码量仅 _100_ 来行，却揭示了协程库的核心机密。经过这次实战，我们将彻底驾驭协程，在协程应用开发中更加游刃有余。