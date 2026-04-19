# toTuple

首发版本：3.00.5

## 语法

`toTuple(X)`

## 详情

该函数与 group by 搭配使用，按照分组将 *X*
转换为元组 (tuple)。如果单独使用则没有效果。

toArray 生成的 Array Vector 后续更新时不能修改长度，而
`toTuple` 无此限制，适用于长度会发生变化的数据分组场景，特别适合需要频繁更新或动态长度的数据处理。

## 参数

**X** 是表的列字段名称或包含列字段的计算表达式。

## 返回值

一个元组（tuple）。

## 例子

```
t = table(1 1 3 4 as id, 10.1 10.3 9.5 9.6 as price)
select toTuple(price) as newPrice from t group by id
```

| id | newPrice |
| --- | --- |
| 1 | [10.1,10.3] |
| 3 | [9.5] |
| 4 | [9.6] |

模拟投资组合持仓数据：组合ID、股票代码、持仓数量（动态变化）。

```
t = table([`P1, `P1, `P1, `P2, `P2, `P3, `P3, `P3, `P3] as portfolioId,
          [`AAPL, `GOOG, `MSFT, `AAPL, `TSLA, `GOOG, `GOOG, `AMZN, `NVDA] as symbol,
          [100, 50, 200, 150, 75, 80, 120, 90, 60] as position)

// 使用 toTuple 按投资组合分组，聚合所有持仓股票和数量为元组（长度可变）
result = select toTuple(symbol) as symbols, toTuple(position) as positions from t group by portfolioId
result
```

| portfolioId | symbols | positions |
| --- | --- | --- |
| P1 | ['AAPL', 'GOOG', 'MSFT'] | [100, 50, 200] |
| P2 | ['AAPL', 'TSLA'] | [150, 75] |
| P3 | ['GOOG', 'GOOG', 'AMZN', 'NVDA'] | [80, 120, 90, 60] |

**相关函数：**toArray, toColumnarTuple。
