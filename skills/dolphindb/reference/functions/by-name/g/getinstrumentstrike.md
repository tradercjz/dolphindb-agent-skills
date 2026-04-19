# getInstrumentStrike

首发版本：3.00.4.1

## 语法

`getInstrumentStrike(instrument)`

## 详情

根据输入的金融工具，获取该工具的执行价格。

## 参数

**instrument** INSTRUMENT 类型标量或向量，表示金融工具。

## 返回值

DOUBLE 类型标量或向量。

## 例子

```
forward =  {
   "productType": "Forward",
    "forwardType": "FxForward",
    "expiry": 2025.09.24,
    "delivery": 2025.09.26,
    "currencyPair": "USDCNY",
    "direction": "Buy",
    "notionalCurrency": "USD",
    "notionalAmount": 1E8,
    "strike": 7.2
}
instrument = parseInstrument(forward)

getInstrumentStrike(instrument)
// output: 7.2
```

**相关函数：**parseInstrument、getInstrumentField、getInstrumentKeys
