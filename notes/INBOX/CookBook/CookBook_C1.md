# CookBook

## 数据结构和算法

### 1.1 多变量赋值


```python
data = [ 'ACME', 50, 91.1, (2012, 12, 21) ]
a, b, c, (e,f,g) = data
print(f)
```

```ad-result
12
```


### 1.2 序列解包


```python
data = 'hello'
a, *b, c = data
print(a)
print(b)
print(c)
```

```ad-result
h
['e', 'l', 'l']
o
```


### 1.3 保留最后 N 个元素


```python
## deque 可以指定长度，且最旧的元素会优先被移除
## deque 在头部和尾部的操作复杂度都为 O(1)

from collections import deque

def search(lines, pattern, history=1):
    search_res = deque(maxlen=history)
    for line in lines:
        if pattern in line:
            search_res.append(line)
            yield line, search_res

text = """
    python cookbook
    is good for
    python developer
"""

for line, search_res in search(text.split("\n"), 'python', 1):
    print(search_res)
```

```ad-result
deque(['    python cookbook'], maxlen=1)
deque(['    python developer'], maxlen=1)
```


### 1.4 查找最大或最小的 N 个元素


```python
import heapq

nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
print(heapq.nlargest(3, nums)) 
print(heapq.nsmallest(3, nums))

portfolio = [
    {'name': 'IBM', 'shares': 100, 'price': 91.1},
    {'name': 'AAPL', 'shares': 50, 'price': 543.22},
    {'name': 'FB', 'shares': 200, 'price': 21.09},
    {'name': 'HPQ', 'shares': 35, 'price': 31.75},
    {'name': 'YHOO', 'shares': 45, 'price': 16.35},
    {'name': 'ACME', 'shares': 75, 'price': 115.65}
]
cheap = heapq.nsmallest(3, portfolio, key=lambda s: s['price'])
most = heapq.nlargest(3, portfolio, key=lambda s: s['shares'])
print(cheap)
print(most)

## 堆数据结构最重要的特征是 heap[0] 永远是最小的元素
heap = nums
heapq.heapify(heap)
print(heapq.heappop(heap))
print(heapq.heappop(heap))
print(heapq.heappop(heap))
```

```ad-result
[42, 37, 23]
[-4, 1, 2]
[{'name': 'YHOO', 'shares': 45, 'price': 16.35}, {'name': 'FB', 'shares': 200, 'price': 21.09}, {'name': 'HPQ', 'shares': 35, 'price': 31.75}]
[{'name': 'FB', 'shares': 200, 'price': 21.09}, {'name': 'IBM', 'shares': 100, 'price': 91.1}, {'name': 'ACME', 'shares': 75, 'price': 115.65}]
-4
1
2
```


### 1.5 实现一个优先级队列


```python
import heapq

class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]
    
class Item:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return 'Item({!r})'.format(self.name)

q = PriorityQueue()
q.push(Item('foo'), 1)
q.push(Item('bar'), 5)
q.push(Item('spam'), 4)
q.push(Item('grok'), 1)
print(q.pop())
print(q.pop())
print(q.pop())
print(q.pop())
```

    Item('bar')
    Item('spam')
    Item('foo')
    Item('grok')


### 1.6 字典中的键映射多个值


```python
from collections import defaultdict

d = defaultdict(list)
d['a'].append(1)
d['a'].append(2)
d['b'].append(4)

print(d)
```

    defaultdict(<class 'list'>, {'a': [1, 2], 'b': [4]})


### 1.7 字典排序


```python
## OrderedDict 内部维护着一个根据键插入顺序排序的双向链表
## 每次当一个新的元素插入进来的时候， 它会被放到链表的尾部
## 对于一个已经存在的键的重复赋值不会改变键的顺序
## 需要注意的是，一个 OrderedDict 的大小是一个普通字典的两倍

from collections import OrderedDict

d = OrderedDict()
d['foo'] = 1
d['bar'] = 2
d['spam'] = 3
d['grok'] = 4
for key in d:
    print(key, d[key])

import json
json.dumps(d)
```

    foo 1
    bar 2
    spam 3
    grok 4





    '{"foo": 1, "bar": 2, "spam": 3, "grok": 4}'



