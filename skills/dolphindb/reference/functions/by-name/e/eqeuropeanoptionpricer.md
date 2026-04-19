# eqEuropeanOptionPricer

首发版本：3.00.5

## 语法

`eqEuropeanOptionPricer(instrument, pricingDate, spot, discountCurve,
dividendCurve, volSurf, [setting])`

## 详情

对权益类欧式期权进行定价。

## 参数

**instrument** INSTRUMENT 类型标量或向量，表示需要定价的权益类欧式期权。字段要求参考 Instrument 字段说明。

**pricingDate** DATE 类型标量或向量，表示定价日期。

**spot** 数值类型标量或向量，表示现货价格。

**discountCurve** MKTDATA 标量或向量，表示折现曲线（IrYieldCurve）。

**dividendCurve** MKTDATA 标量或向量，表示股息曲线（DividendCurve）。该曲线通过
`eqDividendCurveBuilder` 构建。

**volSurf** VolatilitySurface 对象，表示权益类期权波动率曲面。该曲面由
`eqVolatilitySurfaceBuilder` 构建。

**setting** 可选参数，字典（Dictionary<STRING,
BOOL>），用于指定是否计算希腊字母（Greeks）所代表的期权价格敏感性指标。可选值：

| 键 | 值 | 描述 |
| --- | --- | --- |
| calcDelta | 布尔值，默认为 false | 是否计算 Delta，即期权价格相对于标的资产价格的敏感性。 |
| calcGamma | 布尔值，默认为 false | 是否计算 Gamma，即期权 Delta 相对于标的资产价格的敏感性。 |
| calcVega | 布尔值，默认为 false | 是否计算 Vega，即期权价格相对于标的资产波动率的敏感性。 |
| calcTheta | 布尔值，默认为 false | 是否计算 Theta，即期权价格相对于时间变化的敏感性。 |
| calcRhoIr | 布尔值，默认为 false | 是否计算 RhoIr，即期权价格相对于无风险利率的敏感性。 |
| calcRhoDividend | 布尔值，默认为 false | 是否计算 RhoDividend，即期权价格相对于股息收益率变化的敏感性。 |

## 返回值

* 若不指定 *setting* 参数，返回 DOUBLE 类型标量，表示期权的净现值（NPV），即期权的理论价格。
* 指定 *setting* 参数时，返回一个字典（Dictionary<STRING,
  DOUBLE>），包含期权的净现值（NPV）以及希腊字母（Greeks）所代表的期权价格敏感性指标。有关敏感性指标的说明请参考 *setting*
  参数说明。

## 例子

