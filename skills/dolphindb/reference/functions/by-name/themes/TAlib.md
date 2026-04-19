# TA-lib 系列

TA-lib（Technical Analysis
Library）是一个广泛用于金融市场数据分析的库，提供了一系列相关函数和工具。DolphinDB 提供了部分 TA-lib 功能函数，用于量化金融分析。

## TA-lib 系列函数介绍

TA-lib 系列函数对应的高阶函数 talib：

```
talib(func, args...)
```

该函数主要用于保持 DolphinDB 部分函数对数据前项空值的处理和 Python TA-lib 的处理方式保持一致。

内置的 TA-lib 系列函数的通用参数模板如下：

```
TA-libFunc(X, window)
```

* **X** 是一个向量/矩阵/表。
* **window** 是一个大于 1 的正整数，表示滑动窗口长度。

TAlib 系列提供了一个函数模板 ma,
可以通过该函数指定计算移动平均的类型，实现以下函数的功能：

* sma
* ema
* wma
* dema
* tema
* trima
* kama
* t3

指数移动平均（Exponential Moving Average）的拓展函数：

* wilder
* gema

滑动线性回归：linearTimeTrend

## 窗口确定规则

TA-lib 系列函数的 *window* 长度以元素个数衡量。

与 DolphinDB 其它窗口函数不同的是，TA-lib
系列函数会忽略元素开头的空值，并将这些空值保留到结果中，然后从第一个非空元素开始进行滑动窗口的计算。

当以元素个数衡量窗口时，根据滑动窗口的计算规则，只有当 *window* 内的元素填满窗口时，才开始第一次计算，即前
*window* - 1 个元素的计算结果默认为 NULL。

以下图为例，灰色部分为输出是空值的窗口。

其计算规则如下图：

![talib1](../../images/talib_1.png)

上图的对应代码，这里以 talib 应用在 msum
函数为例：

```
X = NULL NULL NULL 1 2 3 4 5 6 NULL 8 9
w = 3 // window

print msum(X, w)
// output
[ , , , 1, 3, 6, 9, 12, 15, 11, 14, 17]

talib(msum, X, w)
// output
[ , , , , , 6, 9, 12, 15, 11, 14, 17]
```

**相关信息**

* [技术分析（Technical Analysis）指标库](../../modules/ta/ta.html "技术分析（Technical Analysis）指标库")