### 1.8 字典的运算


```python
prices = {
    'ACME': 45.23,
    'AAPL': 612.78,
    'IBM': 205.55,
    'HPQ': 37.20,
    'FB': 10.75
}

min_price = min(zip(prices.values(), prices.keys()))
max_price = max(zip(prices.values(), prices.keys()))

print(min_price)
print(max_price)
```

    (10.75, 'FB')
    (612.78, 'AAPL')


### 1.9 查找两字典的相同点


```python
a = {
    'x' : 1,
    'y' : 2,
    'z' : 3
}

b = {
    'w' : 10,
    'x' : 11,
    'y' : 2
}


print(a.keys() & b.keys())

print(a.keys() - b.keys())

print(a.items() & b.items())

c = {key:a[key] for key in a.keys() - {'z', 'w'}}
print(c)
```

    {'y', 'x'}
    {'z'}
    {('y', 2)}
    {'y': 2, 'x': 1}


### 1.10 删除序列相同元素并保持顺序


```python
# hashable对象 可用
def dedupe(items):
    seen = set()
    for item in items:
        if item not in seen:
            seen.add(item)
            yield item

a = [1, 5, 2, 1, 9, 1, 5, 10]
print(list(dedupe(a)))

# unhashable对象可用
def dedupe(items, key=None):
    seen = set()
    for item in items:
        val = item if key is None else key(item)
        if val not in seen:
            seen.add(val)
            yield item
a = [ {'x':1, 'y':2}, {'x':1, 'y':3}, {'x':1, 'y':2}, {'x':2, 'y':4}]
print(list(dedupe(a, key=lambda d: (d['x'],d['y']))))
print(list(dedupe(a, key=lambda d: d['x'])))
```

    [1, 5, 2, 9, 10]
    [{'x': 1, 'y': 2}, {'x': 1, 'y': 3}, {'x': 2, 'y': 4}]
    [{'x': 1, 'y': 2}, {'x': 2, 'y': 4}]


### 1.11 命名切片


```python
record = '....................100 .......513.25 ..........'
cost = int(record[20:23]) * float(record[31:37])
SHARES = slice(20, 23)
PRICE = slice(31, 37)
cost = int(record[SHARES]) * float(record[PRICE])
print(cost)

s = 'HelloWorld'
a = slice(5, 50, 2)
a.indices(len(s)) # indices(size) 方法将 slice 映射到一个已知大小的序列上。
for i in range(*a.indices(len(s))):
    print(s[i])
```

    51325.0
    W
    r
    d


### 1.12 序列中出现次数最多的元素


```python
from collections import Counter

words = [
    'look', 'into', 'my', 'eyes', 'look', 'into', 'my', 'eyes',
    'the', 'eyes', 'the', 'eyes', 'the', 'eyes', 'not', 'around', 'the',
    'eyes', "don't", 'look', 'around', 'the', 'eyes', 'look', 'into',
    'my', 'eyes', "you're", 'under'
]
morewords = ['why','are','you','not','looking','in','my','eyes']

word_counts = Counter(words)
print(word_counts)
top_three = word_counts.most_common(3)
print(top_three)

a = Counter(words)
b = Counter(morewords)
c = a + b
d = a - b
print(c)
print(d)
```

    Counter({'eyes': 8, 'the': 5, 'look': 4, 'into': 3, 'my': 3, 'around': 2, 'not': 1, "don't": 1, "you're": 1, 'under': 1})
    [('eyes', 8), ('the', 5), ('look', 4)]
    Counter({'eyes': 9, 'the': 5, 'look': 4, 'my': 4, 'into': 3, 'not': 2, 'around': 2, "don't": 1, "you're": 1, 'under': 1, 'why': 1, 'are': 1, 'you': 1, 'looking': 1, 'in': 1})
    Counter({'eyes': 7, 'the': 5, 'look': 4, 'into': 3, 'my': 2, 'around': 2, "don't": 1, "you're": 1, 'under': 1})


