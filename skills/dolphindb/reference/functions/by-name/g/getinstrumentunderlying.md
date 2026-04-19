# getInstrumentUnderlying

首发版本：3.00.4.1

## 语法

`getInstrumentUnderlying(instrument)`

## 详情

根据输入的金融工具，获取该工具的标的资产。

## 参数

**instrument** INSTRUMENT 类型标量或向量，表示金融工具。

## 返回值

* 当 *instrument* 为国债期货标量时，返回为 INSTRUMENT 标量；
* 当 *instrument* 为其他标量时，返回类型为 STRING 标量；
* 当 *instrument* 为包含国债期货的向量时，返回元组；
* 当 *instrument* 为不包含国债期货的向量时，返回 STRING 向量。

## 例子

```
bond ={
    "productType": "Cash",
    "assetType": "Bond",
    "bondType": "FixedRateBond",
    "instrumentId": "220010.IB",
    "start": 2020.12.25,
    "maturity": 2031.12.25,
    "issuePrice": 100.0,
    "coupon": 0.0149,
    "frequency": "Annual",
    "dayCountConvention": "ActualActualISDA"
}

futures =  {
    "productType": "Futures",
    "futuresType": "BondFutures",
    "instrumentId": "T2509",
    "nominal": 100.0,
    "maturity": "2022.09.09",
    "settlement": "2022.09.11",
    "underlying": bond,
    "nominalCouponRate": 0.03
}
ins1 = parseInstrument(futures)

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
ins2 = parseInstrument(option)

x = getInstrumentUnderlying(ins1)
y = getInstrumentUnderlying(ins2) //EURUSD
z = getInstrumentUnderlying([ins1,ins2])

typestr x // INSTRUMENT
typestr y // STRING
typestr z // ANY VECTOR
```

**相关函数：**parseInstrument、getInstrumentField、getInstrumentKeys
