

**前言**：参考《机器学习》，对偶问题没看懂。。。。（我只是一个代码的搬运工。。。）  **机器学习专栏**：[机器学习专栏](https://blog.csdn.net/weixin_43008804/category_9386844.html)




### 文章目录


+ [支持向量机（SVM）](#SVM_7)+ 
+ [1、基本原理](#1_8)+ [2、软间隔](#2_49)+ [3、核函数](#3_80)+ [4、sklearn实现SVM](#4sklearnSVM_96)+ [5、SVM多分类](#5SVM_126)+ 
+ [4.1多分类原理](#41_127)+ [4.2sklearn实现SVM多分类](#42sklearnSVM_133)









# 支持向量机（SVM）


## 1、基本原理


现给定数据集$D={((x^{(1)},y^{(i)}),(x^{(2)},y^{(2)}),...,(x^{(m)},y^{(m)}))},y^{(i)}\in\{-1,1 \}$，我们现在的目的就是找一个**超平面**将这两个类别的样本点分开。 在样本空间中，划分超平面可以由线性方程表示为： 

$$w^Tx+b=0$$

 则样本点$x^{(i)}$到超平面$(w,x)$的距离为： 

$$r=\frac{|w^Tx^{(i)}+b|}{||w||}$$

 其中，$||w||$表示范数，这是空间的一个性质，一般指欧式范数。到原点距离的意思，超平面可以理解为平面中的直线、空间中的平面的推广到更高维度，但是作用都是划分。

一个超平面$(w,x)$可以将它所在的空间分为两半, 它的法向量指向的那一半对应的一面是它的正面, 另一面则是它的反面，假设超平面$(w,x)$能够将训练样本正确分类，即： 

$$\left\{\begin{matrix} w^Tx^{(i)}+b>0，&&y^{(i)}=+1\\ w^Tx^{(i)}+b<0,&&y^{(i)}=-1 \end{matrix}\right.$$

 支持向量机要求满足： 

$$\left\{\begin{matrix} w^Tx^{(i)}+b\geqslant+1，&&y^{(i)}=+1\\ w^Tx^{(i)}+b\leqslant -1,&&y^{(i)}=-1 \end{matrix}\right.$$

 距离超平面最近的样本点使上式等号成立，它们被称为“**支持向量**”（support vector）,两个异类支持向量到超平面的距离之和： 

$$\gamma =\frac{2}{||w||}$$

 被称为“**间隔**”（margin） 
![./figures/20191125215254833.png](./figures/20191125215254833.png)
 欲使分类效果更好，我们就要找到具有“**最大间隔**”的划分超平面，即： 

$$\mathop{max}\limits_{w,b} \quad \frac{2}{||w||} \\ s.t. \quad y^{(i)}(w^Tx^{(i)}+b)\geqslant1,\quad i=1,2,...,m$$

 最大化$\frac{2}{||w||}$等价于最小化$\frac{||w||^2}{2}$,，即： 

$$\mathop{min}\limits_{w,b} \quad \frac{||w||^2}{2} \\ s.t. \quad y^{(i)}(w^Tx^{(i)}+b)\geqslant1,\quad i=1,2,...,m$$

 这就是SVM模型，是一个QP问题。（对偶问题以后再看吧，看不懂。）

## 2、软间隔


在处理现实问题的时候，我们其实很难找到一个能刚好划分的超平面，就算找到了，我们也不能确定这个结果不是由于过拟合导致。所以我们要放宽条件，即允许一些样本不满足约束条件，我们称为“**软间隔**”。 
![./figures/20191125231506262.png](./figures/20191125231506262.png)
 但是，我们在最大化间隔的时候，应使不满足约束条件的样本点尽可能少，即： 

$$\mathop{min}\limits_{w,b} \quad \frac{||w||^2}{2}+C\sum_{i=1}^{m}l_{0/1}(y^{(i)}(w^Tx^{(i)}+b)-1)$$

 其中，$C>0$取有限值常数，$l_{0/1}$是“0/1”损失函数 

$$l_{0/1}(z)=\left\{\begin{matrix} 1,&& if\quad z<0\\ 0.&& otherwise \end{matrix}\right.$$

 但是，$l_{0/1}$非凸、非连续，数学性质不好，常用“**替代损失**”（surrogate loss）函数代替：

+ hinge损失：$l_{hinge}(z)=max(0,1-z)$+ 指数损失(exponential loss)：$l_{exp}(z)=exp(-z)$+ 对率损失(logistic loss)：$l_{log}(z)=log(1+exp(-z))$


若采用hinge损失，则模型表示为： 

$$\mathop{min}\limits_{w,b} \quad \frac{||w||^2}{2}+C\sum_{i=1}^{m}max(0,1-y^{(i)}(w^Tx^{(i)}+b))$$

 引入“**松弛变量**”$\xi_i\geqslant0$，可得“**软间隔支持向量机**”，但是要求在这个**软间隔区域**的样本点尽可能少，即： 

$$\mathop{min}\limits_{w,b} \quad \frac{||w||^2}{2}+C\sum_{i=1}^{m}\xi_i \\ s.t. \quad y^{(i)}(w^Tx^{(i)}+b)\geqslant1-\xi_i,\quad i=1,2,...,m$$



## 3、核函数


前面说的是线性可分的情况，那要是出现线性不可分怎么办？比如： 
![./figures/2019112522141040.png](./figures/2019112522141040.png)
 对于这样的问题，我们需要将样本从原始空间映射到一个更高维的特征空间，使得样本在这个特征空间线性可分。比如：现在有样本点如下，很明显我们用$x^2$二次项去拟合更好，这其实就是一个维度提升，核函数就是实现这样的作用的。 
![./figures/20191125223436308.jpg](./figures/20191125223436308.jpg)
 令$\phi(x)$表示将$x$映射后的特征向量，于是在新的特征空间的超平面表示为： 

$$f(x)=w^T\phi(x)+b$$

 此时，SVM模型表示为： 

$$\mathop{min}\limits_{w,b} \quad \frac{||w||^2}{2} \\ s.t. \quad y^{(i)}(w^T\phi(x)+b)\geqslant1,\quad i=1,2,...,m$$

 （这里等我以后再慢慢弄懂）

## 4、sklearn实现SVM


```python
# -*- coding:utf-8 -*-
"""
@author: 1
@file: SVM.py
@time: 2019/11/25 23:58
"""

from sklearn import svm
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

df = pd.read_csv(r'D:\workspace\python\machine learning\data\breast_cancer.csv',header=None)
X = df.iloc[:, 1:10]      # 属性
y = df.iloc[:, 30]       # 分类结果
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
clf = svm.SVC(gamma='scale')
'''SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0,
 decision_function_shape='ovr', degree=3, gamma='scale', kernel='rbf',
 max_iter=-1, probability=False, random_state=None, shrinking=True,
 tol=0.001, verbose=False)'''
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
print('accuracy_score:', accuracy_score(y_test, y_pred))

```


## 5、SVM多分类


### 4.1多分类原理


1、一对多法（one-versus-rest，简称1-v-r SVMs）。训练时依次把某个类别的样本归为一类,其他剩余的样本归为另一类，这样k个类别的样本就构造出了k个SVM。分类时将未知样本分类为具有最大分类函数值的那类。（**这个与逻辑回归的多分类原理相同**）

2、一对一法（one-versus-one，简称1-v-1 SVMs）。其做法是在任意两类样本之间设计一个SVM，因此k个类别的样本就需要设计k(k-1)/2个SVM。当对一个未知样本进行分类时，最后得票最多的类别即为该未知样本的类别。Libsvm中的多类分类就是根据这个方法实现的。

3、层次支持向量机（H-SVMs）。层次分类法首先将所有类别分成两个子类，再将子类进一步划分成两个次级子类，如此循环，直到得到一个单独的类别为止。

### 4.2sklearn实现SVM多分类


```python
# -*- coding:utf-8 -*-
"""
@author: 1
@file: SVM_mc.py
@time: 2019/11/26 20:34
"""


from sklearn import svm
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

df = pd.read_csv(r'D:\workspace\python\machine learning\data\iris.csv')
X = df.iloc[:, 0:4]
Y = df.iloc[:, 4]
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)
clf = svm.SVC(gamma='scale', decision_function_shape="ovr")    # 一对多法
# clf = svm.SVC(gamma='scale', decision_function_shape='ovo')  # 一对一法
clf.fit(x_train, y_train)
'''LinearSVC(C=1.0, class_weight=None, dual=True, fit_intercept=True,
 intercept_scaling=1, loss='squared_hinge', max_iter=1000,
 multi_class='ovr', penalty='l2', random_state=None, tol=0.0001,
 verbose=0)'''
y_pred = clf.predict(x_test)
dec = clf.decision_function(X)
print('accuracy_score：', accuracy_score(y_test, y_pred))
print(dec.shape[1])   # 输出构造分类器的数量

```


