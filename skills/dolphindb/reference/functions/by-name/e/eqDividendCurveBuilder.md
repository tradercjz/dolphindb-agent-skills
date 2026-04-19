# eqDividendCurveBuilder

首发版本：3.00.5

## 语法

`eqDividendCurveBuilder(referenceDate, termDates, method,
[futPrices], [callPrices], [putPrices], [strikes], spot, discountCurve,
dayCountConvention='Actual365', [curveName])`

## 详情

构建权益类分红（股息）曲线。

## 参数

**referenceDate** DATE 类型标量，表示曲线的生成日期。

**termDates** DATE 类型向量，表示曲线的期限日期，要求严格单调递增，且大于 *referenceDate*。

**method** STRING 类型标量，可选 “CallPutParity” 和 “FuturesPrice”：

* method = “CallPutParity”，表示通过看涨看跌平价关系推导隐含股息率；需要使用
  *callPrices*、*putPrices*、*strikes*
* method = “FuturesPrice”，表示通过期货价格公式推导隐含股息率；需要使用 *futPrices*

**futPrices** 可选参数，DOUBLE 类型向量，正数，表示标的期货合约价格。

**callPrices** 可选参数，DOUBLE 类型矩阵，正数，表示看涨期权的价格矩阵。

**putPrices** 可选参数，DOUBLE 类型矩阵，正数，表示看跌期权的价格矩阵。

**strikes** 可选参数，DOUBLE 类型矩阵，表示执行价，要求严格单调递增。

**注**：

* *callPrices*、*putPrices*、*strikes* 三者形状一致且列数与 *termDates*
  等长。
* *futPrices* 也与 *termDates* 等长。

**spot** DOUBLE 类型标量，正数，表示标的的即期价格。

**discountCurve** MKTDATA 类型标量，一个 IrYieldCurve 对象，表示折现曲线。

**dayCountConvention** STRING 类型标量，表示计息日数惯例。可选值为：

* "Actual365"（默认）：实际/365
* "Actual360"：实际/360
* "ActualActualISMA"：实际/实际（ISMA 规则）
* "ActualActualISDA"：实际/实际（ISDA 规则）

**curveName** 可选参数，STRING 类型标量，表示曲线名称。

## 返回值

MKTDATA 类型对象。

## 例子

### CallPutParity

通过 CallPutParity 方法构建一条上证 50ETF（标的代码： 510050.SH）的股息曲线。

