# DStream::map

首发版本：3.00.3

## 语法

`DStream::map(func)`

## 详情

对流中的数据做映射，将指定函数应用到流数据中的每条消息。适用于无状态的数据处理场景（比如数据过滤）。

## 参数

**func** 一元函数，入参为流数据消息组成的表。函数返回一个表，后续引擎根据返回的表结构推导处理逻辑。

注意：*func* 必须是纯函数（pure function），即必须满足：

* 对于相同的输入，总是返回相同的输出。
* 不能产生任何副作用，例如：

  + 修改全局变量或函数外部状态。
  + 写入数据库或文件。
  + 调用外部服务（如发送 HTTP 请求）。
  + 修改传入的参数对象（例如对原始表进行原地更改）。

## 返回值

返回一个 DStream 对象。

## 例子

定义 `map` 合成 AAPL 标的 K 线：

```
use catalog test

g = createStreamGraph("graph")
g.source("trade", `symbol`datetime`price`volume, [SYMBOL,TIMESTAMP,DOUBLE,INT])
    .map(msg -> select * from msg where symbol == "AAPL")
    .timeSeriesEngine(60, 60, <[first(price) as open, max(price) as high, min(price) as low, last(price) as close, sum(volume) as volume]>, "datetime", false, "symbol")
    .sink("output")
```

**相关函数：**DStream::udfEngine
