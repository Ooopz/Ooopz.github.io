

**前言**：参考《机器学习》，简单介绍朴素贝叶斯分类器  **机器学习专栏**：[机器学习专栏](https://blog.csdn.net/weixin_43008804/category_9386844.html)




### 文章目录


+ [一、贝叶斯定理](#_5)+ [二、贝叶斯分类法](#_17)+ [三、sklearn实现贝叶斯分类](#sklearn_48)





# 一、贝叶斯定理


贝叶斯定理（Bayes’ theorem）是概率论中的一个定理，描述在已知一些条件下，某事件的发生概率。

+ 条件概率公式：$P(B|A)=\frac {P(A,B)}{P(B)}$+ 贝叶斯公式：$P(A|B)=\frac{P(A,B)}{P(B)}=\frac {P(B|A)·P(A)}{P(B)}$


其中，

+ P(A)是A的先验概率或边缘概率，它不考虑任何B方面的因素；+ P(A|B)是已知B发生后A的条件概率，也由于得自B的取值而被称作A的后验概率；+ P(B|A)是已知A发生后B的条件概率，也由于得自A的取值而被称作B的后验概率；+ P(B)是B的先验概率或边缘概率，也作标准化常量(normalized constant)。


# 二、贝叶斯分类法


现给定数据集$D={((x^{(1)},y^{(i)}),(x^{(2)},y^{(2)}),...,(x^{(m)},y^{(m)}))}$，假设有K种可能的类别标记，$C=\{c_1,c_2,...,c_K\}$，则$,y^{(i)}\in\{c_1,c_2,...,c_k\}$。

贝叶斯分类的实质就是：给定一个样本$x^{(i)}$，其属于类别k的概率为：$P(c_k|x^{(i)})$，贝叶斯分类的分类结果就是条件概率$P(c|x^{(i)})$（或者称为似然）最大的那个类别，即： 

$$\mathop{arg\;max}\limits_{c_k\in C}\;P(c_k|x^{(i)})$$

 我们将我们前面介绍的贝叶斯公式换成符合数据集D的形式： 

$$P(c|x)=\frac {P(x|c)·P(c)}{P(x)}$$

 给定数据集的情况下，我们利用大数定律就可以确定$P(c)$，对于确定的样本$x$（$x=[x_1,x_2,...,x_n]$）n为属性个数，对所有类别来说$P(x)$也是确定的。 **假设各个属性相互独立**（这就是“朴素”），则： 

$$P(x|c)=\prod_{j=1}^{n}P(x_j|c)$$



基于上面所述的贝叶斯判定准则，可以得出朴素贝叶斯分类器的表达式为： 

$$h_{nb}(x)=\mathop{arg\;max}\limits_{c\in C}\;P(c)\prod_{j=1}^{n}P(x_j|c)$$



+ 对离散属性，令$D_{c,x_i}$表示$D_c$中在第j个属性上取值为$x_j$的样本组成的集合，则： 

$$P(x_j|c)=\frac{|D_{c,x_i}|}{|D_c|}$$

+ 对连续属性可使用概率密度函数，假定$p(x_j|c)\sim N(\mu_{c,j},\delta^2_{c,i})$，其中$\mu_{c,j},\delta^2_{c,i}$分别表示第c类样本在第i个属性上取值的均值和方差，则： 

$$p(x_i|c)=\frac{1}{\sqrt {2\pi}\delta_{c,i}}exp(-\frac{(x_i-\mu_{c,i})^2}{2\delta^2_{c,i}})$$




明显可以看出朴素贝叶斯分类器更适用于离散属性，所以我们也可以考虑连续离散化处理的方法。

# 三、sklearn实现贝叶斯分类


```python
# -*- coding:utf-8 -*-
"""
@author: 1
@file: bayes.py
@time: 2019/11/30 1:25
"""

from sklearn.naive_bayes import GaussianNB
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

df = pd.read_csv(r'D:\workspace\python\machine learning\data\iris.csv')
X = df.iloc[:, 0:3]
Y = df.iloc[:, 4]
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)
# 属性假设为高斯分布
gnb = GaussianNB()
model = gnb.fit(x_train, y_train)
y_pred = model.predict(x_test)
print('accuracy_score：', accuracy_score(y_test, y_pred))

```


