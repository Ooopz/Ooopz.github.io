

**前言**：简单介绍半监督学习，无公式推导，并用sklearn实现  **机器学习专栏**：[机器学习专栏](https://blog.csdn.net/weixin_43008804/category_9386844.html) 


### 文章目录


+ [一、算法思路](#_4)+ 
+ [1、生成模型](#1_5)+ [2、物以类聚（label propagation）](#2label_propagation_7)

+ [二、标签传播算法的两种计算方式](#_10)+ 
+ [1. RBF](#1_RBF_12)+ [2. KNN](#2_KNN_14)

+ [三、sklearn实现LP算法](#sklearnLP_16)





# 一、算法思路


## 1、生成模型


先**计算样本特征的总体的联合分布**，将所有有标注的样本计算出一个分布，然后把没有标注的样本放入这个分布中，看根据这个分布它该如何被标注，这个过程可能是迭代的。

## 2、物以类聚（label propagation）


标签传播算法，LP算法是一个基于图的半监督学习的算法。类似于监督学习算法中的KNN算法，假设**越相近的点更有可能具有相同的类别标签**，然后根据少量的有标签的样本，根据一些规则判断相邻节点之间的相似性，根据相似性对为未标签的样本进行标记。

# 二、标签传播算法的两种计算方式


**（其实这里涉及图相关的算法知识）**

## 1. RBF


距离离的越近越接近于1，距离离的越远越接近于0。向基函数是某种沿径向对称的标量函数，通常定义为**样本到数据中心之间径向距离**（通常是欧氏距离）的单调函数（由于距离是径向同性的）

## 2. KNN


找一个无标注的数据，然后**取附近k个有标注的数据，无标注数据附近哪种标注的数据最多就取哪一个**（以未标注的数据为圆心做KNN，在指定范围内找到了有标注的数据，然后对未标注的数据进行打标，然后进行打标传播，直到未标注的数据全都标注以后，算法结束）

# 三、sklearn实现LP算法


```python
# -*- coding:utf-8 -*-
"""
@author: Tao_RY
@file: LP.py
@time: 2020-04-13 12:35:41
"""

import numpy as np
import pandas as pd
from sklearn.semi_supervised import LabelPropagation
from sklearn.metrics import accuracy_score, recall_score, f1_score, r2_score

df = pd.read_csv(r"C:\Users\1\WorkSpace\python\machine learning\data\iris.csv", sep=',')
labels = np.copy(df['virginica'])
train_data = df.iloc[:, [0, 1, 2, 3]]
# 标签传播算法中，未标注的数据的label必须是-1，随机选一些，标注为-1
random_unlabeled_points = np.random.randint(0, len(labels), (1, 100))
Y = labels[random_unlabeled_points][0, :]
labels[random_unlabeled_points] = -1

LP_model = LabelPropagation()
LP_model.fit(train_data, labels)
y_pred = LP_model.predict(train_data)
Y_pred = y_pred[random_unlabeled_points][0, :]   # -1的那部分重新预测

print('accuracy_score:', accuracy_score(Y, Y_pred))
```


