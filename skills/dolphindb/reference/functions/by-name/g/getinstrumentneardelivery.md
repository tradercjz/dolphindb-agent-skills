# getInstrumentNearDelivery

首发版本：3.00.4.1

## 语法

`getInstrumentNearDelivery(instrument)`

## 详情

根据输入的金融工具，获取该工具的近端交割日期（near delivery date）。

## 参数

**instrument** INSTRUMENT 类型标量或向量，表示金融工具。

## 返回值

DATE 类型标量或向量。

## 例子

```
swap = {
    "productType": "Swap",
    "swapType": "FxSwap",
    "currencyPair": "EURUSD",
    "direction": "Buy",
    "notionalCurrency": "EUR",
    "notionalAmount": 1E6,
    "nearStrike": 1.1,
    "nearExpiry": 2025.12.08,
    "nearDelivery": 2025.12.10,
    "farStrike": 1.2,
    "farExpiry": 2026.06.08,
    "farDelivery": 2026.06.10
}
ins = parseInstrument(swap)
getInstrumentNearDelivery(ins)

// output: 2025.12.10
```

**相关函数：**parseInstrument、getInstrumentField、getInstrumentKeys