```
referenceDate = 2026.02.13
spot = 3.114  // Close Price Of 510050.SH

// 1. Term Structure (Option Expiry Dates)
termDates = [2026.02.25, 2026.03.25, 2026.06.24, 2026.09.23]

// 2. Raw Data Matrices (Settlement Price)
callPrices = matrix(
    [0.2640, 0.2140, 0.1640, 0.1140, 0.0327, 0.0042, 0.0016, 0.0008, 0.0003, 0.0002],
    [0.2723, 0.2289, 0.1810, 0.1424, 0.0721, 0.0323, 0.0138, 0.0075, 0.0050, 0.0039],
    [0.3150, 0.2770, 0.2391, 0.2073, 0.1519, 0.1061, 0.0731, 0.0519, 0.0379, 0.0280],
    [0.3521, 0.3170, 0.2850, 0.2555, 0.2030, 0.1577, 0.1243, 0.0986, 0.0790, 0.0642]
)
putPrices = matrix(
    [0.0004, 0.0008, 0.0021, 0.0044, 0.0215, 0.0928, 0.1889, 0.2884, 0.3895, 0.4903],
    [0.0090, 0.0124, 0.0170, 0.0260, 0.0590, 0.1225, 0.1993, 0.2928, 0.3918, 0.4903],
    [0.0352, 0.0463, 0.0571, 0.0746, 0.1188, 0.1733, 0.2401, 0.3204, 0.4049, 0.4938],
    [0.0601, 0.0739, 0.0903, 0.1091, 0.1548, 0.2113, 0.2795, 0.3471, 0.4307, 0.5120]
)
strikes = matrix(
    [2.8500, 2.9000, 2.9500, 3.0000, 3.1000, 3.2000, 3.3000, 3.4000, 3.5000, 3.6000],
    [2.8500, 2.9000, 2.9500, 3.0000, 3.1000, 3.2000, 3.3000, 3.4000, 3.5000, 3.6000],
    [2.8500, 2.9000, 2.9500, 3.0000, 3.1000, 3.2000, 3.3000, 3.4000, 3.5000, 3.6000],
    [2.8500, 2.9000, 2.9500, 3.0000, 3.1000, 3.2000, 3.3000, 3.4000, 3.5000, 3.6000]
)

// 3. Discount Curve
// Data From https://www.chinamoney.com.cn/chinese/bkcurvuir/
terms = [1d, 1w, 2w, 3w, 1M, 2M, 3M, 6M, 9M, 1y, 18M, 2y, 3y]
dates = array(DATE, size(terms))
for(i in 0..(size(terms)-1)){
    dates[i] = transFreq(temporalAdd(referenceDate, terms[i]), "CFET", "right", "right")
}
discountCurveDict = {
    "mktDataType": "Curve",
    "curveType": "IrYieldCurve",
    "curveName": "CNY_FR_007",
    "referenceDate": referenceDate,
    "currency": "CNY",
    "dayCountConvention": "Actual365",
    "compounding": "Continuous",
    "interpMethod": "Linear",
    "extrapMethod": "Flat",
    "dates": dates,
    "values":[1.5577, 1.5247, 1.5181, 1.5181, 1.5195, 1.5216, 1.5167, 1.4964, 1.4758, 1.4732, 1.4859, 1.4985,1.5306] \ 100
}
discountCurve = parseMktData(discountCurveDict)

// 4. Implied Dividend Curve
// Using Call-Put Parity on the full matrices
dividendCurve = eqDividendCurveBuilder(
    referenceDate, termDates, "CallPutParity", ,
    callPrices, putPrices, strikes, spot, discountCurve, "Actual365"
)

print(dividendCurve)
```

### FuturesPrice

通过 FuturesPrice 方法构建一条沪深300股指（标的代码： 000300.SH）的股息曲线。

```
referenceDate = 2026.02.13
spot = 4660.41  // Close Price Of 000300.SH

// 1. Futures Price
termDates = [2026.02.24, 2026.03.20, 2026.06.22, 2026.09.18] // IF2602/03/06/09 Expiry Date
futPrices = [4650.6, 4639.6, 4601.2, 4540.4]  // Settlement Price

// 2. Discount Curve
// Data From https://www.chinamoney.com.cn/chinese/bkcurvuir/
terms = [1d, 1w, 2w, 3w, 1M, 2M, 3M, 6M, 9M, 1y, 18M, 2y, 3y]
dates = array(DATE, size(terms))
for(i in 0..(size(terms)-1)){
    dates[i] = transFreq(temporalAdd(referenceDate, terms[i]), "CFET", "right", "right")
}
discountCurveDict = {
    "mktDataType": "Curve",
    "curveType": "IrYieldCurve",
    "curveName": "CNY_FR_007",
    "referenceDate": referenceDate,
    "currency": "CNY",
    "dayCountConvention": "Actual365",
    "compounding": "Continuous",
    "interpMethod": "Linear",
    "extrapMethod": "Flat",
    "dates": dates,
    "values":[1.5577, 1.5247, 1.5181, 1.5181, 1.5195, 1.5216, 1.5167, 1.4964, 1.4758, 1.4732, 1.4859, 1.4985, 1.5306] \ 100
}
discountCurve = parseMktData(discountCurveDict)

//3. Build Dividend Curve
dividendCurve = eqDividendCurveBuilder(referenceDate, termDates, "FuturesPrice", futPrices,
    , , , spot, discountCurve, "Actual365", "HS300")
print(dividendCurve)
```

**相关函数**：parseMktData
