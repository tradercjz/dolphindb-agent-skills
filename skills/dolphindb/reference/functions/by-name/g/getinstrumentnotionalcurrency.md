# getInstrumentNotionalCurrency

首发版本：3.00.4.3

## 语法

`getInstrumentNotionalCurrency(instrument)`

## 详情

根据输入的金融工具，获取该工具的名义本金所使用的货币。

## 参数

**instrument** INSTRUMENT 类型标量或向量，表示金融工具。

## 返回值

字符串标量或向量。

## 例子

```
deposit =  {
    "productType": "Cash",
    "assetType": "Deposit",
    "start": 2025.05.15,
    "maturity": 2025.08.15,
    "rate": 0.02,
    "dayCountConvention": "Actual360",
    "notionalAmount":1E6,
    "notionalCurrency":"CNY",
    "payReceive": "Receive"
}
instrument = parseInstrument(deposit)
getInstrumentNotionalCurrency(instrument)

// output: "CNY"
```

**相关函数：**parseInstrument、getInstrumentField、getInstrumentKeys、getInstrumentNotionalAmount
