# Adaboost 策略

## 1. 准备训练集

在日期截面上，准备好 *$N$ 行股票 × ($K$ 列因子值 + $1$ 列股票收益)* 的矩阵。

首先将因子归一化：具体的方法是*先将因子在因子截面排序，再将排序值除以序数最大值*。这样处理的原因是 Adaboost 模型并不关心因子的具体值的大小，而更关心因子值的顺序，而且此类模型*对输入值比较敏感*，不同因子的量纲也不尽一样，归一化让因子之间有了可比性。

然后按一定阈值（可以是正负 30%）将收益转换为正负例标签，*收益率在前 30% 的股票为正例*，标签值为 1，*收益率在后 30% 的股票为负例*，标签值为 -1，*其余的样本则被认为是噪声*而舍去。

需要搞清楚的点：
1.  为什么对输入值敏感?
2.  归一化的方式合理吗？有没有更好的方法呢？
3.  因子的排序方式（正序和逆序）对模型有什么影响?
4.  被舍去的标签真的是噪声吗？阈值应该怎么选?

## 2. 构建弱分类器

在训练集准备好之后，我们开始着手构建弱分类器。每个弱分类器都是基于一个因子构建出来的。

对于构建一个弱分类器：

首先将所有股票赋予相同权重 $w$，且 $\sum_{i=1}^{n} w_i=1$。

然后将因子切分为 $J$ 个 quantile（以 2 为例），计算每个 quantile 中正负例权重之和，其中第 $j$ 个 quantile 正例权重之和为 $W_+^j$，负例权重之和为 $W_-^j$。

我们使用评价函数 $Z=\sqrt{W_+^jW_-^j}$ ，来描述一个因子的一个 quantile 的分类效果，对于一个因子总体的评价使用函数 $Z=\sum_{j=1}^{J}{\sqrt{W_+^jW_-^j}}$ 。可以看出，当因子的分类效果较强时， $W_+^j$ 和 $W_-^j$ 差异较大，得到的 $Z$ 值较低，因此当一个因子的 $Z$ 值越小，说明因子对股票收益的分类越好。需要注意的是，因子对股票收益的分类表现并不等价于因子的盈利能力。

对所有因子计算出其 $Z$ 值，选取 $Z$ 值最小的因子做为第一个弱分类器。分类器是一个分段函数，每一段自变量取值范围即因子 quantile 的取值范围，其表达式如下，$\varepsilon$ 为较小值，用于防止分母为 0 的情况：

$$
h(x)=\frac{1}{2} \ln \left(\frac{W_{+}^{j}+\varepsilon}{W_{-}^{j}+\varepsilon}\right)
$$

当 $W_+^j>W_-^j$ 时，弱分类器的值为正，否则为负，也就是说当一个新样本值落入弱分类器的某一段中，弱分类器能够告诉你股票的预期收益为正（值大于 0，越大则越确信），或为负（值小于 0）。

## 3. 构建强因子

在第一个分类器构建完毕后，需要更新股票的权重，对于那些能正确分类的股票，我们降低其权重，反之则提高权重。这样，在之后的分类器中会更多的考虑那些被错误分类（或分类表现不好）的股票，而那些已经正确分类（或分类表现不错）的股票如果再次被准确分类也仅仅是锦上添花，对模型整体的表现提升不大。

对于新的权重，我们这样计算：

$$
w_i^{new} = w_i × e^{-y_i h(x_i)}
$$

其中 $y_i$ 为 股票的标签值，可以看出，当股票被正确分类后权重降低，错误分类后权重上升。

在重新计算完权重后，需要将权重除以权重之和，让新权重之和任然为 1。

之后，按照构建弱分类器的方法继续寻找下一个分类器。此时我们并不会将之前的选中的因子排除掉，因为在权重调整过后，之前打分较高的因子分数值会下降不太可能会在下一轮选中。当然，在很多轮选择过后，之前选中的因子有可能会被重新选中。

在足够多轮次的选择后（对于数量较小的因子来说，轮次数等于因子数，因子较多时，轮次会小于因子数），将所有的弱分类器简单加到一起就构建出了模型强因子。

## 4. 测试集

