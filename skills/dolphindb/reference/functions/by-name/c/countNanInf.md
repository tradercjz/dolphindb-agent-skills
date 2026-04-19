# countNanInf

## 语法

`countNanInf(X, [includeNull=false])`

## 详情

聚合函数，用于统计 *X* 中 NaN 或 Inf 值的数量。若 *includeNull* 设为 true，NULL 值也会被统计，默认为
false。

## 参数

**X** 是 DOUBLE 类型 的标量/向量/矩阵。

**includeNull** 是一个布尔值。

## 返回值

INT 类型标量。

## 例子

```
x = [1.5, float(`nan), 2.3, float(`inf), NULL, 3.7]

// includeNull = false (默认)，不统计 NULL 值
countNanInf(x)
// output: 2

// includeNull = true，统计 NULL 值
countNanInf(x,true)
// output: 3
```

相关函数：isNanInf
