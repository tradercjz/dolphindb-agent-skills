# movingWindowData

## 语法

`movingWindowData(X, window, [fixed=false])`

## 详情

用于返回向量 *X* 在每个滑动窗口内的所有元素。

## 参数

**X** 是一个向量（常规向量/元组/数组向量）。

**window** 必须是不小于 2 的正整数，表示以元素个数衡量的窗口的长度。

**fixed** 是一个布尔值，表示输出的数组向量中每行元素的长度是否为 *window*。默认值为 false，直接输出窗口内的元素。设置为
true，前 (*window* - 1)个窗口内缺少的元素用 NULL 填充。

## 返回值

返回一个数组向量。

## 例子

```
S = -1 3 -4 0 5 10 9 7
m = movingWindowData(X=S,window=3);
m;
// output: [[-1],[-1,3],[-1,3,-4],[3,-4,0],[-4,0,5],[0,5,10],[5,10,9],[10,9,7]]

mi = movingWindowData(X=S,window=3,fixed=true);
mi;
// output: [[00i,00i,-1],[00i,-1,3],[-1,3,-4],[3,-4,0],[-4,0,5],[0,5,10],[5,10,9],[10,9,7]]

// 获取每个窗口第一个元素的值
m[0]
// output: [-1,-1,-1,3,-4,0,5,10]

mi[0]
// output: [,,-1,3,-4,0,5,10]

// X 为元组
s = [[-1,1], [0], [3], [5,6], [7], [8,9], [10,13]]
m1 = movingWindowData(X=s,window=3);
m1;
// output: [[[-1,1]], [[-1,1], [0]], [[-1,1], [0], [3]], [[0], [3], [5,6]], [[3], [5,6], [7]], [[5,6], [7], [8,9]], [[7], [8,9], [10,13]]]

// X 为数组向量
a = array(INT[], 0, 10).append!([1 2 3, 4 5, 6 7 8, 9 10]);
m2 = movingWindowData(X=a,window=3);
m2;
// output: [[[1,2,3]], [[1,2,3], [4,5]], [[1,2,3], [4,5], [6,7,8]], [[4,5], [6,7,8], [9,10]]]

// 在响应式引擎中获取长度为 5 的滑动窗口的数据
n = 100
DateTime = 2023.01.01T09:00:00 + rand(10000, n).sort!()
SecurityID = take(`600021`600022`600023`600024`600025, n)
Price = 1.0 + rand(1.0, n)
t = table(1:0, `DateTime`SecurityID`Price, [TIMESTAMP, SYMBOL, DOUBLE])
tableInsert(t, DateTime, SecurityID, Price)
output = table(100:0, `SecurityID`DateTime`PriceNew, [SYMBOL, DATETIME, DOUBLE[]])

engine = createReactiveStateEngine(name="rseEngine", metrics=[<DateTime>, <movingWindowData(Price,5)>], dummyTable=t, outputTable=output, keyColumn=`SecurityID, keepOrder=true)
engine.append!(t)
dropStreamEngine(`rseEngine)
```
