

**前言**：数学知识太复杂，似懂非懂  **机器学习专栏**：[机器学习专栏](https://blog.csdn.net/weixin_43008804/category_9386844.html) 


### 主成分分析


+ [一、主成分分析原理](#_4)+ [二、最近重构性和最大可分性](#_10)+ 
+ [1、最近重构性](#1_11)+ [2、最大可分性](#2_24)

+ [三、sklearn实现PCA](#sklearnPCA_37)





# 一、主成分分析原理


主成分分析（Principal components analysis，以下简称PCA）是最重要的降维方法之一。由于各变量间存在一定的相关关系，因此有可能用较少的综合指标分别综合存在于各变量中的各类信息，在数据压缩消除冗余和数据噪音消除等领域都有广泛的应用。 首先考虑一个问题：对于正交属性空间中的样本点，如何用一个超平面（直线的高维推广）对所有样本进行恰当的表达？可以想到，若存在这样的超平面，那么它大概具有这样的性质：

+ 最近重构性：样本点到这个超平面的距离足够近+ 最大可分性：样本点在这个超平面上的投影能尽可能的分开


# 二、最近重构性和最大可分性


## 1、最近重构性


首先对数据样本的每个属性进行中心化，即$\sum_{i=1}^{m} x_j^{(i)}=0$。设投影变换后新空间坐标系为$\{w_1,w_2,...,w_n\}$，其中$w_i$是标准正交向量基（$||w_i||_2=1,w_i^Tw_j=0$）。 现我们要求降维，即丢弃新坐标系中的部分坐标（$n'<n$），则样本点$x^{(i)}$在低维坐标系中的投影是$z^{(i)}=(z^{(i)}_1,z^{(i)}_2,...,z^{(i)}_{n'})$，其中$z^{(i)}_j=w^T_jx^{(i)}$ 若基于$z^{(i)}$来重构$x^{(i)}$，则会得到$\hat{x^{(i)}}=\sum_{j=1}^{n'}z^{(i)}_jw_j$，则考虑整个训练集，原样本点$x^{(i)}$和新样本点$\hat{x^{(i)}}$的距离为： 

$$\sum_{i=1}{m}||\hat{x^{(i)}}-x^{(i)}||_2^2=\sum_{i=1}^{m}{z^{(i)}}^{T}z^{(i)}-2\sum_{i=1}^{m}{z^{(i)}}^TW^Tx^{(i)}+const \\\qquad \qquad \quad\propto -tr(W^T(\sum_{i=1}^{m}x^{(i)}{x^{(i)}}^T))$$

 其中，$W=(w_1,w_2,...,w_n)$。根据最小重构性，得： 

$$\mathop{min} \limits_W \quad -tr(W^TXX^TW) \\ s.t. W^TW=I$$



## 2、最大可分性


从最大可分性角度出发，应该使投影后的样本点的方差最大化 
![./figures/20191204164017768.png](./figures/20191204164017768.png)
 投影后样本点的协方差矩阵是$\sum_{i=1}^{m}W^Tx^{(i)}{x^{(i)}}^TW$，于是优化目标为： 

$$\mathop{max} \limits_W \quad tr(W^TXX^TW) \\ s.t. W^TW=I$$

 对上式使用拉格朗日乘子法得： 

$$XX^Tw^{(j)}=\lambda_jw_j$$

 对协方差矩阵$XX^T$进行特征值分解，将求得的特征值排序：$\lambda_1\geq \lambda_2...\geq \lambda_n$，再取前$n'$个特征值对应的特征值构成$W^*=(w_1,w_2,...,w_{n'})$，这就是主成分分析的解。（$n'$个主成分）

# 三、sklearn实现PCA


```python
# -*- coding:utf-8 -*-
"""
@author: 1
@file: PCA.py
@time: 2019/12/4 20:38
"""


import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.decomposition import PCA           # 加载PCA算法包
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn import svm
import pandas as pd


df = pd.read_csv(r'D:\workspace\python\machine learning\data\iris.csv')
X = df.iloc[:, 0:4]
Y = df.iloc[:, 4]
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)
pca = PCA(n_components=2)       # 加载PCA算法，设置降维后主成分数目为2
reduced_x = pca.fit_transform(X)  # 对样本进行降维
reduced_x = pd.DataFrame(reduced_x)

# SVM分类
x_train, x_test, y_train, y_test = train_test_split(reduced_x, Y, test_size=0.2)
clf = svm.SVC(gamma='scale', decision_function_shape="ovr")    # 一对多法
# clf = svm.SVC(gamma='scale', decision_function_shape='ovo')  # 一对一法
clf.fit(x_train, y_train)
y_pred = clf.predict(x_test)


# 可视化,画分类结果图
N, M = 500, 500  # 横纵各采样多少个值
x1_min, x2_min = x_train.min(axis=0)
x1_max, x2_max = x_train.max(axis=0)
t1 = np.linspace(x1_min, x1_max, N)
t2 = np.linspace(x2_min, x2_max, M)
x1, x2 = np.meshgrid(t1, t2)  # 生成网格采样点
x_show = np.stack((x1.flat, x2.flat), axis=1)  # 测试点
y_predict = clf.predict(x_show)
cm_light = mpl.colors.ListedColormap(['#A0FFA0', '#FFA0A0', '#A0A0FF'])
cm_dark = mpl.colors.ListedColormap(['g', 'r', 'b'])
plt.pcolormesh(x1, x2, y_predict.reshape(x1.shape), cmap=cm_light)
plt.scatter(x_train.iloc[:, 0], x_train.iloc[:, 1], c=y_train, cmap=cm_dark, marker='o', edgecolors='k')
plt.grid(True, ls=':')
plt.show()

```


分类结果图： 
![./figures/20191205190224887.png](./figures/20191205190224887.png)


