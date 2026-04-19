# createDeviceEngine

## 语法

`createDeviceEngine(name, metrics, dummyTable, outputTable, [keyColumn],
[keepOrder])`

## 详情

创建一个设备引擎，该引擎会将注入输入表的数据，通过 GPU 加速完成 metrics 中定义的计算，将结果输出到输出表。

注意：设备引擎不维护上一批数据的状态。即两批数据写入时，第二批数据的起始状态与第一批状态无关。

## 参数

**name** 字符串标量，表示设备引擎的名称，作为其在一个数据节点/计算节点上的唯一标识。可包含字母，数字和下划线，但必须以字母开头。

**metrics** 以元代码的形式表示计算公式，可以是一个或多个表达式、系统内置或用户自定义函数（不支持多返回值，for 循环不得嵌套，for
循环次数不能超过100），也可以是个常量标量/向量。当指定为常量向量时，对应的输出列应该设置为数组向量类型。有关元代码的详情可参考 Metaprogramming。**metrics**
支持的函数包括：

* 单目基础运算操作：not, neg, cast, log, log2, log10 ,log1p ,abs, sign, sqrt, sin,
  sinh, asin, asinh, cos, cosh, acos, acosh, tan, tanh, atan, atanh,
  reciprocal, cbrt, exp, exp2, expm1
* 双目基础运算操作：add, sub, mul, div, ratio, pow, lt, gt, le, ge, eq, ne, and, or,
  or\_\_（即`||`运算符，需要注意关于 NULL 的处理依赖于配置项
  `logicOrIgnoreNull` ）, max, min
* 双目整型运算（其中 mod 支持 BOOL 类型，其他只支持数值类型)：mod, bitAnd, bitOr, bitXor, lshift,
  rshift
* 三目运算：iif
* 单目滑动窗口函数：mavg, msum, mcount, mprod, mvar, mvarp, mstd, mstdp, mskew,
  mkurtosis, mmin, mmax, mimin, mimax, sma, wma, mfirst, mlast, mrank,
  mmaxPositiveStreak, mmed, mpercentile, mmad（暂不支持参数 *useMedian*）
* 双目滑动窗口函数：sma, ema, wma, dema, tema, trima, t3, wilder, gema,
  linearTimeTrend, ma, talib（仅支持所有 m 系列和 mTopN 函数，不支持其他函数）, kama
* 其他滑动窗口函数：linearTimeTrend，mslr
* 单目累计窗口函数：cumsum, cumprod, cummin, cummax, cumvar, cumvarp, cumstd,
  cumstdp, cumnunique, cumfirstNot, cumlastNot, cumavg, cumcount,
  cumPositiveStreak
* 双目累计窗口函数：cumcorr, cumcovar, cumbeta, cumwsum, cumwavg
* 序列相关函数：deltas, ratios, ffill, move, prev, next, percentChange, iterate,
  prevState, ewmMean, ewmVar, ewmStd, ewmCov, ewmCorr

  注意：ewmVar, ewmStd, ewmCov, ewmCorr 均不支持设置 adjust=true，且不支持设置
  bias=false。
* row系列函数：rowMin, rowMax, rowAnd, rowOr, rowXor, rowProd, rowSum, rowSum2,
  rowSize, rowCount, rowAvg, rowVar, rowVarp, rowStd, rowStdp
* tm系列函数：tmsum, tmsum2, tmavg, tmprod, tmcount, tmvar, tmvarp, tmstd, tmstdp,
  tmcovar, tmcorr, tmwavg, tmwsum, tmbeta, tmfirst, tmlast, tmmin, tmmax,
  tmskew, tmkurtosis, tmove
* 其他函数：TrueRange，topRange，lowRange，stateMavg

注意：自 3.00.1 版本起，当计算结果的绝对值小于 `DBL_EPSILON*10000`(约
2.22\*10-12)时，所有滑动窗口系列函数和累积窗口系列函数均不会对结果进行约整，而是保留所有精度。

**dummyTable** 一个表对象，注入数据的结构与其 schema 一致。可以含有数据，亦可为空表。

**outputTable** 计算结果的输出表，可以是内存表或分布式表。使用
`createDeviceReactiveEngine`函数之前，需要将输出表预先设立为一个空表，并指定各列列名以及数据类型。`DeviceReactiveEngine`会将计算结果注入该表。

**keyColumn** 可选参数，字符串标量或向量表示分组列名。计算将在各分组进行。

**keepOrder** 可选参数，表示输出表数据是否按照输入时的顺序排序。默认值为 false。设置 *keepOrder* =
true，表示输出表按照输入时的顺序排序； *keepOrder* = false，表示输出表按照分组列排序。

## 返回值

一个表对象。

## 例子

```
// 创建引擎
dummyTb = table(1:0, `sym`id`value, [SYMBOL,INT,DOUBLE])
share table(100:0, `sym`id`flag`value`factor, [SYMBOL,INT,SYMBOL,DOUBLE,DOUBLE]) as result
de = createDeviceEngine(name="myDe", metrics=[<id>,<"flag"+"_A">,<value>,<mavg(value,5)>], dummyTable=dummyTb, outputTable=result, keyColumn="sym")

// 准备数据
data1 = table(take("A", 100) as sym, 1..100 as id, double(10+1..100) as value)
data2 = table(take("B", 100) as sym, 1..100 as id, double(20+1..100) as value)
data3 = table(take("C", 100) as sym, 1..100 as id, double(30+1..100) as value)
data = data1.unionAll(data2).unionAll(data3).sortBy!(`id)

// 写入数据
de.append!(data)
select top 10 * from result
```

| sym | id | flag | value | factor |
| --- | --- | --- | --- | --- |
| A | 1 | flag\_A | 11 |  |
| A | 2 | flag\_A | 12 |  |
| A | 3 | flag\_A | 13 |  |
| A | 4 | flag\_A | 14 |  |
| A | 5 | flag\_A | 15 | 13 |
| A | 6 | flag\_A | 16 | 14 |
| A | 7 | flag\_A | 17 | 15 |
| A | 8 | flag\_A | 18 | 16 |
| A | 9 | flag\_A | 19 | 17 |
| A | 10 | flag\_A | 20 | 18 |
