# isQuarterEnd

## 语法

`isQuarterEnd(X)`

## 详情

判断 *X* 是否为季度最后一天。

## 参数

**X** 可以是 DATE, DATEHOUR, DATETIME, TIMESTAMP 或 NANOTIMESTAMP
类型的标量或向量。

## 返回值

布尔标量或向量。

## 例子

```
isQuarterEnd(2012.06.30);
// output: true

isQuarterEnd([2012.06.30,2012.07.01]);
// output: [true,false]
```

相关函数：isQuarterStart
