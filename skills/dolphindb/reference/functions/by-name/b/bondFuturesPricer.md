# bondFuturesPricer

首发版本：3.00.4

## 语法

`bondFuturesPricer(instrument, pricingDate,
discountCurve)`

## 详情

计算国债期货合约的净现值。

## 参数

注意：所有输入向量必须等长，输入标量将自动扩展以匹配其它向量的长度。

**instrument** INSTRUMENT 类型标量或向量，一个 BondFutures 对象，表示国债期货合约。

**pricingDate** DATE 类型标量或向量，表示定价日期 。

**discountCurve** MKTDATA 类型标量或向量，一个 IrYieldCurve 对象，表示折现曲线。

## 返回值

DOUBLE 类型标量或向量。

## 例子

```
bond = {
    "productType": "Cash",
    "assetType": "Bond",
    "bondType": "FixedRateBond",
    "instrumentId": "220010.IB",
    "start": "2022.05.15",
    "maturity": "2032.05.15",
    "issuePrice": 100.0,
    "coupon": 0.0276,
    "frequency": "Semiannual",
    "dayCountConvention": "ActualActualISDA"
}

bondFutures = {
    "productType": "Futures",
    "futuresType": "BondFutures",
    "instrumentId": "T2509",
    "nominal": 100.0,
    "maturity": "2025.09.12",
    "settlement": "2025.09.16",
    "underlying": bond,
    "nominalCouponRate": 0.03
}

instrument = parseInstrument(bondFutures)
pricingDate = 2025.06.10
curve = {
    "mktDataType": "Curve",
    "curveType": "IrYieldCurve",
    "referenceDate": pricingDate,
    "currency": "CNY",
    "dayCountConvention": "ActualActualISDA",
    "compounding": "Compounded",
    "interpMethod": "Linear",
    "extrapMethod": "Flat",
    "frequency": "Semiannual",
    "dates":[2025.09.05, 2025.12.05, 2026.03.05, 2027.03.05, 2028.03.05, 2030.03.05, 2035.03.05, 2040.03.05, 2045.03.05, 2055.03.05, 2075.03.05],
    "values":[1.5347, 1.4958, 1.4447, 1.3955, 1.5029, 1.5561, 1.7156, 1.8652, 2.0329, 1.8955, 2.1059] / 100.0
}
discountCurve = parseMktData(curve)
npv = bondFuturesPricer(instrument, pricingDate, discountCurve)
print(npv)  // output:108.716241945330267
bondFuturesPricer([instrument, instrument], pricingDate, discountCurve)
bondFuturesPricer(instrument, [pricingDate, pricingDate, pricingDate], discountCurve)
bondFuturesPricer(instrument, [pricingDate, pricingDate, pricingDate], [discountCurve, discountCurve, discountCurve])
bondFuturesPricer(instrument, pricingDate, [discountCurve, discountCurve, discountCurve])
```
