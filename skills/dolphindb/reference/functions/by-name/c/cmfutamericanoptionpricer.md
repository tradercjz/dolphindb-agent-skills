# cmFutAmericanOptionPricer

首发版本：3.00.5

## 语法

`cmFutAmericanOptionPricer(instrument, pricingDate, futPrice, discountCurve, volSurf,
[setting], [model], [method])`

## 详情

对商品期货美式期权进行定价。

## 参数

**instrument** INSTRUMENT 类型标量或向量 ，表示待定价的商品期货美式期权。商品期货美式期权所需的关键字段详见产品字段要求。

**pricingDate** DATE 类型标量或向量，表示定价日期。

**futPrice**  DOUBLE 类型标量或向量，表示标的期货的现价。

**domesticCurve** MKTDATA 类型（IrYieldCurve）的标量或向量，表示折现曲线。

**volSurf** MKTDATA 类型（VolatilitySurface）的标量或向量，表示波动率曲面。

**setting** 可选参数，一个字典，用于设置定价输出。包含以下 key：

* calcDelta：value 是布尔值，指定是否计算 delta
* calcGamma：value 是布尔值，指定是否计算 gamma
* calcVega：value 是布尔值，指定是否计算 vega
* calcTheta：value 是布尔值，指定是否计算 theta
* calcRho：value 是布尔值，指定是否计算 rho

**model** 可选参数，STRING 类型标量，表示使用的模型。可选值为：

* “Black76”：Black76 公式
* “BAW”（默认值）：Barone-Adesi-Whaley公式
* “AmericanBinomialTree”：美式二叉树定价模型

**method** 可选参数，STRING 类型标量，表示使用的方法。可选值为：

* “Analytic”（默认值）：解析法
* “Tree”：树方法，支持 *model* 为 AmericanBinomialTree

## 返回值

* 当未指定 *setting* 时：返回 DOUBLE 类型标量，表示期权的净现值（NPV）。
* 当指定 *setting* 时：返回一个字典，包含 NPV 及按 *setting* 指定的 Greeks 结果。

## 例子

