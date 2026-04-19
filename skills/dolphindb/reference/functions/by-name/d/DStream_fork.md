# DStream::fork

首发版本：3.00.3

## 语法

`DStream::fork(count)`

## 详情

生成多个流数据下游 DStream 分支（以广播方式复制数据），便于在不同分支中执行各自的处理逻辑。

## 参数

**count** 整数，指定分叉数量。

## 返回值

指定数量的 DStream 实例列表。

## 例子

将 K 线数据复制两份，分别计算 1 分钟和 5 分钟级因子：

```
use catalog test

g = createStreamGraph("indicators")
sourceStreams = g.source("trade", `symbol`datetime`price`volume, [SYMBOL, TIMESTAMP,DOUBLE, INT])
    .fork(2)
stream_1min = sourceStreams[0]
    .timeSeriesEngine(60*1000, 60*1000, <[first(price),max(price),min(price),last(price),sum(volume)]>, "datetime", false, "symbol")
    .reactiveStateEngine(<[datetime, first_price, max_price, min_price, last_price, sum_volume, mmax(max_price, 5), mavg(sum_volume, 5)]>, `symbol)
    .sink("output_1min")
stream_5min = sourceStreams[1]
    .timeSeriesEngine(5*60*1000, 5*60*1000, <[first(price),max(price),min(price),last(price),sum(volume)]>, "datetime", false, "symbol")
    .reactiveStateEngine(<[datetime, first_price, max_price, min_price, last_price, sum_volume, mmax(max_price, 5), mavg(sum_volume, 5)]>, `symbol)
    .sink("output_5min")
g.submit()
```
