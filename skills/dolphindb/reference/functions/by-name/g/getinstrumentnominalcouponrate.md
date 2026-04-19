# getInstrumentNominalCouponRate

首发版本：3.00.4.1

## 语法

`getInstrumentNominalCouponRate(instrument)`

## 详情

根据输入的金融工具，获取该工具的名义票面利率。

## 参数

**instrument** INSTRUMENT 类型标量或向量，表示金融工具。

## 返回值

DOUBLE 类型标量或向量。

## 例子

```
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
instrument = parseInstrument(futures)
getInstrumentNominalCouponRate(instrument)

// output: 0.03
```

**相关函数：**parseInstrument、getInstrumentField、getInstrumentKeys
