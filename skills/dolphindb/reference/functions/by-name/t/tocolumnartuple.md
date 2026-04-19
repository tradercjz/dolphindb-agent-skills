# toColumnarTuple

首发版本：3.00.5

## 语法

`toColumnarTuple(X)`

## 详情

该函数与 group by 搭配使用，按照分组将 *X*
转换为列式元组 (columnar tuple)。如果单独使用则没有效果。

## 参数

**X** 是表的列字段名称或包含列字段的计算表达式。

## 返回值

列式元组 (columnar tuple)。

## 例子

```
t = table([`AAPL, `AAPL, `GOOG, `GOOG, `MSFT, `MSFT] as symbol,
          [182.5, 183.2, 145.8, 146.5, 412.3, 411.8] as price)
t
```

| symbol | price |
| --- | --- |
| AAPL | 182.5 |
| AAPL | 183.2 |
| GOOG | 145.8 |
| GOOG | 146.5 |
| MSFT | 412.3 |
| MSFT | 411.8 |

使用 `toColumnarTuple` 按股票分组，聚合所有价格。聚合后的价格列为 columnar tuple。

```
result = select toColumnarTuple(price) as prices from t group by symbol
result
```

| symbol | prices |
| --- | --- |
| AAPL | [182.5, 183.2] |
| GOOG | [145.8, 146.5] |
| MSFT | [412.3, 411.8] |

**相关函数：**toArray, toTuple。