```
// ================================================================
// 数据来源:
//   现货价格  : akshare fund_etf_hist_sina('sh510050')     → 3.1140
//   期权链/IV : akshare option_risk_indicator_sse('20260213')
//               → Black-Scholes 重建期权结算价
//   利率曲线  : 中国货币网 外币隐含利率曲线（CNY, USD.CNY/Shibor/掉期点）
//               https://www.chinamoney.com.cn/chinese/bkcurvuiruuh/
//               API: POST /ags/ms/cm-u-bk-fx/IuirCurvHis  2026-02-13
//
// 定价标的  : 看涨 Call  strike=3.2000  expiry=2026-03-25
// ================================================================

pricingDate   = 2026.02.13
referenceDate = pricingDate

// ------------------------------------------------------------------
// 1. 现货价格
// ------------------------------------------------------------------
spot = 3.1140

// ------------------------------------------------------------------
// 2. 定义定价合约  (近月 ATM/轻虚值看涨期权)
// ------------------------------------------------------------------
optionDict = {
    "productType"       : "Option",
    "optionType"        : "EuropeanOption",
    "assetType"         : "EqEuropeanOption",
    "notionalCurrency"  : "CNY",
    "notionalAmount"    : 10000,
    "strike"            : 3.2000,
    "maturity"          : 2026.03.25,
    "payoffType"        : "Call",
    "dayCountConvention": "Actual365",
    "underlying"        : "510050"
}
option = parseInstrument(optionDict)

// ------------------------------------------------------------------
// 3. 期权链原始数据  (用于构建股息曲线与波动率曲面)
//    到期日序列: 2026.02.25 | 2026.03.25 | 2026.06.24 | 2026.09.23
//    行权价区间: [2.85, 3.60]
// ------------------------------------------------------------------
termDates = [2026.02.25, 2026.03.25, 2026.06.24, 2026.09.23]

callPrices = matrix(
    [0.2655, 0.2155, 0.1656, 0.1156, 0.0318, 0.0039, 0.0015, 0.0008, 0.0003, 0.0001],
    [0.2690, 0.2248, 0.1770, 0.1385, 0.0697, 0.0303, 0.0128, 0.0069, 0.0046, 0.0036],
    [0.3030, 0.2655, 0.2278, 0.1970, 0.1431, 0.0991, 0.0677, 0.0479, 0.0346, 0.0254],
    [0.3330, 0.2987, 0.2681, 0.2388, 0.1883, 0.1448, 0.1139, 0.0899, 0.0715, 0.0574]
)

putPrices = matrix(
    [0.0004, 0.0009, 0.0021, 0.0045, 0.0218, 0.0939, 0.1901, 0.2896, 0.3908, 0.4916],
    [0.0125, 0.0165, 0.0229, 0.0316, 0.0616, 0.1250, 0.2029, 0.2967, 0.3962, 0.4948],
    [0.0396, 0.0507, 0.0634, 0.0798, 0.1253, 0.1814, 0.2499, 0.3321, 0.4175, 0.5077],
    [0.0651, 0.0798, 0.0973, 0.1180, 0.1662, 0.2250, 0.2952, 0.3651, 0.4508, 0.5342]
)

strikes = matrix(
    [2.8500, 2.9000, 2.9500, 3.0000, 3.1000, 3.2000, 3.3000, 3.4000, 3.5000, 3.6000],
    [2.8500, 2.9000, 2.9500, 3.0000, 3.1000, 3.2000, 3.3000, 3.4000, 3.5000, 3.6000],
    [2.8500, 2.9000, 2.9500, 3.0000, 3.1000, 3.2000, 3.3000, 3.4000, 3.5000, 3.6000],
    [2.8500, 2.9000, 2.9500, 3.0000, 3.1000, 3.2000, 3.3000, 3.4000, 3.5000, 3.6000]
)

// ------------------------------------------------------------------
// 4. 折现曲线  ── 中国货币网 外币隐含利率曲线 CNY 利率（2026-02-13）
//    数据源: https://www.chinamoney.com.cn/chinese/bkcurvuiruuh/
//    USD.CNY / Shibor / 即期询价报价均值 / 掉期点  →  rmbRateStr 字段
// ------------------------------------------------------------------
discountCurveDict = {
    "mktDataType"       : "Curve",
    "curveType"         : "IrYieldCurve",
    "curveName"         : "CNY_FR_007",
    "referenceDate"     : referenceDate,
    "currency"          : "CNY",
    "dayCountConvention": "Actual365",
    "compounding"       : "Continuous",
    "interpMethod"      : "Linear",
    "extrapMethod"      : "Flat",
    "dates"             : [referenceDate + 1, referenceDate + 7, referenceDate + 14, referenceDate + 21, referenceDate + 30, referenceDate + 61, referenceDate + 91, referenceDate + 182, referenceDate + 273, referenceDate + 365, referenceDate + 547, referenceDate + 730, referenceDate + 1095],
    "values"            : [0.016134, 0.016107, 0.016102, 0.016102, 0.016102, 0.016103, 0.016029, 0.015832, 0.015889, 0.015898, 0.015561, 0.015583, 0.015892]
}
discountCurve = parseMktData(discountCurveDict)

// ------------------------------------------------------------------
// 5. 股息曲线  ── Call-Put 平价隐含法 (CallPutParity)
// ------------------------------------------------------------------
dividendCurve = eqDividendCurveBuilder(
    referenceDate, termDates, "CallPutParity", ,
    callPrices, putPrices, strikes, spot, discountCurve,
    "Actual365", "510050"
)

// ------------------------------------------------------------------
// 6. 波动率曲面  ── SABR 模型，使用虚值期权
//    行权价 < Spot → OTM Put；行权价 >= Spot → OTM Call
// ------------------------------------------------------------------
optionExpiries = termDates

optionPrices = matrix(
    [0.0004, 0.0009, 0.0021, 0.0045, 0.0218, 0.0039, 0.0015, 0.0008, 0.0003, 0.0001],
    [0.0125, 0.0165, 0.0229, 0.0316, 0.0616, 0.0303, 0.0128, 0.0069, 0.0046, 0.0036],
    [0.0396, 0.0507, 0.0634, 0.0798, 0.1253, 0.0991, 0.0677, 0.0479, 0.0346, 0.0254],
    [0.0651, 0.0798, 0.0973, 0.1180, 0.1662, 0.1448, 0.1139, 0.0899, 0.0715, 0.0574]
)

payoffTypes = matrix(
    ["Put", "Put", "Put", "Put", "Put", "Call", "Call", "Call", "Call", "Call"],
    ["Put", "Put", "Put", "Put", "Put", "Call", "Call", "Call", "Call", "Call"],
    ["Put", "Put", "Put", "Put", "Put", "Call", "Call", "Call", "Call", "Call"],
    ["Put", "Put", "Put", "Put", "Put", "Call", "Call", "Call", "Call", "Call"]
)

volSurface = eqVolatilitySurfaceBuilder(
    referenceDate,
    optionExpiries,
    strikes,
    optionPrices,
    payoffTypes,
    spot,
    discountCurve,
    dividendCurve,
    "SABR",
    "50ETF_SABR_20260213"
)

// ------------------------------------------------------------------
// 7. 定价 ── 单合约 NPV
// ------------------------------------------------------------------
npv = eqEuropeanOptionPricer(option, pricingDate, spot, discountCurve, dividendCurve, volSurface)
print("NPV = " + string(npv))

// ------------------------------------------------------------------
// 8. 定价 ── 含希腊字母 (Greeks)
// ------------------------------------------------------------------
setting = {
    "calcDelta"      : true,
    "calcGamma"      : true,
    "calcVega"       : true,
    "calcTheta"      : true,
    "calcRhoIr"      : true,
    "calcRhoDividend": true
}
result = eqEuropeanOptionPricer(option, pricingDate, spot, discountCurve, dividendCurve, volSurface, setting)
print(result)

// ------------------------------------------------------------------
// 9. 批量定价 ── 对 2026-03-25 到期的全部公共行权价 Call 合约
// ------------------------------------------------------------------
allStrikes = [2.8500, 2.9000, 2.9500, 3.0000, 3.1000, 3.2000, 3.3000, 3.4000, 3.5000, 3.6000]
results = array(DOUBLE, 0)
for (k in allStrikes) {
    iDict = {
        "productType"       : "Option",
        "optionType"        : "EuropeanOption",
        "assetType"         : "EqEuropeanOption",
        "notionalCurrency"  : "CNY",
        "notionalAmount"    : 10000,
        "strike"            : k,
        "maturity"          : 2026.03.25,
        "payoffType"        : "Call",
        "dayCountConvention": "Actual365",
        "underlying"        : "510050"
    }
    iOpt = parseInstrument(iDict)
    results.append!(eqEuropeanOptionPricer(iOpt, pricingDate, spot, discountCurve, dividendCurve, volSurface))
}
t = table(allStrikes as strike, results as npv)
print(t)
```

