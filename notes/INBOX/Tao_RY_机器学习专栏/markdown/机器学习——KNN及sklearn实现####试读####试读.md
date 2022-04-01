

**前言**：简单介绍KNN算法，sklearn实现  **机器学习专栏**：[机器学习专栏](https://blog.csdn.net/weixin_43008804/category_9386844.html) 


### 文章目录


+ [一、KNN算法原理](#KNN_4)+ [二、算法参数](#_21)+ 
+ [1、距离](#1_22)+ [2、K值](#2K_32)

+ [二、sklearn实现KNN](#sklearnKNN_38)





# 一、KNN算法原理


K近邻算法是一种“懒惰学习”（lazy learning），就是你给我一个测试样本，我才需要去处理。与其相反的是“急切学习”（eager learning），即是在训练阶段就对数据进行处理。

对于分类问题，KNN算法步骤：

+ 计算test样本与每一个train样本的**距离**；+ 按照距离的递增关系进行排序；+ 选取**距离最小的K个train样本**；+ 确定前K个所train样本在类别的出现**频率**；+ 返回前K个train样本中出现频率最高的类别作为测试数据的预测分类。


若是回归任务，修改步骤5，可用下面两种：

+ “平均法”将找出的K个train样本的实值输出的平均值作为预测结果；+ “加权平均”计算K个train样本的加权平均，距离越近的样本其权重越大。


【算法的变种】：对数据采样不均匀（就是可能会出现样本密度分布不均匀）的情况下，我们可以使用一定半径内的样本点代替K个train样本。 
![./figures/20191201133521432.jpg](./figures/20191201133521432.jpg)
 （图源网络，侵删！）

# 二、算法参数


## 1、距离


在KNN中，通过计算对象间距离来作为各个对象之间的非相似性指标，避免了对象之间的匹配问题，一般使用欧氏距离或曼哈顿距离：

+ 欧式距离 

$$d=\sqrt {\sum_{j=1}^{n}(x1_j-x2_j)^2}$$

+ 曼哈顿距离 

$$d=\sqrt {\sum_{j=1}^{n}{|x1_j-x2_j|}}$$




## 2、K值


一、K值过小 $\quad$ “学习”近似误差会减小，只有与输入实例很近或相似的训练实例才会对预测结果起作用，容易发生**过拟合**； 二、K值过大 $\quad$ 可以减少学习的估计误差，但缺点是学习的近似误差会增大。这时候，与输入实例较远（不相似的）训练实例也会对预测器作用，容易发生**欠拟合**，使预测发生错误。 
![./figures/20191201130006910.png](./figures/20191201130006910.png)


# 二、sklearn实现KNN


1、最近邻分类

```python
# -*- coding:utf-8 -*-
"""
@author: 1
@file: KNN_c.py
@time: 2019/12/2 12:00
"""


from sklearn import neighbors
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.metrics import accuracy_score

n_neighbors = 15          # K
df = pd.read_csv(r'D:\workspace\python\machine learning\data\iris.csv')
X = df.iloc[:, 0:4]
y = df.iloc[:, 4]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

clf = neighbors.KNeighborsClassifier(n_neighbors, weights='uniform')
# weights = 'uniform' 为每个近邻分配统一的权重。而 weights = 'distance' 分配权重与查询点的距离成反比。
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
print('accuracy_score:', accuracy_score(y_test, y_pred))

```


2、最近邻回归

```python
# -*- coding:utf-8 -*-
"""
@author: 1
@file: KNN_L.py
@time: 2019/12/2 12:44
"""


from sklearn import neighbors
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split

# 导入波士顿房价数据集load_diabetes()
diabetes_X = pd.read_csv(r'D:\workspace\python\machine learning\data\diabetes_data.csv\X.csv', sep=' ', header=None)
diabetes_Y = pd.read_csv(r'D:\workspace\python\machine learning\data\diabetes_target.csv\y.csv', sep=' ', header=None)

# 利用sklearn里面的包来对数据集进行划分，以此来创建训练集和测试集
# train_size表示训练集所占总数据集的比例
diabetes_X_train, diabetes_X_test, diabetes_y_train, diabetes_y_test = train_test_split(diabetes_X, diabetes_Y,
                                                                                        train_size=0.80)
n_neighbors = 5

knn = neighbors.KNeighborsRegressor(n_neighbors, weights='distance')
knn.fit(diabetes_X_train, diabetes_y_train)
y_pred = knn.predict(diabetes_X_test)

plt.plot(range(len(diabetes_y_test)), diabetes_y_test, 'b', label='test')
plt.plot(range(len(y_pred)), y_pred, 'r', label='pred')
plt.xticks(())
plt.legend()
plt.show()

```



![./figures/20191203010841624.png](./figures/20191203010841624.png)


