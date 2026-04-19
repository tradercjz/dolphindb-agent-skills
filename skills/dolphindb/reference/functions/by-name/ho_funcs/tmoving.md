# tmoving

## 语法

`tmoving(func, T, funcArgs, window, [excludedPeriod])`

## 详情

应用函数/运算符到给定对象的一个滚动窗口上。

内置函数 tmsum, tmcount 和 tmavg 为各自的计算场景进行了优化，因此比 *tmoving* 高阶函数有更好的性能。

## 参数

* **func** 是一个函数。
* **T** 是一个递增的整型或时间类型的向量，且不能包含NULL值。
* **funcArgs**
  是函数func的参数。可为向量、字典或表。如果有多个参数，则用元组表示，并且每个参数的长度（向量/字典的元素个数或表的行数）必须相同。
* **window** 是一个正整数或一个 duration，表示滚动窗口的区间大小。

  对于 *T* 中每个元素 *Ti*：
  + 当 *T* 为整型时，确定的窗口区间为 (*Ti*
    - window, *Ti* ]
  + 当 *T* 为时间类型时， 确定的窗口区间为
    (temporalAdd(*Ti*, -window), *Ti*]
* **excludedPeriod** 是　TIME、NANOTIME、MINUTE 和 SECOND
  类型的数据对。用于设定一个交易日内的非交易时间段（该时间段被排除在计算窗口之外）。若设置该参数，必须同时保证以下3点：

  + 数据对中的右值必须大于左值。
  + 时间段长度必须小于 (24 - *window*)
  + *T* 中不能包含 *excludedPeriod* 区间内的时间，且数据类型必须是 TIMESTAMP,
    NANOTIMESTAMP, TIME 或 NANOTIME。

其他相关的 tm 系列函数的参数说明和窗口计算规则请参考: tmFunctions

## 返回值

一个与输入参数长度相同的向量。

## 例子

```
date=2021.08.01 2021.08.02 2021.08.02 2021.08.02 2021.08.03 2021.08.04 2021.08.05 2021.08.06 2021.08.09 2021.08.10 2021.08.14
value=1..11
t = table(date,value)
timer(100) select date, value, tmoving(avg,date,value,3d) from t;

//output: Time elapsed: 7.9 ms
```

```
timer(100) select date, value, tmavg(date, value, 3d) from t;

//output: Time elapsed: 6.805 ms
```

单独打印计算结果，可以看到，当窗口滑动到2021.08.09，计算窗口范围为 [2021.08.07, 2021.08.08,
2021.08.09]，但 7 日和 8 日值缺失，因此不参与计算。

| date | value | tmoving\_sum |
| --- | --- | --- |
| 2021.08.01 | 1 | 1 |
| 2021.08.02 | 2 | 1.5 |
| 2021.08.02 | 3 | 2 |
| 2021.08.02 | 4 | 2.5 |
| 2021.08.03 | 5 | 3 |
| 2021.08.04 | 6 | 4 |
| 2021.08.05 | 7 | 6 |
| 2021.08.06 | 8 | 7 |
| 2021.08.09 | 9 | 9 |
| 2021.08.10 | 10 | 9.5 |
| 2021.08.14 | 11 | 11 |

下例通过 *excludedPeriod* 参数指定股市上午的休市时间，计算长度为一分钟的滚动窗口内的价格平均值。

```
excludedPeriod=(11:30:00:13:00:00)
ts=timestamp(2023.11.01T11:21:00+1..500) join timestamp(2023.11.01T13:00:00+1..500)
t=table(ts, rand(10.0,size(ts)) as price)

// 通过 excludedPeriod 指定休市时间为11:30:00 到 13:00:00，则此段时间被忽略，不会被作为计算窗口。
res1=select ts, tmoving(func=avg, T=ts, funcArgs=price, window=1m, excludedPeriod=excludedPeriod) from t
// 不指定 excludedPeriod 时，休市时间也会被考虑为计算窗口。
res2=select ts, tmoving(func=avg, T=ts, funcArgs=price, window=1m) from t

// 对比是否指定 excludedPeriod 的计算结果。
select * from res1 where ts between timestamp(2023.11.01T13:00:00) and timestamp(2023.11.01T13:01:00)

select * from res2 where ts between timestamp(2023.11.01T13:00:00) and timestamp(2023.11.01T13:01:00)
```

下例通过指定多个 *funcArgs* 参数，计算长度为 5 分钟的滚动窗口内债券价格在达到峰值后的最低值。

```
data_time = 2023.01.01T00:00:00 + 0..5 * 3600000
last_price_bond = 100 + rand(10.0, 10)

defg getMinPrice(data_time, last_price_bond){
        maxPriceTime = atImax(last_price_bond, data_time)
        maxPrice = max(last_price_bond)
        newPriceList = min(iif(data_time<maxPriceTime, maxPrice, last_price_bond))
        return min(newPriceList)
}
calTime = "5m"
tmoving(getMinPrice, data_time, [data_time, last_price_bond], duration(calTime))
```