## Instrument 字段说明

| 字段名 | 类型 | 描述 | 是否必填 |
| --- | --- | --- | --- |
| productType | STRING | 固定填 "Option" | 是 |
| optionType | STRING | 固定填 "EuropeanOption" | 是 |
| assetType | STRING | 固定填 “EqEuropeanOption" | 是 |
| notionalAmount | DOUBLE | 名义本金额 | 是 |
| notionalCurrency | STRING | 名义本金货币，默认为 CNY | 否 |
| instrumentId | STRING | 合约代码，如中证500ETF期权  510500C2512M04800 | 否 |
| direction | SRTRING | 买卖方向 Buy Sell，默认为 Buy | 否 |
| maturity | DATE | 到期日 | 是 |
| strike | DOUBLE | 执行利率 | 是 |
| payoffType | STRING | 枚举，可选Call和Put | 是 |
| underlying | STRING | 标的期货合约代码，如 510050 | 是 |
| dayCountConvention | STRING | 日期计数惯例, 可选 "ActualActualISDA", "ActualActualISMA", "Actual365", "Actual360" | 是 |
| discountCurve | STRING | 定价时参考的贴现曲线名称，人民币存款默认为 "CNY\_FR\_007" | 否 |
| dividendCurve | STRING | 定价时参考的股息曲线名称 | 否 |

**相关函数：**parseInstrument、parseMktData、eqDividendCurveBuilder、eqVolatilitySurfaceBuilder