### 1.13 通过某个关键字排序一个字典列表


```python
from operator import itemgetter

rows = [
    {'fname': 'Brian', 'lname': 'Jones', 'uid': 1003},
    {'fname': 'David', 'lname': 'Beazley', 'uid': 1002},
    {'fname': 'John', 'lname': 'Cleese', 'uid': 1001},
    {'fname': 'Big', 'lname': 'Jones', 'uid': 1004}
]

rows_by_fname = sorted(rows, key=itemgetter('fname'))
rows_by_uid = sorted(rows, key=itemgetter('uid'))
print(rows_by_fname)
print(rows_by_uid)
```

    [{'fname': 'Big', 'lname': 'Jones', 'uid': 1004}, {'fname': 'Brian', 'lname': 'Jones', 'uid': 1003}, {'fname': 'David', 'lname': 'Beazley', 'uid': 1002}, {'fname': 'John', 'lname': 'Cleese', 'uid': 1001}]
    [{'fname': 'John', 'lname': 'Cleese', 'uid': 1001}, {'fname': 'David', 'lname': 'Beazley', 'uid': 1002}, {'fname': 'Brian', 'lname': 'Jones', 'uid': 1003}, {'fname': 'Big', 'lname': 'Jones', 'uid': 1004}]


### 1.14 排序不支持原生比较的对象


```python
from operator import attrgetter

users = [User(31), User(23), User(99)]

class User:
    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return 'User({})'.format(self.user_id)

def sort_notcompare():
    users = [User(23), User(3), User(99)]
    print(users)
    print(sorted(users, key=lambda u: u.user_id))
    
print(sorted(users, key=attrgetter('user_id')))
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-28-f7269facbc93> in <module>
          1 from operator import attrgetter
          2 
    ----> 3 users = [User(31), User(23), User(99)]
          4 
          5 class User:


    NameError: name 'User' is not defined


### 1.15 通过某个字段将记录分组


```python
## groupby() 函数扫描整个序列并且查找连续相同值（或者根据指定 key 函数返回值相同）的元素序列
## 若值相同但不连续则会分到不同的组

from operator import itemgetter
from itertools import groupby

rows = [
    {'address': '5412 N CLARK', 'date': '07/01/2012'},
    {'address': '5148 N CLARK', 'date': '07/04/2012'},
    {'address': '5800 E 58TH', 'date': '07/02/2012'},
    {'address': '2122 N CLARK', 'date': '07/03/2012'},
    {'address': '5645 N RAVENSWOOD', 'date': '07/02/2012'},
    {'address': '1060 W ADDISON', 'date': '07/02/2012'},
    {'address': '4801 N BROADWAY', 'date': '07/01/2012'},
    {'address': '1039 W GRANVILLE', 'date': '07/04/2012'},
]

rows.sort(key=itemgetter('date')) #
for date, items in groupby(rows, key=itemgetter('date')):
    print(date)
    for i in items:
        print(' ', i)
```

    07/01/2012
      {'address': '5412 N CLARK', 'date': '07/01/2012'}
      {'address': '4801 N BROADWAY', 'date': '07/01/2012'}
    07/02/2012
      {'address': '5800 E 58TH', 'date': '07/02/2012'}
      {'address': '5645 N RAVENSWOOD', 'date': '07/02/2012'}
      {'address': '1060 W ADDISON', 'date': '07/02/2012'}
    07/03/2012
      {'address': '2122 N CLARK', 'date': '07/03/2012'}
    07/04/2012
      {'address': '5148 N CLARK', 'date': '07/04/2012'}
      {'address': '1039 W GRANVILLE', 'date': '07/04/2012'}


### 1.16 过滤序列元素


```python
from itertools import compress

mylist = [1, 4, -5, 10, -7, 2, 3, -1]
neg = [n for n in mylist if n < 0]
pos = (n for n in mylist if n > 0)
print(neg)
print(list(pos))

