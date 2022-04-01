

**前言**：有三维聚类图，我只是一个代码的搬运工。。。  **机器学习专栏**：[机器学习专栏](https://blog.csdn.net/weixin_43008804/category_9386844.html)




### 文章目录


+ [k-均值（k-means）聚类](#kkmeans_5)+ 
+ [1、k-均值算法](#1k_6)+ [2、k-均值算法的代价函数](#2k_10)+ [3、k-均值算法步骤](#3k_14)+ [4、初始化聚类中心点和聚类个数](#4_20)+ [5、sklearn实现k-means算法](#5sklearnkmeans_26)







# k-均值（k-means）聚类


## 1、k-均值算法


k-均值算法是一种无监督学习，是一种“基于原型的聚类”（prototype-based clustering）方法，给定的数据是不含标签的$公式解析异常$，目标是找出数据的模式特征进行分类。如社交网络分析，通过用户特征进行簇划分，分出不同群体。 
![./figures/20191119110045609.png](./figures/20191119110045609.png)
 (图源网络，侵删)

## 2、k-均值算法的代价函数


给定数据集$公式解析异常$，k-均值聚类算法的代价函数（基于欧式距离的平方误差）为： 

$$J=\frac{m}{1}\sum_{i=1}^{m}||x^{(i)}-u_{c^{(i)}}||^2$$

 其中，$c^{(i)}$是训练样例$x^{(i)}$分配的聚类序号；$u_{c^{(i)}}$是 $x^{(i)}$所属聚类的中心点 。k-均值算法的代价函数函数的物理意义就是，训练样例到其所属的聚类中心点的距离的平均值。

## 3、k-均值算法步骤


k-均值算法主要包括：根据聚类中心分配样本类别——>更新聚类中心

+ 随机选择K个聚类中心$u_1,u_2,...,u_K$；+ 从1~m中遍历所有的数据集，计算$x^{(i)}$分别到$u_1,u_2,...,u_K$的距离，记录距离最短的聚类中心点$u_k$，然后把$x^{(i)}$这个点分配给这个簇，即令 $c^{(i)}=k$；+ 从1~k中遍历所有的聚类中心，移动聚类中心的新位置到这个簇的均值处，即$u_k=\frac{1}{c_k}\sum_{j=1}^{c_k}x^{(j)}$，其中$c_k$表示这个簇的样本数；+ 重复步骤2，直到聚类中心不再移动。


## 4、初始化聚类中心点和聚类个数


1、在实际应用的过程中，聚类结果会和我们初始化的聚类中心相关，因为代价函数可能会收敛在一个局部最优解上，而不是全局最优解。我们的解决方法是**多次初始化**，然后**选取代价函数最小的**。 
![./figures/20191120183857492.jpg](./figures/20191120183857492.jpg)
 2、如果没有特别的业务要求，聚类个数如何选取？我们可以把聚类个数作为横坐标，代价函数作为纵坐标，找出拐点。 
![./figures/20191120183911722.jpg](./figures/20191120183911722.jpg)


## 5、sklearn实现k-means算法


推荐一篇博文： [聚类效果评价](https://blog.csdn.net/sinat_26917383/article/details/70577710)  主函数KMeans

```python
sklearn.cluster.KMeans(n_clusters=8,
	 init='k-means++', 
	n_init=10, 
	max_iter=300, 
	tol=0.0001, 
	precompute_distances='auto', 
	verbose=0, 
	random_state=None, 
	copy_x=True, 
	n_jobs=1, 
	algorithm='auto'
	)
```


参数解释：

+ n_clusters:簇的个数，即你想聚成几类+ init: 初始簇中心的获取方法+ n_init: 获取初始簇中心的更迭次数，为了弥补初始质心的影响，算法默认会初始10次质心，实现算法，然后返回最好的结果。+ max_iter: 最大迭代次数（因为kmeans算法的实现需要迭代）+ tol: 容忍度，即kmeans运行准则收敛的条件+ precompute_distances：是否需要提前计算距离，这个参数会在空间和时间之间做权衡，如果是True 会把整个距离矩阵都放到内存中，auto 会默认在数据样本大于featurs*samples 的数量大于12e6 的时候False,False 时核心实现的方法是利用Cpython 来实现的+ verbose: 冗长模式（不太懂是啥意思，反正一般不去改默认值）+ random_state: 随机生成簇中心的状态条件。+ copy_x: 对是否修改数据的一个标记，如果True，即复制了就不会修改数据。bool 在scikit-learn 很多接口中都会有这个参数的，就是是否对输入数据继续copy 操作，以便不修改用户的输入数据。这个要理解Python 的内存机制才会比较清楚。+ n_jobs: 并行设置+ algorithm: kmeans的实现算法，有：‘auto’, ‘full’, ‘elkan’, 其中 'full’表示用EM方式实现


代码：

```python
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 18:52:21 2019

@author: 1
"""

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

df=pd.read_csv('D:\\workspace\\python\machine learning\\data\\iris.csv',sep=',')
data=df.iloc[:,0:3]
kmeans=KMeans(n_clusters=3)   #n_clusters:number of cluster
kmeans.fit(data)
labels=kmeans.labels_#聚类标签
centres=kmeans.cluster_centers_#聚类中心

#画三维聚类结果图
markers=['o','^','*']
colors=['r','b','y']
data['labels']=labels
ax = plt.subplot(111, projection='3d')  # 创建一个三维的绘图工程
data_new,X,Y,Z=[[]]*3,[[]]*3,[[]]*3,[[]]*3
for i in range(3):
    data_new[i]=data.loc[data['labels']==i]
    X[i],Y[i],Z[i]=data_new[i].iloc[:,0],data_new[i].iloc[:,1],data_new[i].iloc[:,2]
    ax.scatter(X[i],Y[i],Z[i],marker=markers[i],c=colors[i])
```


聚类结果： 
![./figures/20191120212523833.png](./figures/20191120212523833.png)


