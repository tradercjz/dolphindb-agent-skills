# tmovingWindowData

## 语法

`tmovingWindowData(T, X, window, [leftClosed =
false])`

## 详情

返回一个数组向量，其每行元素表示 *X* 每个滑动窗口的元素。

## 参数

**T** 是一个非严格递增的整型或时间类型的向量。

**X** 是一个与 T 长度相同的向量。

**window** 是一个正整型或 DURATION 标量，表示以时间衡量的窗口的长度。

**leftClosed** 是一个布尔值，表示窗口是否包含左边界的数据，默认为 false。

## 例子

```
T = 2022.01.01T09:00:00 + 1 1 2 3 6 7 9 10 13 14
S = 1..10
tmovingWindowData(T, S, 3s)
[[1],[1,2],[1,2,3],[1,2,3,4],[5],[5,6],[6,7],[7,8],[9],[9,10]]

tmovingWindowData(T, S, 3s, leftClosed=true)
[[1],[1,2],[1,2,3],[1,2,3,4],[4,5],[5,6],[5,6,7],[6,7,8],[8,9],[9,10]]

// 在响应式引擎中获取10分钟滑动窗口的数据
n = 100
DateTime = 2023.01.01T09:00:00 + rand(10000, n).sort!()
SecurityID = take(`600021`600022`600023`600024`600025, n)
Price = 1.0 + rand(1.0, n)
t = table(1:0, `DateTime`SecurityID`Price, [TIMESTAMP, SYMBOL, DOUBLE])
tableInsert(t, DateTime, SecurityID, Price)
output = table(100:0, `SecurityID`DateTime`PriceNew, [SYMBOL, DATETIME, DOUBLE[]])

engine = createReactiveStateEngine(name="rseEngine", metrics=[<DateTime>, <tmovingWindowData(DateTime, Price,10m)>], dummyTable=t, outputTable=output, keyColumn=`SecurityID, keepOrder=true)
engine.append!(t)
dropStreamEngine(`rseEngine)
```
