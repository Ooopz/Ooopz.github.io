

**机器学习专栏**：[机器学习专栏](https://blog.csdn.net/weixin_43008804/category_9386844.html) 


### 模型评估


+ 
+ [一、回归指标](#_9)+ 
+ [1. 回归方差(反应自变量与因变量之间的相关程度)](#1__11)+ [2. 平均绝对误差](#2__17)+ [3. 均方差](#3__24)+ [4. 中值绝对误差](#4__30)+ [5. R平方值](#5_R_36)

+ [二、分类指标](#_42)+ 
+ [1. 精度](#1___43)+ [2. ROC曲线下的面积：较大的AUC代表了较好的performance](#2_ROCAUCperformance_48)+ [3. 根据预测得分计算平均精度(AP)](#3_AP_54)+ [4. 通过计算混淆矩阵来评估分类的准确性，返回混淆矩阵](#4__60)+ [5. F1值](#5_F1_65)+ [6. 对数损耗，又称逻辑损耗或交叉熵损耗](#6__81)+ [7. 计算ROC曲线下的面积就是AUC的值，the larger the better](#7_ROCAUCthe_larger_the_better_86)+ [8. ROC曲线](#8_ROC_92)







**导入方式**:sklearn.metrics



```python
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
```


## 一、回归指标


### 1. 回归方差(反应自变量与因变量之间的相关程度)


```python
explained_variance_score(y_true, y_pred, sample_weight=None, multioutput=‘uniform_average’)
```


### 2. 平均绝对误差


```python
mean_absolute_error(y_true,y_pred,sample_weight=None,multioutput=‘uniform_average’)
```


### 3. 均方差


```python
mean_squared_error(y_true,y_pred,sample_weight=None,multioutput=‘uniform_average’)
```


### 4. 中值绝对误差


```python
median_absolute_error(y_true, y_pred) 
```


### 5. R平方值


```python
r2_score(y_true,y_pred,sample_weight=None,multioutput=‘uniform_average’) 
```


## 二、分类指标


### 1. 精度


```python
accuracy_score(y_true,y_pre)
```


### 2. ROC曲线下的面积：较大的AUC代表了较好的performance


```python
auc(x, y, reorder=False)
```


### 3. 根据预测得分计算平均精度(AP)


```python
average_precision_score(y_true, y_score, average=‘macro’, sample_weight=None)
```


### 4. 通过计算混淆矩阵来评估分类的准确性，返回混淆矩阵


```python
confusion_matrix(y_true, y_pred, labels=None, sample_weight=None)
```


### 5. F1值


F1 = 2 * (precision * recall) / (precision + recall) precision(查准率)=TP/(TP+FP) recall(查全率)=TP/(TP+FN)

```python
precision_score(y_true, y_pred, labels=None, pos_label=1, average=‘binary’)
```


```python
recall_score(y_true, y_pred, labels=None, pos_label=1, average=‘binary’, sample_weight=None)
```


```python
f1_score(y_true, y_pred, labels=None, pos_label=1, average=‘binary’, sample_weight=None)
```


### 6. 对数损耗，又称逻辑损耗或交叉熵损耗


```python
log_loss(y_true, y_pred, eps=1e-15, normalize=True, sample_weight=None, labels=None)
```


### 7. 计算ROC曲线下的面积就是AUC的值，the larger the better


```python
roc_auc_score(y_true, y_score, average=‘macro’, sample_weight=None)
```


### 8. ROC曲线


ROC曲线越接近左上角，代表模型越好，即ACU接近1

```python
def plot_roc(labels, predict_prob):
    false_positive_rate, true_positive_rate, thresholds = roc_curve(labels, predict_prob)
    roc_auc = auc(false_positive_rate, true_positive_rate)
    plt.title('ROC')
    plt.plot(false_positive_rate, true_positive_rate,'b',label='AUC = %0.4f'% roc_auc)
    plt.legend(loc='lower right')
    plt.plot([0,1],[0,1],'r--')
    plt.ylabel('TPR')
    plt.xlabel('FPR')
    plt.show()
```


