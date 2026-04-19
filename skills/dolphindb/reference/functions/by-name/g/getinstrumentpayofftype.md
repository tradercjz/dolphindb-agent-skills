# getInstrumentPayoffType

首发版本：3.00.4.1

## 语法

`getInstrumentPayoffType(instrument)`

## 详情

根据输入的金融工具，获取该工具的收益类型。

## 参数

**instrument** INSTRUMENT 类型标量或向量，表示金融工具。

## 返回值

STRING 类型标量或向量。

## 例子

```
option = {
    "productType": "Option",
    "optionType": "EuropeanOption",
    "assetType": "FxEuropeanOption",
    "notionalCurrency": "EUR",
    "notionalAmount": 1000000.0,
    "strike": 1.2,
    "maturity": "2025.10.08",
    "payoffType": "Call",
    "dayCountConvention": "Actual365",
    "underlying": "EURUSD"
}
ins = parseInstrument(option)
getInstrumentPayoffType(ins)
// output: Call
```

**相关函数：**parseInstrument、getInstrumentField、getInstrumentKeys