```
// ================================================================
// AUTO-GENERATED DolphinDB Script
// Function   : cmFutAmericanOptionPricer  商品期货美式期权定价示例
// Underlying : 上海期货交易所铜期货期权（cu）
// PricingDate: 2026-02-13
//
// 数据来源:
//   期货结算价  : akshare get_futures_daily(market='SHFE')
//   期权结算价  : akshare option_hist_shfe('铜期权', '20260213')
//   利率曲线    : 中国货币网 外币隐含利率曲线（CNY, USD.CNY/Shibor/掉期点）
//                https://www.chinamoney.com.cn/chinese/bkcurvuiruuh/
//                API: POST /ags/ms/cm-u-bk-fx/IuirCurvHis  2026-02-13
//
// 定价标的    : CU2605 铜期货美式看涨 Call
//               strike=102000  opt_expiry=2026-04-24
//               fut_price=101230
// ================================================================

pricingDate   = 2026.02.13
referenceDate = pricingDate

// ------------------------------------------------------------------
// 1. 折现曲线 (CNY_FR_007) ── 中国货币网外币隐含利率曲线
//    数据源: https://www.chinamoney.com.cn/chinese/bkcurvuiruuh/
//    USD.CNY / Shibor / 即期询价报价均值 / 掉期点  →  rmbRateStr 字段
// ------------------------------------------------------------------
discountCurveDict = {
    "mktDataType"       : "Curve",
    "curveType"         : "IrYieldCurve",
    "referenceDate"     : referenceDate,
    "currency"          : "CNY",
    "dayCountConvention": "Actual365",
    "compounding"       : "Continuous",
    "interpMethod"      : "Linear",
    "extrapMethod"      : "Flat",
    "frequency"         : "Annual",
    "dates"             : [referenceDate + 1, referenceDate + 7, referenceDate + 14, referenceDate + 21, referenceDate + 30, referenceDate + 61, referenceDate + 91, referenceDate + 182, referenceDate + 273, referenceDate + 365, referenceDate + 547, referenceDate + 730, referenceDate + 1095],
    "values"            : [0.016134, 0.016107, 0.016102, 0.016102, 0.016102, 0.016103, 0.016029, 0.015832, 0.015889, 0.015898, 0.015561, 0.015583, 0.015892],
    "name"              : "CNY_FR_007"
}
discountCurve = parseMktData(discountCurveDict)

// ------------------------------------------------------------------
// 2. 期货价格曲线 (AssetPriceCurve)
//    各到期月份铜期货结算价
// ------------------------------------------------------------------
futPriceCurveDict = {
    "mktDataType" : "Curve",
    "curveType"   : "AssetPriceCurve",
    "referenceDate": referenceDate,
    "currency"    : "CNY",
    "asset"       : "CU",
    "interpMethod": "Linear",
    "extrapMethod": "Flat",
    "dates"       : [2026.04.15, 2026.05.15, 2026.06.15, 2026.07.15, 2026.08.17, 2026.09.15],
    "values"      : [100980.0, 101230.0, 101240.0, 101100.0, 101230.0, 101250.0]
}
futPriceCurve = parseMktData(futPriceCurveDict)

// ------------------------------------------------------------------
// 3. 期权市场数据 ── 构建波动率曲面
//    到期日数: 6
//    使用虚值期权: K < F → Put, K >= F → Call
// ------------------------------------------------------------------
optionExpiries = [2026.03.25, 2026.04.24, 2026.05.25, 2026.06.24, 2026.07.27, 2026.08.25]
futMaturities  = [2026.04.15, 2026.05.15, 2026.06.15, 2026.07.15, 2026.08.17, 2026.09.15]

strikes = [
    [82000, 84000, 86000, 88000, 90000, 92000, 94000, 96000, 98000, 100000, 102000, 104000, 106000, 108000, 110000, 112000, 114000, 116000, 118000, 120000],
    [82000, 84000, 86000, 88000, 90000, 92000, 94000, 96000, 98000, 100000, 102000, 104000, 106000, 108000, 110000, 112000, 114000, 116000, 118000, 120000],
    [82000, 84000, 86000, 88000, 90000, 92000, 94000, 96000, 98000, 100000, 102000, 104000, 106000, 108000, 110000, 112000, 114000, 116000, 118000, 120000],
    [82000, 84000, 86000, 88000, 90000, 92000, 94000, 96000, 98000, 100000, 102000, 104000, 106000, 108000, 110000, 112000, 114000, 116000, 118000, 120000],
    [82000, 84000, 86000, 88000, 90000, 92000, 94000, 96000, 98000, 100000, 102000, 104000, 106000, 108000, 110000, 112000, 114000, 116000, 118000, 120000],
    [82000, 84000, 86000, 88000, 90000, 92000, 94000, 96000, 98000, 100000, 102000, 104000, 106000, 108000, 110000, 112000, 114000, 116000, 118000, 120000]
]

optionPrices = [
    [118, 208, 344, 544, 826, 1204, 1702, 2322, 3078, 3986, 4012, 3192, 2506, 1946, 1490, 1124, 836, 612, 442, 316],
    [396, 580, 826, 1144, 1552, 2052, 2652, 3360, 4178, 5108, 5382, 4536, 3792, 3146, 2590, 2114, 1718, 1388, 1114, 886],
    [828, 1112, 1464, 1888, 2392, 2980, 3660, 4440, 5312, 6276, 6570, 5712, 4950, 4276, 3672, 3132, 2664, 2264, 1908, 1596],
    [1218, 1566, 1980, 2474, 3048, 3702, 4432, 5240, 6142, 7138, 7308, 6450, 5696, 5006, 4370, 3820, 3324, 2870, 2490, 2146],
    [2054, 2508, 3014, 3614, 4272, 4986, 5792, 6666, 7586, 8616, 8924, 8076, 7304, 6566, 5926, 5306, 4768, 4258, 3808, 3390],
    [1938, 2374, 2876, 3460, 4104, 4804, 5608, 6472, 7386, 8410, 8734, 7886, 7116, 6378, 5742, 5132, 4592, 4094, 3644, 3240]
]

payoffTypes = [
    ["Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Call", "Call", "Call", "Call", "Call", "Call", "Call", "Call", "Call", "Call"],
    ["Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Call", "Call", "Call", "Call", "Call", "Call", "Call", "Call", "Call", "Call"],
    ["Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Call", "Call", "Call", "Call", "Call", "Call", "Call", "Call", "Call", "Call"],
    ["Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Call", "Call", "Call", "Call", "Call", "Call", "Call", "Call", "Call", "Call"],
    ["Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Call", "Call", "Call", "Call", "Call", "Call", "Call", "Call", "Call", "Call"],
    ["Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Call", "Call", "Call", "Call", "Call", "Call", "Call", "Call", "Call", "Call"]
]

// ------------------------------------------------------------------
// 4. 构建波动率曲面 ── BAW 公式 + SVI 模型
//    使用 BAW 公式计算美式期权隐含波动率
// ------------------------------------------------------------------
volSurf = cmFutVolatilitySurfaceBuilder(
    referenceDate, futMaturities, optionExpiries,
    strikes, optionPrices, payoffTypes,
    discountCurve, futPriceCurve,
    formula="BAW", model="SVI",
    surfaceName="cu_vol_surface_20260213"
)
print(volSurf)

// ------------------------------------------------------------------
// 5. 定义定价合约 ── 铜期货美式看涨期权
//    标的: CU2605  行权价: 102000  到期: 2026-04-24
// ------------------------------------------------------------------
cmFutAmericanOption = {
    "productType"       : "Option",
    "optionType"        : "AmericanOption",
    "assetType"         : "CmFutAmericanOption",
    "instrumentId"      : "CU2605C102000",
    "notionalAmount"    : 5.0,
    "notionalCurrency"  : "CNY",
    "strike"            : 102000.0,
    "maturity"          : 2026.04.24,
    "payoffType"        : "Call",
    "dayCountConvention": "Actual365",
    "underlying"        : "CU2605",
    "domesticCurve"     : "CNY_FR_007"
}
instrument = parseInstrument(cmFutAmericanOption)

// ------------------------------------------------------------------
// 6. 定价 ── 单合约 NPV (BAW 模型)
// ------------------------------------------------------------------
spot = 101230.0
npv = cmFutAmericanOptionPricer(instrument, pricingDate, spot, discountCurve, volSurf, model="BAW")
print("NPV = " + string(npv))

// ------------------------------------------------------------------
// 7. 定价 ── 含希腊字母 (Greeks)
// ------------------------------------------------------------------
setting = {
    "calcDelta" : true,
    "calcGamma" : true,
    "calcVega"  : true,
    "calcTheta" : true,
    "calcRho"   : true
}
result = cmFutAmericanOptionPricer(instrument, pricingDate, spot, discountCurve, volSurf, setting, model="BAW")
print(result)

// ------------------------------------------------------------------
// 8. 批量定价 ── 对 CU2605 到期的多个行权价 Call 合约定价
// ------------------------------------------------------------------
allStrikes = [82000, 84000, 86000, 88000, 90000, 92000, 94000, 96000, 98000, 100000, 102000, 104000, 106000, 108000, 110000, 112000, 114000, 116000, 118000, 120000]
results = array(DOUBLE, 0)
for (k in allStrikes) {
    iDict = {
        "productType"       : "Option",
        "optionType"        : "AmericanOption",
        "assetType"         : "CmFutAmericanOption",
        "instrumentId"      : "CU2605C" + string(int(k)),
        "notionalAmount"    : 5.0,
        "notionalCurrency"  : "CNY",
        "strike"            : k,
        "maturity"          : 2026.04.24,
        "payoffType"        : "Call",
        "dayCountConvention": "Actual365",
        "underlying"        : "CU2605",
        "domesticCurve"     : "CNY_FR_007"
    }
    iOpt = parseInstrument(iDict)
    results.append!(cmFutAmericanOptionPricer(iOpt, pricingDate, spot, discountCurve, volSurf, model="BAW"))
}
t = table(allStrikes as strike, results as npv)
print(t)
```

