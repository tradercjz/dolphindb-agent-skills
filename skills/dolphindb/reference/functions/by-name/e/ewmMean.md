# ewmMean

## 语法

`ewmMean(X, [com], [span], [halfLife], [alpha], [minPeriods=0], [adjust=true],
[ignoreNA=false], [times])`

## 详情

返回 *X* 的指数加权移动平均值。该函数必须指定 *com*, *span*,
*halfLife*, *alpha* 四个参数中的一个。

## 参数

**X** 是一个数值型向量、矩阵或表。若 *X* 是表，只对其内数值型和布尔型的列进行计算。

**com** 可选参数，是一个大于等于 0 的数值型标量，表示质心。根据质心指定平滑系数时，公式如下：

![](../../images/ewmmean_com.png)

**span** 可选参数，是一个大于等于 1 的数值型标量，表示跨度。根据跨度指定平滑系数时，公式如下：

![](../../images/ewmmean_span.png)

**halfLife** 可选参数，是一个大于 0 的数值型标量，表示半衰期。若为 DURATION 类型，需同时指定 *times*
参数，且两者单位需一致。根据半衰期指定平滑系数时，公式如下：

![](../../images/ewmmean_halflife.png)

**alpha** 可选参数，是一个 (0,1] 之间的浮点数，表示平滑系数。

**minPeriods** 可选参数，是一个整数，表示窗口中的最小观察数。默认值为 0。

**adjust** 可选参数，是一个布尔值，表示是否除以开始阶段的衰减调整因子。默认值为 true。

* 若 *adjust* 为 true，其公式为：

  ![](../../images/ewmmean_adjust_true.png)
* 若 *adjust* 为 false，其公式为：

  ![](../../images/ewmmean_adjust_false.png)

**ignoreNA** 可选参数，是一个布尔值，表示计算权重时是否忽略 NULL 值。默认值为 false，即不忽略 NULL 值。以
[x0, NULL, x2] 为例：

* 若 *ignoreNA* 为 true，
  + *adjust* 为 false，x0、x2 的最终权重为 1-α、α；
  + *adjust* 为 true，则 x0、x2 的最终权重为 1-α、1；
* 若 *ignoreNA* 为 false，
  + *adjust* 为 false，则
    x0、x2的最终权重为（1-α）2、α；
  + *adjust* 为 true,则 x0、x2
    的最终权重为（1-α）2、1。

**times** 可选参数，时间类型向量，需与 *X* 等长且严格递增。仅当 *halfLife* 为 DURATION 类型时必需，单位需与
*halfLife* 一致。

注意：若 *halfLife* 以 B（工作日）或交易日历为单位，则 *times* 必须为 DATE 类型向量。

## 返回值

DOUBLE 类型，数据形式同 *X*。

## 例子

使用以下的 a 作为 X 的值，

```
a=[0,1,2,int(),4];
ewmMean(X=a,com=0.5);
// output: [0,0.75,1.615385,1.615385,3.670213]

ewmMean(X=a,com=0.5,ignoreNA=true);
// output: [0,0.75,1.615385,1.615385,3.225]

ewmMean(a, halfLife = 4d, times=[2019.12.31, 2020.01.03, 2020.01.10, 2020.01.15, 2020.01.17])
// output: [0,0.627115,1.558466,1.558466,3.256043]

// halfLife 指定为交易日历
ewmMean(a, halfLife = 4XNYS, times=[2019.12.31, 2020.01.03, 2020.01.10, 2020.01.15, 2020.01.17])
// output: [0,0.585786,1.409080,1.409080,2.913483]

// halfLife 指定为工作日
ewmMean(a, halfLife = 4B, times=[2019.12.31, 2020.01.03, 2020.01.10, 2020.01.15, 2020.01.17])
// output: [0,0.627115,1.448981,1.448981,2.947520]
```

使用以下的 t1 作为 X 的值，

```
n = 20
colNames = `time`sym`qty`price
colTypes = [TIME,SYMBOL,INT,DOUBLE]
t1 = table(n:0, colNames, colTypes)
insert into t1 values(09:30:00.001,`AAPL,100,56.5)
insert into t1 values(09:30:00.001,`AAPL,200,30.5)
insert into t1 values(09:30:00.001,`DELL,150,35.5)
insert into t1 values(09:30:00.001,`DELL,170,60.5)
insert into t1 values(09:30:00.001,`DELL,130,40.5)
b=[2,4,3,6,5]
ewmMean(X=t1,com=0.5);
```

返回如下：

| time | sym | qty | price |
| --- | --- | --- | --- |
| 09:30:00.001 | AAPL | 100 | 56.5 |
| 09:30:00.001 | AAPL | 175 | 37 |
| 09:30:00.001 | DELL | 157.6923 | 35.9615 |
| 09:30:00.001 | DELL | 166 | 52.525 |
| 09:30:00.001 | DELL | 141.9008 | 44.4752 |

**相关信息**

* [ewmCorr](ewmCorr.html "ewmCorr")
* [ewmCov](ewmCov.html "ewmCov")
* [ewmStd](ewmStd.html "ewmStd")
* [ewmVar](ewmVar.html "ewmVar")
