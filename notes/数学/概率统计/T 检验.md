# T 检验

## 0. 引子

t 检验（t test）又称学生 t 检验（Student t-test）可以说是统计推断中非常常见的一种检验方法，用于统计量服从正态分布，但方差未知的情况。

有关 t 检验的历史（以及学生 t 检验的由来）可以参考 [维基百科](https://en.wikipedia.org/wiki/Student%27s_t-test%23History) 。

t 检验的前提是要求样本服从正态分布或近似正态分布，不然可以利用一些变换（取对数、开根号、倒数等等）试图将其转化为服从正态分布是数据，如若还是不满足正态分布，只能利用非参数检验方法。不过*当样本量大于 30 的时候，可以认为数据近似正态分布*。

t 检验最常见的四个用途：

1.  单样本均值检验（One-sample t-test）

    用于检验 **总体方差未知、正态数据或近似正态的 单样本的均值 是否与 已知的总体均值相等**

2.  两独立样本均值检验（Independent two-sample t-test）

    用于检验 两**对独立的 正态数据或近似正态的 样本的均值 是否相等**，这里可根据总体方差是否相等分类讨论

3.  配对样本均值检验（Dependent t-test for paired samples）

    用于检验 **一对配对样本的均值的差 是否等于某一个值**

4.  回归系数的显著性检验（t-test for regression coefficient significance）

    用于检验 **回归模型的解释变量对被解释变量是否有显著影响**

## 1. 单样本均值检验

**目的：** 
检验单样本的均值是否和已知总体的均值相等。

**要求：**
1.  总体方差未知（否则就可以利用 $Z$ 检验，也叫 $U$ 检验，就是正态检验）
2.  正态数据或近似正态

**应用场景举例：**
1.  从某厂生产的零件中随机抽取若干件，检验其某种规格的均值是否与要求的规格相等（双侧检验）
2.  在某偏远地区随机抽取若干健康男子，检验其脉搏均数是否高于全体健康男子平均水平（单侧检验）
3.  检验某一线城市全体高三学生视力水平是否比全国全体高三学生视力水平低（单侧检验）

**检验原理：**
$H_{0}$ : 样本均值与总体均值相等
$H_{1}$ : 样本均值与总体均值不等

记总体均值为  $\mu$  ，总体方差为  $\sigma^{2}$(末知)，样本均值  $\bar{X}=\frac{1}{n} \sum_{i=1}^{n} X_{i}$  ，样本标准差 $s=\sqrt{\frac{1}{n-1} \sum_{i=1}^{n}\left(X_{i}-\bar{X}\right)^{2}}$  则有：

$$
\begin{aligned}
X_{i} \sim N\left(\mu, \sigma^{2}\right) & \rightarrow \bar{X}=\frac{1}{n} \sum_{i=1}^{n} X_{i} \sim N\left(\mu, \frac{\sigma^{2}}{n}\right) \\
& \rightarrow \frac{\bar{X}-\mu}{\frac{\sigma}{\sqrt{n}}}=\frac{\sqrt{n}(\bar{X}-\mu)}{\sigma} \sim N(0,1)
\end{aligned}
$$

对于熟悉数理统计的朋友，上面这一条是显然的。下面我们试着构造出一个 $t$ 统计量，我们知道 $t$ 统计量的构造定义是一个 **分子为标准正态变量、分母为卡方变量除以它自由度后开根号** 的分式。上面我们已经得到了一个标准正态变量，不难想到卡方变量的一个重要定理：

$$
\frac{(n-1) s^{2}}{\sigma^{2}} \sim \chi^{2}(n-1)
$$

因此，构造出的 $t$ 统计量应该如下：

$$
\frac{\frac{\sqrt{n}(\bar{X}-\mu)}{\sigma}}{\sqrt{\frac{\frac{(n-1) s^{2}}{\sigma^{2}}}{n-1}}}=\frac{\sqrt{n}(\bar{X}-\mu)}{s} \sim t(n-1)
$$

检验原理：

在  $H_{0}$  成立的条件下， $\bar{X}-\mu=0$  ，若上述统计量的值偏离 0 "太多"，是小概率事件，在一次 抽样中几乎不可能发生，其发生的概率即为  $p$  值。给定显著性水平 $\alpha$(如  0.05  )，根据研究的问 题确定是双侧检验 (two-side test) 还是单侧检验 (one-side test)，若为双侧检验，则查界值 表中自由度为  $n-1$  ，双侧  $\alpha$  ，得到临界值  $t_{\frac{\alpha}{2}, n-1}$  ；若为单侧检验，则查界值表中自由度为  $n-1$  ，单侧  $\alpha$  ，得到临界值  $t_{\alpha, n-1}$ 。

1.  对于要检验样本均值是否等于总体均值的双侧检验，若根据样本数据算出来的 $t$ 统计量的绝对值  $\left|\frac{\sqrt{n}(\bar{X}-\mu)}{s}\right|>t \frac{\alpha}{2, n-1}$  ，则拒绝原假设，认为样本均值与总体均值不等，否则不拒绝原假设。
2.  对于要检验样本均值是否比总体均值大的单侧检验，若根据样本数据算出来的 $t$ 统计量  $\frac{\sqrt{n}(\bar{X}-\mu)}{s}<t_{\alpha, n-1}$  ，则拒绝原假设，认为样本均值不大于总体均值，否则不拒绝原假设。
3.  对于要检验样本均值是否比总体均值小的单侧检验，若根据样本数据算出来的 $t$ 统计量  $\frac{\sqrt{n}(\bar{X}-\mu)}{s}>t_{\alpha, n-1}$ ，则拒绝原假设，认为样本均值不小于总体均值，否则不拒绝原假设。

##  2. 两独立样本均值检验

**目的：**
检验两独立样本的均值是否相等。

**要求：**
两样本独立，服从正态分布或近似正态。

**应用场景举例：**
1.  检验两工厂生产同种零件的规格是否相等（双侧检验）
2.  为研究某种治疗儿童贫血新药的疗效，以常规药作为对照，治疗一段时间后，检验施以新药的儿童血红蛋白的增加量是否比常规药的大（单侧检验）
3.  检验两种药物对治疗高血压的效果，检验两组药物的降压水平是否相等（双侧检验）

记两总体分别为  $X_{1} \sim N\left(\mu_{1}, \sigma_{1}^{2}\right)$, $X_{2} \sim N\left(\mu_{2}, \sigma_{2}^{2}\right)$  ，样本均值、样本标准差:

$$
\begin{array}{l}
\bar{X}_{1}=\frac{1}{n_{1}} \sum_{i=1}^{n_{1}} X_{1 i} , \quad \bar{X}_{2}=\frac{1}{n_{2}} \sum_{i=1}^{n_{2}} X_{2 i} \\
s_{1}=\sqrt{\frac{1}{n_{1}-1} \sum_{i=1}^{n_{1}}\left(X_{1 i}-\bar{X}_{1}\right)^{2}}, \quad s_{2}=\sqrt{\frac{1}{n_{2}-1} \sum_{i=1}^{n_{2}}\left(X_{2 i}-\bar{X}_{2}\right)^{2}}
\end{array}
$$

根据总体方差是否相等可以分为两类

### 2.1 情况1

**总体方差相等且未知，样本方差满足 $\frac{1}{2}<\frac{s_{1}^{2}}{s_{2}^{2}}<2$**

记总体方差为 $\sigma^{2}=\sigma_{1}^{2}=\sigma_{2}^{2}$

跟之前的思路类似，要检验两总体均值是否相等，先给出 样本均值的差 的分布，根据假设易得*式 A*：

$$
\begin{aligned}
& \bar{X}_{1}-\bar{X}_{2} \sim N\left(\mu_{1}-\mu_{2},\left(\frac{1}{n_{1}}+\frac{1}{n_{2}}\right) \sigma^{2}\right) \\
\rightarrow & \frac{\left(\bar{X}_{1}-\bar{X}_{2}\right)-\left(\mu_{1}-\mu_{2}\right)}{\sigma \sqrt{\frac{1}{n_{1}}+\frac{1}{n_{2}}}} \sim N(0,1) \quad(A)
\end{aligned}
$$

由卡方变量的重要定理：

$$\frac{\left(n_{1}-1\right) s_{1}^{2}}{\sigma^{2}} \sim \chi^{2}\left(n_{1}-1\right), \quad \frac{\left(n_{2}-1\right) s_{2}^{2}}{\sigma^{2}} \sim \chi^{2}\left(n_{2}-1\right)$$

由于两分布独立，则$S_{1}^{2}$，$S_{2}^{2}$独立，由卡方变量的可加性可得*式 B*：

$$\frac{\left(n_{1}-1\right) s_{1}^{2}}{\sigma^{2}}+\frac{\left(n_{2}-1\right) s_{2}^{2}}{\sigma^{2}} \sim \chi^{2}\left(n_{1}+n_{2}-2\right) \quad(B)$$

由$t$分布的构造定义，$(A) \div \sqrt{(B) /\left(n_{1}+n_{2}-2\right)}$，化简整理后可以得到：

$$\frac{\left(\bar{X}_{1}-\bar{X}_{2}\right)-\left(\mu_{1}-\mu_{2}\right)}{s_{p} \sqrt{\frac{1}{n_{1}}+\frac{1}{n_{2}}}} \sim t\left(n_{1}+n_{2}-2\right)$$

其中：

$$s_{p}=\sqrt{\frac{\left(n_{1}-1\right) s_{1}^{2}+\left(n_{2}-1\right) s_{2}^{2}}{n_{1}+n_{2}-2}}=\sqrt{\frac{\sum_{i=1}^{n_{1}}\left(X_{1 i}-\bar{X}_{1}\right)^{2}+\sum_{i=1}^{n_{2}}\left(X_{2 i}-\bar{X}_{2}\right)^{2}}{n_{1}+n_{2}-2}}$$

为两样本的**合并标准差**（pooled standard deviation），可以证明它的方差，即两样本的合并方差是总体方差 $\sigma^{2}$ 的无偏估计（unbiased estimator），证明见[[估计量的偏差与无偏估计]]。

同样地，在  $H_{0}$  成立的条件下，  $\mu_{1}-\mu_{2}=0$  。根据研究的问题确定是双侧检验 (two-side test）还是单侧检验 (one-side test)，若为双侧检验，则查 $t$ 界值表中自由度为  $n-1$  ，双侧  $\alpha$  ，得到临界值  $t_{\frac{\alpha}{2}, n-1}$  ；若为单侧检验，则查界值表中自由度为  $n-1$  ，双侧  $\alpha$  ，得到临界值  $t_{\alpha, n-1}$  。

**检验原理**

1. 对于要检验两总体均值是否相等的双侧检验，若根据样本数据算出来的  $t$  统计量的绝对值  $\left|\frac{\bar{X}_{1}-\bar{X}_{2}}{s_{p} \sqrt{\frac{1}{n_{1}}+\frac{1}{n_{2}}}}\right|>t \frac{\alpha}{2}, n-1$  ，则拒绝原假设，认为样本均值与总体均值不等，否则不拒绝原假设。
2. 对于要检验总体均值  $\bar{X}_{1}>\bar{X}_{2}$  单侧检验，若根据样本数据算出来的  $t$  统计量  $\left|\frac{\bar{X}_{1}-\bar{X}_{2}}{s_{p} \sqrt{\frac{1}{n_{1}}+\frac{1}{n_{2}}}}\right|>t_{\alpha, n-1}$  ，否则不拒绝原假设
3. 对于要检验总体均值  $\bar{X}_{1}<\bar{X}_{2}$  单侧检验，若根据样本数据算出来的  $t$  统计量  $\left|\frac{\bar{X}_{1}-\bar{X}_{2}}{s_{p} \sqrt{\frac{1}{n_{1}}+\frac{1}{n_{2}}}}\right|>t_{\alpha, n-1}$  ，否则不拒绝原假设。

### 2.2 情况2

**总体方差不等且未知（或者对它们一无所知），满足$s_{1}^{2}>2 s_{2}^{2}$ 或 $s_{2}^{2}>2 s_{1}^{2}$**

在这种情况（来自正态总体的两独立样本，无法假定它们方差相等）下，如何进行区间估计和假设检验的这个问题是由[Walter Behrens](https://link.zhihu.com/?target=https%3A//en.wikipedia.org/wiki/Walter_Behrens_%28statistician%29) and [Ronald Fisher](https://link.zhihu.com/?target=https%3A//en.wikipedia.org/wiki/Ronald_Fisher)提出来的，故称为[Behrens–Fisher problem](https://link.zhihu.com/?target=https%3A//en.wikipedia.org/wiki/Behrens%25E2%2580%2593Fisher_problem)。对于这个问题的研究，Behrens和Fisher给出了他们的估计[Behrens_and_Fisher_approach](https://link.zhihu.com/?target=https%3A//en.wikipedia.org/wiki/Behrens%25E2%2580%2593Fisher_problem%23Behrens_and_Fisher_approach)，而现在最常用的是[Welch's_approximate_t_solution](https://link.zhihu.com/?target=https%3A//en.wikipedia.org/wiki/Behrens%25E2%2580%2593Fisher_problem%23Welch%27s_approximate_t_solution)，它是[Satterthwaite_equation](https://link.zhihu.com/?target=https%3A//en.wikipedia.org/wiki/Welch%25E2%2580%2593Satterthwaite_equation)的解。

回到我们的问题。这里要引入Welch's t test，又名Welch's unequal variances _t_-test、unequal variances _t_-test（不等方差 $t$ 检验)

在总体方差不等的情况下，[2.1](数学/概率统计/T%20检验#2%201%20总体方差相等且未知，样本方差满足%20frac%201%202%20frac%20s_%201%202%20s_%202%202%202)中 $t$ 统计量的分母已不是总体方差的无偏估计，已不再适用，需重新构造一个 $t$ 统计量，这里需要利用**Satterthwaite近似法**。

取统计量：

$$t=\frac{\bar{X}_{1}-\bar{X}_{2}}{\sqrt{\frac{s_{1}^{2}}{n_{1}}+\frac{s_{2}^{2}}{n_{2}}}}
$$

它的自由度（df, degrees of freedom）：

$$\nu \approx \frac{\left(\frac{s_{1}^{2}}{n_{1}}+\frac{s_{2}^{2}}{n_{2}}\right)^{2}}{\frac{s_{1}^{4}}{n_{1}^{2} \nu_{1}}+\frac{s_{2}^{4}}{n_{2}^{2} \nu_{2}}}
$$

其中  $\nu_{1}=n_{1}-1, \nu_{2}=n_{2}-1$  分别是 $X_{1}$, $X_{2}$  的自由度，当 $n_{1}$, $n_{2}>5$  时，近似  $t$  分布 的效果比较好。

同样地，根据研究的问题确定是双侧检验 (two-side test) 还是单侧检验 (one-side test)，若 为双侧检验，则查  $t$  界值表中自由度为  $\nu$  ，双侧  $\alpha$  ，得到临界值  $t_{\frac{\alpha}{2}, \nu}$  ；若为单侧检验，则查界 值表中自由度为  $\nu$  ，单侧  $\alpha$  ，得到临界值  $t_{\alpha, \nu}$  。

**检验原理同2.1**


## 3.配对样本均值检验

这种情况常常出现在生物医学研究中，常见的情形有：

1.  配对的受试对象分别接受不同的处理（如将小白鼠配对为两组，分别接受不同的处理，检验处理结果的差异）
2.  同一受试对象的两个部分接受不同的处理（如对于一批血清样本，将其分为两个部分，利用不同的方法接受某种化合物的检验，检验结果的差异）
3.  同一受试对象的自身前后对照（如检验癌症患者术前、术后的某种指标的差异）

**要求：**
1.  总体方差相等
2.  正态数据或近似正态

既然是配对设计，不妨设 $n=n_{1}=n_{2}$  ；方差相等，有  $\sigma^{2}=\sigma_{1}^{2}=\sigma_{2}^{2}$  。取要检验的指标的差值  $d_{i}=X_{1 i}-X_{2 i}$  ，计算  $d_{i}$  的样本标准差  $s_{d}=\sqrt{\frac{1}{n-1} \sum_{i=1}^{n}\left(d_{i}-\bar{d}\right)^{2}}$  。要检验配对样本均数的差是否为0，即检验 $d_{i}$  的均值是否为0，这样就转化为了“1.单样本t检验”，由于正态性和方差相等的假定，差值的均值（以大写字母表示随机变量，小写字母表示样本取值）：

$$\bar{D}=\bar{X}_{1}-\bar{X}_{2} \sim N\left(\mu_{1}-\mu_{2}, \frac{2 \sigma^{2}}{n}\right) $$

从而得出*式 C*：

$$\frac{\bar{D}-\left(\mu_{1}-\mu_{2}\right)}{\sigma \sqrt{\frac{2}{n}}} \sim N(0,1) \quad(C)$$

构造卡方变量得出*式 D*：

$$\frac{(n-1) s_{d}}{\frac{2 \sigma^{2}}{n}} \sim \chi^{2}(n-1) \quad(D)$$

$(C) \div \sqrt{(D) /(n-1)}$ 化简整理得到：

$$\frac{\sqrt{n}\left(\bar{D}-\left(\mu_{1}-\mu_{2}\right)\right)}{s_{d}} \sim t(n-1)$$


同样地，在  $H_{0}$  成立的条件下，  $\mu_{1}-\mu_{2}=0$  。根据研究的问题确定是双侧检验 (two-side test) 还是单侧检验 (one-side test) ，若为双侧检验，则查 $t$ 界值表中自由度为 $ n-1$  ，双侧  $\alpha$  ，得到临界值  $t_{\frac{\alpha}{2}, n-1}$  ；若为单侧检验，则查  $t$  界值表中自由度为  $n-1$  ，双侧  $\alpha$  ，得到临界值  $t_{\alpha, n-1}$  。

**检验原理：**
1. 对于要检验差值的均值是否为 0 的双侧检验，若根据样本数据算出来的  $t$  统计量的绝对值  $\left|\frac{\sqrt{n} \bar{D}}{s_{d}}\right|>t_{\frac{\alpha}{2}, n-1}$  ，则拒绝原假设，认为样本均值与总体均值不等，否则不拒绝原假设。
2. 对于要检验  $\mu_{1}>\mu_{2}$  的单侧检验，若根据样本数据算出来的  $t$$  ，则 拒绝原假设，认为  $\mu_{1} \leq \mu_{2}$  ，否则不拒绝原假设。
3. 对于要检验  $\mu_{1}<\mu_{2}$  的单侧检验，若根据样本数据算出来的  $t$  统计量  $\frac{\sqrt{n} \bar{D}}{s_{d}}>t_{\alpha, n-1}$  ，则 拒绝原假设，认为  $\mu_{1} \geq \mu_{2}$  ，否则不拒绝原假设。

**注意，第2条和第3条两种检验不要误用，否则可能会得到错误的结论，参考文献[1]例7.2.4就是一个典型的例子，在此例中，配对检验消除了每一对自身的差异，若直接利用两独立样本检验，则无法消除这个差异，得到错误的结论。**


## 4.回归系数的显著性检验

**目的：**
检验回归模型的回归系数是否等于给定的值，一般取为0，此时检验的意义是检验该回归系数对应的解释变量对被解释变量是否有显著影响（因为若接受取值为0的假设，则该解释变量的项对被解释变量没有作用了）。

将多元线性回归模型：

$$Y_{i}=\beta_{0}+\beta_{1} X_{1 i}+\beta_{2} X_{2 i}+\cdots+\beta_{p} X_{p i}+\varepsilon_{i}$$

写为矩阵形式：

$$\boldsymbol{y}=\boldsymbol{X} \boldsymbol{\beta}+\boldsymbol{\varepsilon} \quad \text { or } \quad \hat{\boldsymbol{y}}=\boldsymbol{X} \hat{\boldsymbol{\beta}}$$

其中：

$$
\begin{array}{l}
\boldsymbol{y}=\left(\begin{array}{c}
y_{1} \\
y_{2} \\
\vdots \\
y_{n}
\end{array}\right)_{n \times 1} \quad \boldsymbol{X}=\left(\begin{array}{ccccc}
1 & x_{11} & x_{12} & \cdots & x_{1 p} \\
1 & x_{21} & x_{22} & \cdots & x_{2 p} \\
\vdots & \vdots & \vdots & & \vdots \\
1 & x_{n 1} & x_{n 2} & \cdots & x_{n p}
\end{array}\right)_{n \times(p+1)} \\
\boldsymbol{\beta}=\left(\begin{array}{c}
\beta_{0} \\
\beta_{1} \\
\vdots \\
\beta_{p}
\end{array}\right)_{(p+1) \times 1} \quad, \quad \boldsymbol{\varepsilon}=\left(\begin{array}{c}
\varepsilon_{1} \\
\varepsilon_{2} \\
\vdots \\
\varepsilon_{n}
\end{array}\right)_{n \times 1} \sim \boldsymbol{N}\left(\mathbf{0}, \sigma^{2} \boldsymbol{I}_{n}\right)
\end{array}
$$


其中  $\boldsymbol{I}_{n}$  为  $n$  阶单位方阵。方程满足  $\boldsymbol{X}$  满秩、Gauss-Markov条件、随机误差项服从正态分布等假定。

可以证明（见**附录2.1**）：

$$
\begin{array}{l}
\hat{\boldsymbol{\beta}}=\left(\boldsymbol{X}^{T} \boldsymbol{X}\right)^{-1} \boldsymbol{X}^{T} \boldsymbol{y} \quad(E)\\
E(\hat{\boldsymbol{\beta}})=\boldsymbol{\beta} \quad(F) \\
D(\hat{\boldsymbol{\beta}})=\sigma^{2}\left(\boldsymbol{X}^{T} \boldsymbol{X}\right)^{-1} \quad(G)
\end{array} 
$$

其中  $D(\hat{\boldsymbol{\beta}})$  表示  $\hat{\boldsymbol{\beta}}$  的方差-协方差矩阵。在  $\boldsymbol{\varepsilon}$  服从正态分布的假定下，由于  $\boldsymbol{\beta}$  是常向量 (回归模 型背后蒀含的末知的规律 )，给定一组 $\boldsymbol{X}$ （ $\boldsymbol{X}$  可以看成变量，但不是随机变量，因为  $\boldsymbol{X}$  的取值 是人为给定的)，从而  $\boldsymbol{\beta} \boldsymbol{X}$  是常向量，从而  $\boldsymbol{y}=\boldsymbol{\beta} \boldsymbol{X}+\boldsymbol{\varepsilon} \sim \boldsymbol{N}\left(\boldsymbol{\beta} \boldsymbol{X}, \sigma^{2} \boldsymbol{I}_{n}\right)$  是正态变量。 由$(E)$，  $\hat{\boldsymbol{\beta}}$  是  $\boldsymbol{y}$  的线性函数，从而  $\hat{\boldsymbol{\beta}}$  也是正态变量，再由 $(F)$、$(G)$:

$$\hat{\boldsymbol{\beta}} \sim \boldsymbol{N}\left(\boldsymbol{\beta}, \sigma^{2}\left(\boldsymbol{X}^{T} \boldsymbol{X}\right)^{-1}\right)$$

令 $\left(\boldsymbol{X}^{T} \boldsymbol{X}\right)^{-1}=\left(c_{i j}\right), \quad i, j=1,2, \cdots, p+1$ ，从而：

$$\hat{\beta}_{j-1} \sim N\left(\beta_{j-1}, \sigma^{2} c_{j-1, j-1}\right) \rightarrow \frac{\hat{\beta}_{j-1}-\beta_{j-1}}{\sigma \sqrt{c_{j-1, j-1}}} \sim N(0,1) \quad(H)$$

这样我们找到了一个**标准正态变量**，为了构造一个 $t$ 统计量，接着就是要寻找一个**与之独立的卡方变量**，这一步是最难的，我们在这里直接给出来，$(I)$ 的证明见**附录2.3**。两者独立的证明见**附录2.4**。

$$\frac{\hat{\sigma}^{2}(n-p-1)}{\sigma^{2}} \sim \chi^{2}(n-p-1) \quad(I)$$

其中  $\hat{\sigma}^{2}=\frac{S S E}{n-p-1}=\frac{\sum_{i=1}^{n} e_{i}^{2}}{n-p-1}$ 是 $\sigma^{2}$ 的无偏估计（证明见**附录2.2**）。

根据  $t$  分布的构造定义，由  $(H) / \sqrt{(I) /(n-p-1)}$  得:

$$\frac{\hat{\beta}_{j-1}-\beta_{j-1}}{\hat{\sigma} \sqrt{c_{j-1, j-1}}} \sim t(n-p-1) \quad j=1,2, \ldots, p+1$$



一般要检验解释变量  $X_{j}$  对被解释变量  $Y$  是否有显著影响，也即检验回归系数 $\hat{\beta}_{j-1}$  是否显著不 为 0 ，在这种情况下取  $\beta_{j-1}=0$  。而在一般情况下，要检验回归系数  $\hat{\beta}_{j-1}$  是否等于给定的  $\beta_{j-1}$  就有:

$$
\begin{array}{l}
H_{0}: \hat{\beta}_{j-1} \text { 等于 } \beta_{j-1} \\
H_{1}: \hat{\beta}_{j-1} \text { 不等于 } \beta_{j-1}
\end{array}
$$

取显著性水平  $\alpha$  ，查得自由度为 $n-p-1$  的双侧  $\alpha$  的  t  界值  $t_{\frac{\alpha}{2}, n-p-1}$  。若计算出来的  $t$  统计 量的绝对值  $\left|\frac{\hat{\beta}_{j-1}-\beta_{j-1}}{\hat{\sigma} \sqrt{c_{j j}}}\right|>t_{\frac{\alpha}{2}, n-p-1}$  ，则拒绝原假设，认为  $\hat{\beta}_{j-1}$  不等于  $\beta_{j-1}$  ，否则不 拒绝原假设。绝大多数情况都是取  $\beta_{j-1}=0$  。

## 附录

**附录1 合并方差是总体方差的无偏估计 的证明**

“加一项减一项”是很多数理统计证明题的灵魂，这里就用到了这个技巧。对于$X_{1}$：

$$
\begin{aligned}
\sum_{i=1}^{n_{1}}\left(X_{1 i}-\bar{X}_{1}\right)^{2} &=\sum_{i=1}^{n_{1}}\left[\left(X_{1 i}-\mu_{1}\right)-\left(\bar{X}_{1}-\mu_{1}\right)\right]^{2} \\
&=\sum_{i=1}^{n_{1}}\left(X_{1 i}-\mu_{1}\right)^{2}-2\left(\bar{X}_{1}-\mu_{1}\right) \sum_{i=1}^{n_{1}}\left(X_{1 i}-\mu_{1}\right)+n_{1}\left(\bar{X}_{1}-\mu_{1}\right)^{2} \\
&=\sum_{i=1}^{n_{1}}\left(X_{1 i}-\mu_{1}\right)^{2}-n_{1}\left(\bar{X}_{1}-\mu_{1}\right)^{2}
\end{aligned}
$$

由于:

$$\mu_{1}=E\left(X_{1 i}\right)=E(\bar{X})$$

从而:

$$\begin{aligned}
E\left(\sum_{i=1}^{n_{1}}\left(X_{1 i}-\bar{X}_{1}\right)^{2}\right) &=E\left(\sum_{i=1}^{n_{1}}\left(X_{1 i}-\mu_{1}\right)^{2}-n_{1}\left(\bar{X}_{1}-\mu_{1}\right)^{2}\right) \\
&=\sum_{i=1}^{n_{1}} E\left(X_{1 i}-\mu_{1}\right)^{2}-n_{1} E\left(\bar{X}_{1}-\mu_{1}\right)^{2} \\
&=\sum_{i=1}^{n_{1}} E\left(X_{1 i}-E\left(X_{1 i}\right)\right)^{2}-n_{1} E\left(\bar{X}_{1}-E\left(\bar{X}_{1}\right)\right)^{2} \\
&=\sum_{i=1}^{n_{1}} \operatorname{Var}\left(X_{1 i}\right)-n_{1} \operatorname{Var}\left(\bar{X}_{1}\right) \\
&=n_{1} \sigma^{2}-n_{1} \frac{\sigma^{2}}{n_{1}} \\
&=\left(n_{1}-1\right) \sigma^{2}
\end{aligned}$$


同理，对于  $X_{2}$  :

$$E\left(\sum_{i=1}^{n_{2}}\left(X_{2 i}-\bar{X}_{2}\right)^{2}\right)=\left(n_{2}-1\right) \sigma^{2}$$

从而证明了是无偏估计:

$$\begin{aligned}
E\left(s_{p}^{2}\right) &=E\left(\frac{\sum_{i=1}^{n_{1}}\left(X_{1 i}-\bar{X}_{1}\right)^{2}+\sum_{i=1}^{n_{2}}\left(X_{2 i}-\bar{X}_{2}\right)^{2}}{n_{1}+n_{2}-2}\right) \\
&=\frac{\left(n_{1}+n_{2}-2\right) \sigma^{2}}{n_{1}+n_{2}-2} \\
&=\sigma^{2}
\end{aligned}$$

附录2.1 (15)-(17) 的证明
先证明(15)。这里介绍一个很方便的求 $\boldsymbol{\beta}$  的估计值的方法，不过要熟悉矩阵的运算，而且要首先给 出三个引理:

Lemma 1 向量求导法则

$$\mid \begin{array}{l}
\forall \boldsymbol{A} \in \mathbb{R}^{n \times p}, \boldsymbol{X} \in \mathbb{R}^{p} \text { ，有: } \\
\frac{\partial(\boldsymbol{A} \boldsymbol{X})}{\partial \boldsymbol{X}}=\boldsymbol{A}^{T}, \quad \frac{\partial\left(\boldsymbol{X}^{T} \boldsymbol{X}\right)}{\partial \boldsymbol{X}}=\mathbf{2} X
\end{array}$$

第一个等式右边一定要记得转置，第二个等式可以类比一元函数求导:  $\left(x^{2}\right)^{\prime}=2 x$

Lemma 2 复合向量函数求导法则

若 $\boldsymbol{Z}(\boldsymbol{Y})$ 是 $\boldsymbol{Y}$  的向量函数，  $\boldsymbol{Y}(\boldsymbol{X})$  是  $\boldsymbol{X}$  的向量函数，则:

$$\frac{\partial \boldsymbol{Z}}{\partial \boldsymbol{X}}=\frac{\partial \boldsymbol{Y}}{\partial \boldsymbol{X}} \cdot \frac{\partial \boldsymbol{Z}}{\partial \boldsymbol{Y}}$$

等式右边的求导顺序一定不能反。

Lemma 3

对于下式左边，由前两个引理，不妨将  $(\boldsymbol{A} \boldsymbol{X})^{T} \boldsymbol{A} \boldsymbol{X}$  视为Lemma2中的  $\boldsymbol{Z}(\boldsymbol{Y})$ ，$ \boldsymbol{A} \boldsymbol{X}$  视为  $\boldsymbol{Y}(\boldsymbol{X})$  ，易得:

$$
\begin{aligned}
\frac{\partial\left((\boldsymbol{A} \boldsymbol{X})^{T} \boldsymbol{A} \boldsymbol{X}\right)}{\partial \boldsymbol{X}} &=\frac{\partial(\boldsymbol{A} \boldsymbol{X})}{\partial \boldsymbol{X}} \frac{\partial\left((\boldsymbol{A} \boldsymbol{X})^{T} \boldsymbol{A} \boldsymbol{X}\right)}{\partial(\boldsymbol{A} \boldsymbol{X})} \\
&=\boldsymbol{A}^{T} \cdot 2 \boldsymbol{A} \boldsymbol{X} \\
&=2 \boldsymbol{A}^{T} \boldsymbol{A} \boldsymbol{X}
\end{aligned}
$$



接者我们定义残差  $e_{i}=y_{i}-\hat{y}_{i}$  ，从而残差向量:

$$
\left(\begin{array}{c}
e_{1} \\
e_{2} \\
\vdots \\
e_{n}
\end{array}\right):=\boldsymbol{e}=\boldsymbol{y}-\hat{\boldsymbol{y}}=\boldsymbol{y}-\boldsymbol{X} \hat{\boldsymbol{\beta}}
$$



根据最小二乘估计 (Least Square Estimation, LSE)，要求 $\hat{\boldsymbol{\beta}}$  ，即求使得  $\sum_{i=1}^{n} e_{i}^{2}$  最小的  $\hat{\boldsymbol{\beta}}$  。


$$
\begin{aligned}
\sum_{i=1}^{n} e_{i}^{2} &=\left(e_{1}, e_{2}, \cdots, e_{n}\right) \cdot\left(\begin{array}{c}
e_{1} \\
e_{2} \\
\vdots \\
e_{n}
\end{array}\right) \\
&=\boldsymbol{e}^{T} \boldsymbol{e} \\
&=(\boldsymbol{y}-\boldsymbol{X} \hat{\boldsymbol{\beta}})^{T}(\boldsymbol{y}-\boldsymbol{X} \hat{\boldsymbol{\beta}})
\end{aligned}
$$

根据Lemma 3 的结论:

$$\begin{aligned}
\frac{\partial\left(\sum_{i=1}^{n} e_{i}^{2}\right)}{\partial \hat{\boldsymbol{\beta}}} &=\frac{\partial\left((\boldsymbol{y}-\boldsymbol{X} \hat{\boldsymbol{\beta}})^{T}(\boldsymbol{y}-\boldsymbol{X} \hat{\boldsymbol{\beta}})\right)}{\partial \hat{\boldsymbol{\beta}}} \\
&=-2 \boldsymbol{X}^{T}(\boldsymbol{y}-\boldsymbol{X} \boldsymbol{\beta})
\end{aligned}$$

令上式等于 0 ，得到:

$$\begin{aligned}
-2 \boldsymbol{X}^{T}(\boldsymbol{y}-\boldsymbol{X} \boldsymbol{\beta}) &=0 \\
\rightarrow \boldsymbol{X}^{T} \boldsymbol{y} &=\boldsymbol{X}^{T} \boldsymbol{X} \boldsymbol{\beta} \\
\rightarrow \hat{\boldsymbol{\beta}} &=\left(\boldsymbol{X}^{T} \boldsymbol{X}\right)^{-1} \boldsymbol{X}^{T} \boldsymbol{y} \quad\left(\text { 两边同乘 }\left(\boldsymbol{X}^{T} \boldsymbol{X}\right)^{-1}\right)
\end{aligned}$$

接着证明(16):

$$\begin{aligned}
E(\hat{\boldsymbol{\beta}}) &=E\left[\left(\boldsymbol{X}^{T} \boldsymbol{X}\right)^{-1} \boldsymbol{X}^{T} \boldsymbol{y}\right] \\
&=\left(\boldsymbol{X}^{T} \boldsymbol{X}\right)^{-1} \boldsymbol{X}^{T} \boldsymbol{E}(y) \\
&=\left(\boldsymbol{X}^{T} \boldsymbol{X}\right)^{-1} \boldsymbol{X}^{T} \boldsymbol{X} \boldsymbol{\beta} \\
&=\boldsymbol{\beta}
\end{aligned}$$


Lemma 4

$$\begin{array}{l}
\text { 若 } \operatorname{Var}(\boldsymbol{y})=\sigma^{2} \boldsymbol{I}_{n}, \boldsymbol{c}=\left(\begin{array}{c}
c_{1} \\
c_{2} \\
\vdots \\
c_{n}
\end{array}\right) \\
\operatorname{Var}\left(\boldsymbol{c}^{T} \boldsymbol{y}\right)=\boldsymbol{c}^{T} \boldsymbol{I}_{n} \boldsymbol{c} \cdot \operatorname{Var}(\boldsymbol{y})=\sigma^{2} \boldsymbol{c}^{T} \boldsymbol{c}^{n} ， \text { 则: } \\
\text { 若 } \boldsymbol{c}_{1}, \boldsymbol{c}_{2} \in \mathbb{R}^{n} ， \text { 则: } \\
\operatorname{Cov}\left(\boldsymbol{c}_{1}^{T} \boldsymbol{y}, \boldsymbol{c}_{2}^{T} \boldsymbol{y}\right)=\boldsymbol{c}_{1}^{T} \boldsymbol{I}_{n} \boldsymbol{c}_{2} \cdot \operatorname{Var}(\boldsymbol{y})=\sigma^{2} \boldsymbol{c}_{1}^{T} \boldsymbol{c}_{2}
\end{array}$$

利用该引理:

$$ \begin{aligned} D(\hat{\boldsymbol{\beta}}) &=\operatorname{Cov}(\hat{\boldsymbol{\beta}}, \hat{\boldsymbol{\beta}}) \\ &=\operatorname{Cov}\left[\left(\boldsymbol{X}^{T} \boldsymbol{X}\right)^{-1} \boldsymbol{X}^{T} \boldsymbol{y},\left(\boldsymbol{X}^{T} \boldsymbol{X}\right)^{-1} \boldsymbol{X}^{T} \boldsymbol{y}\right] \\ &=\left(\boldsymbol{X}^{T} \boldsymbol{X}\right)^{-1} \boldsymbol{X}^{T} \cdot \sigma^{2} \boldsymbol{I}_{n} \cdot\left[\left(\boldsymbol{X}^{T} \boldsymbol{X}\right)^{-1} \boldsymbol{X}^{T}\right]^{T} \\ &=\sigma^{2} \cdot\left(\boldsymbol{X}^{T} \boldsymbol{X}\right)^{-1} \boldsymbol{X}^{T} \boldsymbol{X}\left(\boldsymbol{X}^{T} \boldsymbol{X}\right)^{-1} \\ &=\sigma^{2}\left(\boldsymbol{X}^{T} \boldsymbol{X}\right)^{-1} \\ 
 \end{aligned} $$
附录2.2  $\hat{\sigma}^{2} = \frac{\sum_{i=1}^{n} e_{i}^{2}}{n-p-1}$ 是 $\sigma^{2}$ 的无偏估计的证明

这里要对于矩阵取方差-协方差的运算给出引理:

Lemma 5

设  $\boldsymbol{A} \in \mathbb{R}^{m \times n}$  为常矩阵， $\boldsymbol{y} \in \mathbb{R}^{n \times 1}$  为随机向量，则  $\boldsymbol{A} \boldsymbol{y}$  的方差-协方差矩阵:

$$D(\boldsymbol{A} \boldsymbol{y})=\boldsymbol{A} D(\boldsymbol{y}) \boldsymbol{A}^{T}$$

在附录2.1中我们得到了 $\hat{\boldsymbol{\beta}}=\left(\boldsymbol{X}^{T} \boldsymbol{X}\right)^{-1} \boldsymbol{X}^{T} \boldsymbol{y}$ , 从而:

$$\begin{aligned}
\boldsymbol{e} &=\boldsymbol{y}-\hat{\boldsymbol{y}} \\
&=\boldsymbol{y}-\boldsymbol{X} \hat{\boldsymbol{\beta}} \\
&=\boldsymbol{y}-\boldsymbol{X}\left(\boldsymbol{X}^{T} \boldsymbol{X}\right)^{-1} \boldsymbol{X}^{T} \boldsymbol{y} \\
&=\left(\boldsymbol{I}-\boldsymbol{X}\left(\boldsymbol{X}^{T} \boldsymbol{X}\right)^{-1} \boldsymbol{X}^{T}\right) \boldsymbol{y} \\
&=(\boldsymbol{I}-\boldsymbol{H}) \boldsymbol{y} \quad\left(\operatorname{Let} \boldsymbol{H}=\boldsymbol{X}\left(\boldsymbol{X}^{T} \boldsymbol{X}\right)^{-1} \boldsymbol{X}^{T}\right)
\end{aligned}$$


上式中的  $H=\boldsymbol{X}\left(\boldsymbol{X}^{T} \boldsymbol{X}\right)^{-1} \boldsymbol{X}^{T}$  称为帽子矩阵，因为它作用在  $\boldsymbol{y}$  上就得到了  $\hat{\boldsymbol{y}}$  ，就像给  $\boldsymbol{y}$  戴 了一顶帽子。  $\boldsymbol{I}$  的简写。现在证明两个很重要的结论:
1.  $\boldsymbol{I}-\boldsymbol{H}$  为对称阵

$$\begin{aligned}
(\boldsymbol{I}-\boldsymbol{H})^{T} &=\left(\boldsymbol{I}-\boldsymbol{X}\left(\boldsymbol{X}^{T} \boldsymbol{X}\right)^{-1} \boldsymbol{X}^{T}\right)^{T} \\
&=\boldsymbol{I}^{T}-\left(\boldsymbol{X}\left(\boldsymbol{X}^{T} \boldsymbol{X}\right)^{-1} \boldsymbol{X}^{T}\right)^{T} \\
&=\boldsymbol{I}-\left(\boldsymbol{X}^{T}\right)^{T} \cdot\left(\boldsymbol{X}^{T} \boldsymbol{X}\right)^{-1} \cdot \boldsymbol{X}^{T} \\
&=\boldsymbol{I}-\boldsymbol{X}\left(\boldsymbol{X}^{T} \boldsymbol{X}\right)^{-1} \boldsymbol{X}^{T} \\
&=\boldsymbol{I}-\boldsymbol{H}
\end{aligned}$$

2.  $\boldsymbol{I}-\boldsymbol{H}$  为幕等阵

$$\begin{aligned}
(\boldsymbol{I}-\boldsymbol{H}) \cdot(\boldsymbol{I}-\boldsymbol{H})=&\left(\boldsymbol{I}-\boldsymbol{X}\left(\boldsymbol{X}^{T} \boldsymbol{X}\right)^{-1} \boldsymbol{X}^{T}\right) \cdot\left(\boldsymbol{I}-\boldsymbol{X}\left(\boldsymbol{X}^{T} \boldsymbol{X}\right)^{-1} \boldsymbol{X}^{T}\right) \\
=& \boldsymbol{I}-2 \boldsymbol{X}\left(\boldsymbol{X}^{T} \boldsymbol{X}\right)^{-1} \boldsymbol{X}^{T} \\
&+\left(\boldsymbol{X}\left(\boldsymbol{X}^{T} \boldsymbol{X}\right)^{-1} \boldsymbol{X}^{T}\right) \cdot\left(\boldsymbol{X}\left(\boldsymbol{X}^{T} \boldsymbol{X}\right)^{-1} \boldsymbol{X}^{T}\right) \\
=& \boldsymbol{I}-2 \boldsymbol{X}\left(\boldsymbol{X}^{T} \boldsymbol{X}\right)^{-1} \boldsymbol{X}^{T}+\boldsymbol{X}\left(\boldsymbol{X}^{T} \boldsymbol{X}\right)^{-1} \boldsymbol{X}^{T} \\
=& \boldsymbol{I}-\boldsymbol{X}\left(\boldsymbol{X}^{T} \boldsymbol{X}\right)^{-1} \boldsymbol{X}^{T} \\
=& \boldsymbol{I}-\boldsymbol{H}
\end{aligned}$$


稍安勿躁，现在求  $\boldsymbol{e}$  的期望:

$$\begin{aligned}
E(\boldsymbol{e}) &=E(\boldsymbol{y}-\boldsymbol{X} \hat{\boldsymbol{\beta}}) \\
&=\boldsymbol{y}-\boldsymbol{X} E(\hat{\boldsymbol{\beta}}) \\
&=\boldsymbol{y}-\boldsymbol{X} \boldsymbol{\beta} \\
&=\mathbf{0}
\end{aligned}$$

从而  $$E\left(e_{i}\right)=0, \quad i=1,2, \cdots, n$$ 
再求  $e$  的方差-协方差矩阵，由Lemma 4:

$$\begin{aligned}
D(\boldsymbol{e}) &=D((\boldsymbol{I}-\boldsymbol{H}) \boldsymbol{y}) \\
&=(\boldsymbol{I}-\boldsymbol{H}) \cdot D(\boldsymbol{y}) \cdot(\boldsymbol{I}-\boldsymbol{H})^{T}
\end{aligned}$$

在正文中已证明了  $D(\boldsymbol{y})=\sigma^{2} \boldsymbol{I}$  ，从而

$$\begin{aligned}
D(\boldsymbol{e}) &=(\boldsymbol{I}-\boldsymbol{H}) D(\boldsymbol{y})(\boldsymbol{I}-\boldsymbol{H})^{T} \\
&=(\boldsymbol{I}-\boldsymbol{H}) \cdot \sigma^{2} \boldsymbol{I} \cdot(\boldsymbol{I}-\boldsymbol{H})^{T} \\
&=\sigma^{2} \boldsymbol{I} \cdot(\boldsymbol{I}-\boldsymbol{H}) \cdot(\boldsymbol{I}-\boldsymbol{H})^{T} \\
&=\sigma^{2}(\boldsymbol{I}-\boldsymbol{H}) \cdot(\boldsymbol{I}-\boldsymbol{H}) \\
&=\sigma^{2}(\boldsymbol{I}-\boldsymbol{H}) \\
\end{aligned}$$
记 $\boldsymbol{H}=\left(h_{i j}\right), \quad i, j=1,2, \cdots, n$ 。从而

$$\operatorname{Var}\left(e_{i}\right)=\sigma^{2}\left(1-h_{i i}\right), \quad i=1,2, \cdots, n$$


现在来看一下 $\boldsymbol{H}$  的迹，也即对角线元素之和，需要用到性质：  $\operatorname{tr}(\boldsymbol{A B})=\operatorname{tr}(\boldsymbol{B A})$  ：

$$\begin{aligned}
\sum_{i=1}^{n} h_{i i} &=\operatorname{tr}(\boldsymbol{H}) \\
&=\operatorname{tr}\left(\boldsymbol{X}\left(\boldsymbol{X}^{T} \boldsymbol{X}\right)^{-1} \boldsymbol{X}^{T}\right) \\
&=\operatorname{tr}\left(\left(\boldsymbol{X}^{T} \boldsymbol{X}\right)^{-1} \boldsymbol{X}^{T} \boldsymbol{X}\right) \\
&=\operatorname{tr}\left(\boldsymbol{I}_{p+1}\right) \\
&=p+1
\end{aligned}$$
现在就可以回到原来的问题，证明 $\hat{\sigma}^{2}=\frac{\sum_{i=1}^{n} e_{i}^{2}}{n-p-1}$  是  $\sigma^{2}$  的无偏估计:

$$
\begin{aligned}
E\left(\frac{\sum_{i=1}^{n} e_{i}^{2}}{n-p-1}\right) &=\frac{1}{n-p-1} \sum_{i=1}^{n} E\left(e_{i}^{2}\right) \\
&=\frac{1}{n-p-1} \sum_{i=1}^{n}\left[E\left(e_{i}^{2}\right)-0\right] \\
&=\frac{1}{n-p-1} \sum_{i=1}^{n}\left[E\left(e_{i}^{2}\right)-E\left(e_{i}\right)\right] \\
&=\frac{1}{n-p-1} \sum_{i=1}^{n} \operatorname{Var}\left(e_{i}\right) \\
&=\frac{1}{n-p-1} \sum_{i=1}^{n} \sigma^{2}\left(1-h_{i i}\right) \\
&=\frac{\sigma^{2}}{n-p-1}\left(n-\sum_{i=1}^{n} h_{i i}\right) \\
&=\frac{\sigma^{2}}{n-p-1}(n-p-1) \\
&=\sigma^{2}
\end{aligned}
$$



附录2.3 证明  $\frac{\hat{\sigma}^{2}(n-p-1)}{\sigma^{2}} \sim \chi^{2}(n-p-1)$
首先，记 $\boldsymbol{y}^{*}=\boldsymbol{y}-\boldsymbol{X} \boldsymbol{\beta} \sim \boldsymbol{N}\left(\mathbf{0}, \sigma^{2} \boldsymbol{I}\right)$  ，利用 "$\boldsymbol{H} \boldsymbol{X}=\boldsymbol{X}\left(\boldsymbol{X}^{T} \boldsymbol{X}\right)^{-1} \boldsymbol{X}^{T} \boldsymbol{X}=\boldsymbol{X}$" 的性质得到:

$$\begin{aligned}
\boldsymbol{e} &=\boldsymbol{y}-\hat{\boldsymbol{y}} \\
&=(\boldsymbol{y}-\boldsymbol{X} \boldsymbol{\beta})-(\hat{\boldsymbol{y}}-\boldsymbol{X} \boldsymbol{\beta}) \\
&=\boldsymbol{y}^{*}-(\boldsymbol{H} \boldsymbol{y}-\boldsymbol{H} \boldsymbol{X} \boldsymbol{\beta}) \\
&=\boldsymbol{y}^{*}-\boldsymbol{H}(\boldsymbol{y}-\boldsymbol{X} \boldsymbol{\beta}) \\
&=\boldsymbol{y}^{*}-\boldsymbol{H} \boldsymbol{y}^{*} \\
&=(\boldsymbol{I}-\boldsymbol{H}) \boldsymbol{y}^{*}
\end{aligned}$$



从而:

$$\begin{aligned}
\hat{\sigma}^{2}(n-p-1) &=\boldsymbol{e}^{T} \boldsymbol{e} \\
&=\left(y^{*}\right)^{T}(\boldsymbol{I}-\boldsymbol{H})^{T} \cdot(\boldsymbol{I}-\boldsymbol{H}) \boldsymbol{y}^{*} \\
&=\left(y^{*}\right)^{T}(\boldsymbol{I}-\boldsymbol{H}) \boldsymbol{y}^{*}
\end{aligned}$$


由于  $\boldsymbol{I}-\boldsymbol{H}$  为幂等阵，故存在一个对角矩阵

$$\begin{aligned}
\Lambda_{r} &=\operatorname{diag}(\underbrace{1,1, \cdots, 1}_{r 个 1}, \underbrace{0,0, \cdots, 0}_{n-r 个 0}) \\
&=\left(\begin{array}{ccccc}
1 & & & & \\
& \ddots & & & \\
& & 1 & & & \\
& & 0 & & \\
& & & \ddots & \\
& & & & 0
\end{array}\right)
\end{aligned}$$

和正交矩阵  $\boldsymbol{P}$  (满足 $\boldsymbol{P} \boldsymbol{P}^{T}=\boldsymbol{P}^{T} \boldsymbol{P}=\boldsymbol{I}$  )，使得:

$$\mid \boldsymbol{I}-\boldsymbol{H}=\boldsymbol{P}^{T} \boldsymbol{\Lambda}_{r} \boldsymbol{P}$$

由此关系重新考虑  $\boldsymbol{I}-\boldsymbol{H}$  的迹可以得到  $r$  的值:

$$ n-p-1=\operatorname{tr}(\boldsymbol{I}-\boldsymbol{H})=\operatorname{tr}\left(\boldsymbol{P}^{T} \boldsymbol{\Lambda}_{r} \boldsymbol{P}\right)=\operatorname{tr}\left(\boldsymbol{\Lambda}_{r} \boldsymbol{P} \boldsymbol{P}^{T}\right)=\operatorname{tr}\left(\boldsymbol{\Lambda}_{r}\right)=r$$

另一方面，令  $\boldsymbol{Z}=\boldsymbol{P} \boldsymbol{y}^{*}$  ，利用矩阵乘法以及期望的线性性质容易得到 (这也是多元统计分析里 的基本结论)：

$$E(\boldsymbol{Z})=E\left(\boldsymbol{P} \boldsymbol{y}^{*}\right)=\boldsymbol{P} E\left(\boldsymbol{y}^{*}\right)=\boldsymbol{P} \cdot \mathbf{0}=\mathbf{0}$$


再由**Lemma 4**：


$$\begin{aligned}
D(\boldsymbol{Z}) &=D\left(\boldsymbol{P} \boldsymbol{y}^{*}\right) \\
&=\boldsymbol{P} D\left(\boldsymbol{y}^{*}\right) \boldsymbol{P}^{T} \\
&=\boldsymbol{P} \cdot \sigma^{2} \boldsymbol{I} \cdot \boldsymbol{P}^{T} \\
&=\sigma^{2} \boldsymbol{I} \cdot \boldsymbol{P} \boldsymbol{P}^{T} \\
&=\sigma^{2} \boldsymbol{I}
\end{aligned}$$



由于  $\boldsymbol{Z}$  为正态变量  $\boldsymbol{y}^{*}$  的线性函数，故  $\boldsymbol{Z}$  也为正态变量，取它的每一个分量 $z_{i} \sim N\left(0, \sigma^{2}\right), \quad i=1,2, \cdots, n$  。从而:

$$\frac{z_{i}}{\sigma} \sim N(0,1) \rightarrow \frac{z_{i}^{2}}{\sigma^{2}} \sim \chi^{2}(1)$$

再回到对  $\sigma^{2}(n-p-1)$  的探究上:

$$ 
\begin{aligned}
\sigma^{2}(n-p-1)&=\left(y^{*}\right)^{T}(\boldsymbol{I}-\boldsymbol{H}) \boldsymbol{y}^{*}\\ 
 &=\left(y^{*}\right)^{T}\left(\boldsymbol{P}^{T} \boldsymbol{\Lambda}_{r} \boldsymbol{P}\right) \boldsymbol{y}^{*} \\
 &=\left(\boldsymbol{P} \boldsymbol{y}^{*}\right)^{T} \boldsymbol{\Lambda}_{r}\left(\boldsymbol{P} \boldsymbol{y}^{*}\right) \\
 &=\boldsymbol{Z}^{T} \boldsymbol{\Lambda}_{r} \boldsymbol{Z} \\
 &=\left(z_{1}, z_{2}, \cdots, z_{n}\right)\left(\begin{array}{cccccc}1 & & & & & \\ & \ddots & & & & \\ & & 1 & & & \\ & & & 0 & & \\ & & & & \ddots & \\ & & & & & 0\end{array}\right)\left(\begin{array}{c}z_{1} \\ z_{2} \\ \vdots \\ z_{n}\end{array}\right)\\ 
 &=\sum_{i=1}^{r} z_{i}^{2} 
 \end{aligned}$$

 最后利用卡方分布的可加性我们证明了结论:

$$\begin{aligned}
\frac{\hat{\sigma}^{2}(n-p-1)}{\sigma^{2}} &=\frac{\sum_{i=1}^{r} z_{i}^{2}}{\sigma^{2}} \\
&=\sum_{i=1}^{n-p-1} \frac{z_{i}^{2}}{\sigma^{2}} \quad(r=n-p-1) \\
& \sim \chi^{2}(n-p-1)
\end{aligned}$$

其实这里  $\Lambda_{r}$  的秩 $\operatorname{rank}\left(\Lambda_{r}\right)=r$  恰恰就是卡方变量的自由度，这也是自由度与矩阵的关系。
附录2.4 标准正态变量与卡方变量的独立性的证明
要证  $\hat{\beta}_{j}  与  \frac{\hat{\sigma}^{2}(n-p-1)}{\sigma^{2}}$  的独立性，由于  $\hat{\sigma}^{2}=\frac{\sum_{i=1}^{n} e_{i}^{2}}{n-p-1}$  ，我们来考察 $\hat{\boldsymbol{\beta}}$  与  $\boldsymbol{e}$  的关系， 为了计算它们的协方差，我们首先给出一个引理:

Lemma 5

$$\begin{array}{l}
\text { 若 } \operatorname{Var}(\boldsymbol{y})=\sigma^{2} \boldsymbol{I}_{n}, \boldsymbol{c}=\left(\begin{array}{c}
c_{1} \\
c_{2} \\
\vdots \\
c_{n}
\end{array}\right)_{n \times 1} \in \mathbb{R}^{n} \text { ，则： } \\
\operatorname{Var}\left(\boldsymbol{c}^{T} \boldsymbol{y}\right)=\boldsymbol{c}^{T} \boldsymbol{I}_{n} \boldsymbol{c} \cdot \operatorname{Var}(\boldsymbol{y})=\sigma^{2} \boldsymbol{c}^{T} \boldsymbol{c} \\
\text { 若 } \boldsymbol{c}_{1}, \boldsymbol{c}_{2} \in \mathbb{R}^{n}, \text { 则: } \\
\operatorname{Cov}\left(\boldsymbol{c}_{1}^{T} \boldsymbol{y}, \boldsymbol{c}_{2}^{T} \boldsymbol{y}\right)=\boldsymbol{c}_{1}^{T} \boldsymbol{I}_{n} \boldsymbol{c}_{2} \cdot \operatorname{Var}(\boldsymbol{y})=\sigma^{2} \boldsymbol{c}_{1}^{T} \boldsymbol{c}_{2}
\end{array}$$

根据Lemma 5:


$$\begin{aligned}
\operatorname{Cov}(\hat{\boldsymbol{\beta}}, \boldsymbol{e}) &=\operatorname{Cov}\left(\left(\boldsymbol{X}^{T} \boldsymbol{X}\right)^{-1} X^{T} \boldsymbol{y},(\boldsymbol{I}-\boldsymbol{H}) \boldsymbol{y}\right) \\
&=\sigma^{2} \cdot\left(\boldsymbol{X}^{T} \boldsymbol{X}\right)^{-1} \boldsymbol{X}^{T} \cdot(\boldsymbol{I}-\boldsymbol{H}) \\
&=\sigma^{2} \cdot\left(\boldsymbol{X}^{T} \boldsymbol{X}\right)^{-1} \boldsymbol{X}^{T} \cdot\left(\boldsymbol{I}-\boldsymbol{X}\left(\boldsymbol{X}^{T} \boldsymbol{X}\right)^{-1} \boldsymbol{X}^{T}\right) \\
&=\sigma^{2} \cdot\left(\left(\boldsymbol{X}^{T} \boldsymbol{X}\right)^{-1} \boldsymbol{X}^{T}-\left(\boldsymbol{X}^{T} \boldsymbol{X}\right)^{-1} \boldsymbol{X}^{T} \cdot \boldsymbol{X}\left(\boldsymbol{X}^{T} \boldsymbol{X}\right)^{-1} \boldsymbol{X}^{T}\right) \\
&=\sigma^{2} \cdot\left(\left(\boldsymbol{X}^{T} \boldsymbol{X}\right)^{-1} \boldsymbol{X}^{T}-\left(\boldsymbol{X}^{T} \boldsymbol{X}\right)^{-1} \boldsymbol{X}^{T}\right) \\
&=0
\end{aligned}$$

说明 $\hat{\boldsymbol{\beta}}$  与  $\boldsymbol{e}$  不相关。由于它们都是正态变量，两正态变量不相关等价于独立，且两独立变量的函 数变量也相互独立。而  $\hat{\sigma}^{2}=\frac{\sum e_{i}^{2}}{n-p-1}=\frac{\boldsymbol{e}^{T} \boldsymbol{e}}{n-p-1}$  是  $\boldsymbol{e}$  的函数。从而  $\hat{\boldsymbol{\beta}}$  与  $\hat{\sigma}^{2}$  独立，从 而标准正态分布与卡方变量独立。

自此，  $t$  检验的原理结束了。