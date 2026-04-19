# getInstrumentInstrumentId

首发版本：3.00.4.1

## 语法

`getInstrumentInstrumentId(instrument)`

## 详情

根据输入的金融工具，获取该工具的 ID。

## 参数

**instrument** INSTRUMENT 类型标量或向量，表示金融工具。

## 返回值

STRING 类型标量或向量。

## 例子

```
bond = {
    "productType": "Cash",
    "assetType": "Bond",
    "bondType": "DiscountBond",
    "instrumentId": "259924.IB",
    "start": 2025.04.17,
    "maturity": 2025.07.17,
    "issuePrice": 99.664,
    "dayCountConvention": "ActualActualISDA"
}
instrument = parseInstrument(bond)
getInstrumentInstrumentId(instrument)

// output: 259924.IB
```

**相关函数：**parseInstrument、getInstrumentField、getInstrumentKeys
