# getInstrumentIssuePrice

首发版本：3.00.4.1

## 语法

`getInstrumentIssuePrice(instrument)`

## 详情

根据输入的金融工具，获取该工具的发行价格（Issue Price）。

## 参数

**instrument** INSTRUMENT 类型标量或向量，表示金融工具。

## 返回值

DOUBLE 类型标量或向量。

## 例子

```
bond = {
    "productType": "Cash",
    "assetType": "Bond",
    "bondType": "FixedRateBond",
    "nominal": 100,
    "instrumentId": "0001",
    "start": 2022.05.15,
    "maturity": 2032.05.15,
    "dayCountConvention": "ActualActualISDA",
    "coupon": 0.0276,
    "issuePrice": 100.0,
    "frequency": "Semiannual"
}
ins = parseInstrument(bond)
getInstrumentIssuePrice(ins)
// output: 100
```

**相关函数：**parseInstrument、getInstrumentField、getInstrumentKeys