values = ['1', '2', '-3', '-', '4', 'N/A', '5']
def is_int(val):
    try:
        x = int(val)
        return True
    except ValueError:
        return False
ivals = list(filter(is_int, values))
print(ivals)

addresses = [
    '5412 N CLARK',
    '5148 N CLARK',
    '5800 E 58TH',
    '2122 N CLARK',
    '5645 N RAVENSWOOD',
    '1060 W ADDISON',
    '4801 N BROADWAY',
    '1039 W GRANVILLE',
]
counts = [ 0, 3, 10, 4, 1, 7, 6, 1]
more5 = [n > 5 for n in counts]
res = list(compress(addresses, more5))
print(res)
```

    [-5, -7, -1]
    [1, 4, 10, 2, 3]
    ['1', '2', '-3', '4', '5']
    ['5800 E 58TH', '1060 W ADDISON', '4801 N BROADWAY']


### 1.17 从字典中提取子集


```python
prices = {
    'ACME': 45.23,
    'AAPL': 612.78,
    'IBM': 205.55,
    'HPQ': 37.20,
    'FB': 10.75
}

p1 = {key: value for key, value in prices.items() if value > 200}
print(p1)

tech_names = {'AAPL', 'IBM', 'HPQ', 'MSFT'}
p2 = {key: value for key, value in prices.items() if key in tech_names}
print(p2)
```

    {'AAPL': 612.78, 'IBM': 205.55}
    {'AAPL': 612.78, 'IBM': 205.55, 'HPQ': 37.2}


### 1.18 映射名称到序列元素


```python
from collections import namedtuple
Subscriber = namedtuple('Subscriber', ['addr', 'joined'])
sub = Subscriber('jonesy@example.com', '2012-10-19')
print(sub)
print(sub.addr)
print(sub.joined)
```

    Subscriber(addr='jonesy@example.com', joined='2012-10-19')
    jonesy@example.com
    2012-10-19


### 1.19 转换并同时计算数据


```python
nums = range(100000)
%timeit s = sum(x * x for x in nums)
%timeit s1 = sum((x * x for x in nums)) # 比前一个表达式有更多的开销
%timeit s2 = sum([x * x for x in nums]) # 消耗更多内存
```

    10.1 ms ± 27.2 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
    9.87 ms ± 250 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
    9.02 ms ± 21.3 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)


### 1.20 合并多个字典或映射


```python
from collections import ChainMap

a = {'x': 1, 'z': 3 }
b = {'y': 2, 'z': 4 }

## ChainMap 使用原来的字典，它自己不创建新的字典
c = ChainMap(a,b)
print(c['x'])
print(c['y'])
print(c['z']) # 如果出现重复键，那么第一次出现的映射值会被返回

## 对于字典的更新或删除操作总是影响的是列表中第一个字典
c['z'] = 10
c['w'] = 40
del c['x']
print(c)

del c['y'] # 第一个字典没有键 y
```

    1
    2
    3
    ChainMap({'z': 10, 'w': 40}, {'y': 2, 'z': 4})



    ---------------------------------------------------------------------------

    KeyError                                  Traceback (most recent call last)

    /opt/anaconda3/lib/python3.8/collections/__init__.py in __delitem__(self, key)
        950         try:
    --> 951             del self.maps[0][key]
        952         except KeyError:


    KeyError: 'y'

    
    During handling of the above exception, another exception occurred:


    KeyError                                  Traceback (most recent call last)

    <ipython-input-34-43d6557a409c> in <module>
         16 print(c)
         17 
    ---> 18 del c['y']
    

    /opt/anaconda3/lib/python3.8/collections/__init__.py in __delitem__(self, key)
        951             del self.maps[0][key]
        952         except KeyError:
    --> 953             raise KeyError('Key not found in the first mapping: {!r}'.format(key))
        954 
        955     def popitem(self):


    KeyError: "Key not found in the first mapping: 'y'"