## 产品字段说明

| 字段名 | 类型 | 描述 | 是否必填 |
| --- | --- | --- | --- |
| productType | STRING | 固定填 "Option" | 是 |
| optionType | STRING | 固定填 "AmericanOption" | 是 |
| assetType | STRING | 固定填 "CmFutAmericanOption" | 是 |
| notionalAmount | DOUBLE | 名义本金额 | 是 |
| notionalCurrency | STRING | 名义本金货币 | 是 |
| instrumentId | STRING | 合约代码，标准格式为：标的期货合约代码+合约到期月份+期权类型代码+行权价格，如白糖期权为 SR2509P6300 = SR+2509+P+6300 | 否 |
| direction | SRTRING | 买卖方向，可选值为 Buy，Sell。默认值为 Buy。 | 否 |
| maturity | DATE | 到期日 | 是 |
| strike | DOUBLE | 执行利率 | 是 |
| payoffType | STRING | 收益类型，可选 Call 和 Put | 是 |
| underlying | STRING | 标的期货合约代码，如 SR2509 | 是 |
| dayCountConvention | STRING | 日期计数惯例, 可选 "ActualActualISDA", "ActualActualISMA", "Actual365", "Actual360" | 是 |
| discountCurve | STRING | 定价时参考的贴现曲线名称，人民币存款默认为 "CNY\_FR\_007" | 否 |

**相关函数：**
parseInstrument、parseMktData、cmFutVolatilitySurfaceBuilder
