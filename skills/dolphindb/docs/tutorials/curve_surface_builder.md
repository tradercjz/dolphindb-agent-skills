<!-- Auto-mirrored from upstream `documentation-main/tutorials/curve_surface_builder.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# FICC 曲线/曲面构建

## 1.前言

构建收益率曲线和期权波动率曲面是金融工程和定量分析的核心环节。它确保了定价的精确性、一致性，并为后续的风险管理和交易决策提供了坚实的基础。一个微小的曲线构建误差，可能会导致数百万甚至数亿的定价偏差或风险误判。​
随着市场的发展（如 LIBOR 向 SOFR 的过渡）和产品的复杂化（如结构性产品），构建曲线/曲面的模型和技术也变得日益复杂和重要。

DolphinDB V3.00.4 推出四个市场数据构建函数：

| 函数名 | 模型 | 描述 |
| --- | --- | --- |
| bondYieldCurveBuilder | Bootstrap/NS/NSS | 债券收益率曲线构建 |
| irSingleCurrencyCurveBuilder | Bootstrap | 单货币利率互换曲线构建 |
| irCrossCurrencyCurveBuilder | Bootstrap | 交叉货币利率互换曲线构建（外币隐含利率曲线构建） |
| fxVolatilitySurfaceBuilder | SVI/SABR/Linear/CubicSpline | 外汇期权波动率曲面构建 |

下面分别对这四个函数进行详细说明。

## 2.债券收益率曲线构建

所有债券的定价和风险计量都需要用到即期曲线（零息利率曲线）。收益率曲线的形态（陡峭、平坦、倒挂）和其预期的变化，是衍生出众多交易策略的基础。这里，我们着重介绍债券收益率曲线构建（到期->即期）的方法。

### 2.1 Bootstrap

拨靴法（Bootstrap）是一个核心且经典的金融工程方法，用于从一系列市场上可交易的、无套利的债券价格中，推导出即期利率曲线。核心算法是从样本券中剩余期限最小的开始，根据样本券的到期收益率（YTM）报价，利用债券计算器
(bondCalculator) 得到债券全价（dirty），然后利用假设的即期曲线作为折现曲线对债券进行定价，得到理论价格
npv，不断调整即期利率，使得 npv 和 dirty
相等（误差小于阈值），即可得到该样本券剩余期限时间点对应的即期利率，依次类推，即可得到整条即期曲线。

这里，我们根据外汇交易中心（CFETS）2025 年 8 月份国债收益率曲线构建基准债券列表，选取 2025 年 8 月 18 日收盘数据，通过
Bootstrap 方法得到即期曲线（“Zero Rate” 列），并与 CFETS 即期曲线（“CFETS Zero Rate”
列）进行对比，发现最大误差为期限 20Y 的 0.4964 个 bp，所有期限误差均小于 0.5 个 bp。

![](images/curve_surface_builder/2_1.png)

### 2.2 Nelson-Siegel（NS）

Nelson-Siegel (NS) 模型最早由 Nelson 和 Siegel 于 1987 年提出，该模型适用于债券的利率期限结构分析。NS
模型中有四个参数，每个都有自身的经济含义，不同参数值能描述不同情境下的利率曲线的变动情况（参考[1]）。

NS 模型假定了瞬时远期利率的形式：

![](images/curve_surface_builder/formula2_2_1.svg)

该模型有四个参数 β0 , β1 , β2 , λ，其中 τ=T-t
是到期年限，λ>0。

瞬时远期利率 f(t, T) 里面有三项：

* 第一项 β0 是当 τ 趋近无穷大时的远期利率，因此 β0= f(∞)。
* 第二项是个单调函数，当 β1> 0 时递减，当 β1 < 0 时递增。
* 第三项是个非单调函数，可以产生凸起（hump）。

当 τ 趋近零时，第二项趋近于 β1，第三项趋近于 0，因此 f(0) = β0 +
β1。

对瞬时远期利率求积分，可以得到即期利率的公式：（公式 1）

![](images/curve_surface_builder/formula2_2_2.svg)

这样容易看出：

* β0 的因子载荷是**常数**，对于对所有期限利率的影响是相同的，因此 β0
  可控制**利率水平**（level），它的变动会使得收益率曲线发生水平上下移动。
* β1 的因子载荷是**单调递减**，从1 很快的衰减到 0，这表明 β1
  对短端利率的影响较大，因此 β1 可控制**曲线斜率**（slope），影响着利率曲线的斜率程度。
* β2 的因子载荷**先增后减**，从 0 增到 1 再减到 0，这表明 β2
  对利率曲线的短端和长端影响较弱，对中端的影响较大，因此 β2 控制**曲线曲率**（curvature）。
* τ 是 β1 和 β2 的因子载荷的衰减速度，该值越大衰减越快。

NS模型构建即期曲线的过程首先是根据样本券的到期收益率（YTM）报价，利用债券计算器（bondCalculator）得到债券全价（dirty），然后利用假设的即期曲线（公式 1）作为折现曲线对债券进行定价，得到理论价格 npv
，n 个样本券可以得到 n 对 (dirty， npv)，最小化以下目标函数即可得到四个参数

![](images/curve_surface_builder/formula2_2_3.svg)

### 2.3 Nelson-Siegel-Svensson（NSS）

在 NS 基础上，Svensson 在 1994 年做了改进，为了能多模拟一个 hump
形状而增加了两个参数。该模型下的**瞬时远期利率**的形式为

![](images/curve_surface_builder/formula2_3_1.svg)

同时求积分我们可以得到其**即期利率**：

![](images/curve_surface_builder/formula2_3_2.svg)

NSS 模型构建即期曲线的过程跟 NS 模型类似 ，只是即期曲线的函数解析式不同，暂不赘述。

### 2.4 示例

```
// 以2025年8月18日的国债收益率曲线构建为例
bond1 = {
    "productType": "Cash",
    "assetType": "Bond",
    "bondType": "DiscountBond",
    "instrumentId": "259916.IB",
    "start": 2025.03.13,
    "maturity": 2025.09.11,
    "issuePrice":  99.2070,
    "dayCountConvention": "ActualActualISDA"
}
bond2 = {
    "productType": "Cash",
    "assetType": "Bond",
    "bondType": "FixedRateBond",
    "instrumentId": "240021.IB",
    "start": 2024.10.25,
    "maturity": 2025.10.25,
    "coupon": 0.0133,
    "frequency": "Annual",
    "dayCountConvention": "ActualActualISDA"
}
bond3 = {
    "productType": "Cash",
    "assetType": "Bond",
    "bondType": "FixedRateBond",
    "instrumentId": "250001.IB",
    "start": 2025.01.15,
    "maturity": 2026.01.15,
    "coupon": 0.0116,
    "frequency": "Annual",
    "dayCountConvention": "ActualActualISDA"
}
bond4 = {
    "productType": "Cash",
    "assetType": "Bond",
    "bondType": "FixedRateBond",
    "instrumentId": "250013.IB",
    "start": 2025.07.25,
    "maturity": 2026.07.25,
    "coupon": 0.0133,
    "frequency": "Annual",
    "dayCountConvention": "ActualActualISDA"
}
bond5 = {
    "productType": "Cash",
    "assetType": "Bond",
    "bondType": "FixedRateBond",
    "instrumentId": "250012.IB",
    "start": 2025.06.15,
    "maturity": 2027.06.15,
    "coupon": 0.0138,
    "frequency": "Annual",
    "dayCountConvention": "ActualActualISDA"
}
bond6 = {
    "productType": "Cash",
    "assetType": "Bond",
    "bondType": "FixedRateBond",
    "instrumentId": "250010.IB",
    "start": 2025.05.25,
    "maturity": 2028.05.25,
    "coupon": 0.0146,
    "frequency": "Annual",
    "dayCountConvention": "ActualActualISDA"
}

referenceDate = 2025.08.18
bondsTmp = [bond1, bond2, bond3, bond4, bond5, bond6]
bonds = parseInstrument(bondsTmp)
/*
此案例对标的是外汇交易中心，使用标准期限，各个样本券的剩余期限(term)和报价(quote)都是虚拟出来的
https://www.chinamoney.com.cn/chinese/bkcurvclosedyhis/index.html
*/
terms = [1M, 3M, 6M, 1y, 2y, 3y]
quotes=[1.3000, 1.3700, 1.3898, 1.3865, 1.4296, 1.4466]/100

// method = "BoostStarp"
bootstrapCurve = bondYieldCurveBuilder(referenceDate, `CNY, bonds, terms, quotes, "ActualActualISDA", method='Bootstrap')
bootstrapCurveDict = extractMktData(bootstrapCurve)
print(bootstrapCurveDict)

// method = "NS"
nsCurve = bondYieldCurveBuilder(referenceDate, `CNY, bonds, terms, quotes, "ActualActualISDA", method='NS')
nsCurveDict = extractMktData(nsCurve)
print(nsCurveDict)

// method = "NSS"
nssCurve = bondYieldCurveBuilder(referenceDate, `CNY, bonds, terms, quotes, "ActualActualISDA", method='NSS')
nssCurveDict=extractMktData(nssCurve)
print(nssCurveDict)
```

## 3. 单货币利率互换曲线构建

利率互换（IRS）是一种重要的金融衍生工具，它允许交易双方在约定时期内，根据​**​相同名义本金​**​和不同利率计算方式，​**​交换利息现金流​**​。这通常涉及固定利率与浮动利率的交换，但不交换本金。利率互换定价需要用到利率互换曲线，我们这里介绍单货币利率互换曲线构建，涉及到的金融工具包括：

* **存款利率 (Depo)：** 提供短期利率信息（如 1 天至 1 年）
* **远期利率协议 (FRA)：** 提供短期到中期的远期利率信息（如 3M-6M）
* **利率期货 (Futures)：** 提供中短期的隐含远期利率（如 3M-2Y）
* **利率互换 (Swaps)：** 提供中长期固定利率点（如 1Y-30Y）

![](images/curve_surface_builder/3_1.png)

### 3.1 Bootstrap

针对国内市场，我们选取的是 Depo 和 Swaps 作为构建工具，采用 Bootstrap 方法（算法请参考[2][3]）。这里仅展示 CNY\_FR\_007 和
CNY\_SHIBOR\_3M 两条曲线的构建结果。

![](images/curve_surface_builder/3_2.png)

我们以2021年5月26日数据为例，根据 CNY\_FR\_007 各个期限交易的报价(“Quote”列)，利用 Bootstrap 方法，得到即期曲线 (“Zero
Rate” 列) ，对比国内某大型机构的即期曲线（“Benchmark Zero Rate”），误差几乎为零。

![](images/curve_surface_builder/3_3.png)

我们以2021年5月26日数据为例，根据 CNY\_SHIBOR\_3M 各个期限交易的报价 (“Quote”列)，利用 Bootstrap
方法，得到即期曲线(“Zero Rate“列)，对比国内某大型机构的即期曲线（“Benchmark Zero Rate”），误差最大为 1M 期的
1.0539bp，其余期限误差均小于 0.5bp。

### 3.2 示例

例1. 构建一条以人民币计价、参考 FR\_007 浮动利率的利率互换曲线。

```
referenceDate = 2021.05.26
currency = "CNY"
terms = [7d, 1M, 3M, 6M, 9M, 1y, 2y, 3y, 4y, 5y, 7y, 10y]
instNames = take("CNY_FR_007", size(terms))
instNames[0] = "FR_007"
instTypes = take("IrVanillaSwap", size(terms))
instTypes[0] = "Deposit"
quotes = [2.3500, 2.3396, 2.3125, 2.3613, 2.4075, 2.4513, 2.5750, 2.6763, 2.7650, 2.8463, 2.9841, 3.1350]\100
dayCountConvention = "Actual365"
curve = irSingleCurrencyCurveBuilder(referenceDate, currency, instNames, instTypes, terms, quotes, dayCountConvention, curveName="CNY_FR_007")
curveDict = extractMktData(curve)
print(curveDict)
```

例2. 构建一条以人民币计价、参考 SHIBOR\_3M 浮动利率的利率互换曲线。

```
referenceDate = 2021.05.26
currency = "CNY"
terms = [1w, 2w, 1M, 3M, 6M, 9M, 1y, 2y, 3y, 4y, 5y, 7y, 10y]
instNames = take("CNY_SHIBOR_3M", size(terms))
instNames[0] = "SHIBOR_1W"
instNames[1] = "SHIBOR_2W"
instNames[2] = "SHIBOR_1M"
instNames[3] = "SHIBOR_3M"
instTypes = take("IrVanillaSwap", size(terms))
instTypes[0] = "Deposit"
instTypes[1] = "Deposit"
instTypes[2] = "Deposit"
instTypes[3] = "Deposit"
quotes = [2.269, 2.311, 2.405, 2.479, 2.6013, 2.7038,2.7725,
          2.9625, 3.11, 3.24, 3.3513, 3.5313, 3.7125]/100
dayCountConvention = "Actual365"
curve = irSingleCurrencyCurveBuilder(referenceDate, currency, instNames, instTypes, terms, quotes, dayCountConvention)
curveDict = extractMktData(curve)
print(curveDict)
```

## 4. 外币隐含利率曲线构建

在外汇产品的定价中，需要输入两种货币的即期曲线来分别表示各自的资金成本，所以构建外币的隐含利率曲线也是很重要的。 通常情况下，构建外币隐含利率曲线的金融工具有：

* **外汇掉期 (FxSwap)：** 提供短期利率信息
* **货币交叉互换 (CrossCurrencySwap)：** 提供中期到远期期的利率信息

### 4.1 Bootstrap

对于国内市场，我们全部采用 FxSwap 和外汇即期报价，通过利率平价公式，推导出外币的隐含利率曲线。根据远期汇率公式（以连续复利为例）：

![](images/curve_surface_builder/formula4_1_1.svg)

![](images/curve_surface_builder/formula4_1_2.svg)

其中 S1 为近端（即期）汇率，S2 为远端汇率，t 为掉期的期限，SwapPointt
为外汇掉期的报价，rd,t 为对应期限 t 的本币零息利率。根据上式即可推导出期限 t 对应的外币的零息利率
rf,t 。

这里展示一条美元隐含收益率曲线（USD\_USDCNY\_FX）的构建结果：

![](images/curve_surface_builder/4_1.png)

根据外汇交易中心提供的2025年8月18日 USDCNY 外汇掉期报价(“Quote” 列)、即期汇率和人民币即期利率曲线（“CNY Zero
Rate”列），利用利率平价公式，得到美元即期曲线（“Zero Rate” 列），对比外汇交易中心的美元即期曲线（“CFETS Zero
Rate”），误差几乎为零。

### 4.2 示例

```
// 以2025年8月18日的USDCNY美元隐含收益率曲线构建为例
refDate = 2025.08.18
spotDate1 = temporalAdd(refDate, 2, "XNYS")    //美元的即期日，其中“XNYS”为美国交易日历
spotDate2 = temporalAdd(refDate, 2, "CFET")   //人民币的即期日，其中“XNYS”为中国交易日历
spotDate = max(spotDate1, spotDate2)
instNames = take("USDCNY", 13)
instTypes = take("FxSwap", 13)
terms = ["1d", "1w", "2w", "3w", "1M", "2M", "3M", "6M", "9M", "1y", "18M", "2y", "3y"]
curveDates = array(DATE)
// 计算每个外汇掉期报价到期日，作为曲线的时间轴
for(term in terms){
    dur = duration(term)
    d1 = transFreq(temporalAdd(spotDate, dur), "XNYS", "right", "right")
    d2 = transFreq(temporalAdd(spotDate, dur), "CFET", "right", "right")
    curveDates.append!(max(d1, d2))
 }
quotes = [-5.54, -39.00, -75.40, -113.20, -177.00, -317.00, -466.00, -898.50,
         -1284.99, -1676.00, -2320.00, -2870.00, -3962.50] \ 10000  // fx swap points

curve = {
    "mktDataType": "Curve",
    "curveType": "IrYieldCurve",
    "referenceDate": refDate,
    "currency": "CNY",
    "dayCountConvention": "Actual365",
    "compounding": "Continuous",
    "interpMethod": "Linear",
    "extrapMethod": "Flat",
    "dates": curveDates,
    "values": [1.5113, 1.5402, 1.5660, 1.5574, 1.5556, 1.5655, 1.5703,
               1.5934, 1.6040, 1.6020, 1.5928, 1.5842, 1.6068] \ 100,
    "settlement": spotDate
}

cnyShibor3m = parseMktData(curve)

spot = 7.1627
curve = irCrossCurrencyCurveBuilder(refDate, "USD", instNames, instTypes, terms, quotes, "USDCNY", spot, "Actual365", cnyShibor3m, "Continuous")
curveDict = extractMktData(curve)
for(i in 0..(size(quotes)-1) ){
    print(curveDict["values"][i]*100)
}
```

## 5. 外汇期权波动率曲面构建

外汇期权定价需要用到波动率，而对于单个期权而言，其波动率需要按照自身的执行价和剩余期限从波动率曲面中插值出来。不同于其他资产对应期权的 strike-vol
报价，外汇期权报价采用 delta-vol 的形式，所以曲面构建的第一步就是 delta 转 strike， 转换过程如下：

```
//Step1：计算出单个期权对应的vol
sigma_25c = sigma_atm + bf_25 + 0.5 * rr_25   //delta = 0.25的vol
sigma_25p = sigma_atm + bf_25 - 0.5 * rr_25   //delta =-0.25的vol
sigma_10c = sigma_atm + bf_10 + 0.5 * rr_10   //delta = 0.10的vol
sigma_10p = sigma_atm + bf_10 - 0.5 * rr_10   //delta =-0.10的vol
/*
其中
sigma_atm：平值期权报价
bf_25：delta=0.25的碟式（Butterfly）期权报价
rr_25：delta=0.25的风险逆转（Risk Reversal）期权报价
bf_10：delta=0.10的碟式（Butterfly）期权报价
rr_10：delta=0.10的风险逆转（Risk Reversal）期权报价
*/

//Step2：根据Black-Scholes计算delta的公式反堆strike，这里不展开，请参考文献[5]
```

得到
strike-vol（smile）离散点之后，就可以根据以下模型构建波动率微笑了。由于线性插值（Linear）和三次样条插值（CubicSpline）构建波动率微笑比较简单，这里不展开，重点介绍
SVI 和 SABR 模型。

### 5.1 SVI（Stochastic Volatility Inspired）

SVI 模型由 Jim Gatheral 提出，通过总方差建模隐含波动率微笑：（公式 2）

![](images/curve_surface_builder/formula5_1_1.svg)

其中：

* ω(k)：总方差， 定义
  ω(k)=σ2imp×T，σ2imp
  为隐含波动率，T 为到期时间
* k：对数 moneyness，k=ln(K/F)，K 为行权价格，F 为远期汇率
* a：最小总方差，控制总方差的基准水平
* b：控制总方差的倾斜程度
* ρ：控制微笑的对称性（ρ∈[-1,1]），通常为负值
* m：对数 moneyness 的中心位置
* σ：控制微笑的宽带

公式 2 中的左边可以根据上一节 strike-vol 得到，strike 就是 k=ln(K/F) 的计算公式中的 K（F 可以根据远期汇率公式计算）， vol
就是 σimp 。定义目标函数

![](images/curve_surface_builder/formula5_1_3.svg)

可以采用 **Levenberg-Marquardt** 等算法最小化目标函数，求出五个参数，即可得到整个 smile 曲线上任意 strike 对应的
vol。

### 5.2 SABR（Stochastic Alpha Beta Rho）

SABR 模型的隐含波动率近似公式为：

![](images/curve_surface_builder/formula5_2_1.svg)

其中：

* IV(K)：行权价格 K 对应的隐含波动率
* α：初始波动率，控制波动率水平
* β：控制波动率对标的价格的敏感性，取值范围为 [0,1]
* ρ：标的资产价格与波动率之间的相关性
* υ：波动率的波动率（vol-of-vol）
* K ：行权价格
* F ：远期汇率
* T ：到期时间

定义目标函数 ![](images/curve_surface_builder/formula5_2_2.svg) 采用 **Levenberg-Marquardt**等算法最小化目标函数，求出四个参数，即可得到整个 smile 曲线上任意 strike 对应的 vol。

### 5.3 示例

![](images/curve_surface_builder/5_1.png)

![](images/curve_surface_builder/5_2.png)

![](images/curve_surface_builder/5_3.png)

以外汇交易中心 2025 年 8 月 18 日数据为例，选取 USDCNY 外汇期权 delta 报价矩阵为参数，SVI
模型拟合波动率微笑，得到了外汇波动率曲面，该曲面可用作外汇期权的定价。

```
refDate = 2025.08.18
ccyPair = "USDCNY"
quoteTerms = ['1d', '1w', '2w', '3w', '1M', '2M', '3M', '6M', '9M', '1y', '18M', '2y', '3y']
quoteNames = ["ATM", "D25_RR", "D25_BF", "D10_RR", "D10_BF"]
quotes = [0.030000, -0.007500, 0.003500, -0.010000, 0.005500,
          0.020833, -0.004500, 0.002000, -0.006000, 0.003800,
          0.022000, -0.003500, 0.002000, -0.004500, 0.004100,
          0.022350, -0.003500, 0.002000, -0.004500, 0.004150,
          0.024178, -0.003000, 0.002200, -0.004750, 0.005500,
          0.027484, -0.002650, 0.002220, -0.004000, 0.005650,
          0.030479, -0.002500, 0.002400, -0.003500, 0.005750,
          0.035752, -0.000500, 0.002750,  0.000000, 0.006950,
          0.038108,  0.001000, 0.002800,  0.003000, 0.007550,
          0.039492,  0.002250, 0.002950,  0.005000, 0.007550,
          0.040500,  0.004000, 0.003100,  0.007000, 0.007850,
          0.041750,  0.005250, 0.003350,  0.008000, 0.008400,
          0.044750,  0.006250, 0.003400,  0.009000, 0.008550]
quotes = reshape(quotes, size(quoteNames):size(quoteTerms)).transpose()
spot = 7.1627
curveDates = [2025.08.21, 2025.08.27, 2025.09.03, 2025.09.10, 2025.09.22, 2025.10.20,
  2025.11.20, 2026.02.24,2026.05.20, 2026.08.20, 2027.02.22, 2027.08.20, 2028.08.21]
domesticCurveInfo = {
    "mktDataType": "Curve",
    "curveType": "IrYieldCurve",
    "referenceDate": refDate,
    "currency": "CNY",
    "dayCountConvention": "Actual365",
    "compounding": "Continuous",
    "interpMethod": "Linear",
    "extrapMethod": "Flat",
    "frequency": "Annual",
    "dates": curveDates,
    "values":[1.5113, 1.5402, 1.5660, 1.5574, 1.5556, 1.5655, 1.5703,
              1.5934, 1.6040, 1.6020, 1.5928, 1.5842, 1.6068]/100
}
foreignCurveInfo = {
    "mktDataType": "Curve",
    "curveType": "IrYieldCurve",
    "referenceDate": refDate,
    "currency": "USD",
    "dayCountConvention": "Actual365",
    "compounding": "Continuous",
    "interpMethod": "Linear",
    "extrapMethod": "Flat",
    "frequency": "Annual",
    "dates": curveDates,
    "values":[4.3345, 4.3801, 4.3119, 4.3065, 4.2922, 4.2196, 4.1599,
              4.0443, 4.0244, 3.9698, 3.7740, 3.6289, 3.5003]/100
}
domesticCurve = parseMktData(domesticCurveInfo)
foreignCurve = parseMktData(foreignCurveInfo)
surf = fxVolatilitySurfaceBuilder(refDate, ccyPair, quoteNames, quoteTerms, quotes, spot, domesticCurve, foreignCurve)
surfDict = extractMktData(surf)
print(surfDict)
```

## 6. 工具函数

### 6.1 curvePredict

构建好曲线之后，我们可以通过 curvePredict 函数获取任意时间的曲线值。

```
curveDict = {
    "mktDataType": "Curve",
    "curveType": "IrYieldCurve",
    "referenceDate": 2025.08.18,
    "currency": "CNY",
    "dayCountConvention": "ActualActualISDA",
    "compounding": "Continuous",
    "interpMethod": "Linear",
    "extrapMethod": "Flat",
    "frequency": "Annual",
    "dates": [2025.08.21, 2025.08.27, 2025.09.03, 2025.09.10, 2025.09.22, 2025.10.20,
     2025.11.20, 2026.02.24, 2026.05.20, 2026.08.20, 2027.02.22,2027.08.20, 2028.08.21],
    "values":[1.5113, 1.5402, 1.5660, 1.5574, 1.5556, 1.5655, 1.5703,
              1.5934, 1.6040, 1.6020, 1.5928, 1.5842, 1.6068]/100
}

curve = parseMktData(curveDict)
curvePredict(curve, 2025.10.18)
// output: 0.0156
curvePredict(curve, 1.0)
// output: 0.0160
curvePredict(curve, [2025.10.18, 2026.10.18])
// output: [0.0156,0.0159]
curvePredict(curve, [1.0, 2.0])
// output: [0.0160,0.0158]
```

### 6.2 optionVolPredict

波动率曲面是一个三维曲面，我们可以通过 optionVolPredict 获取指定时间和执行价时曲面上的波动率。

```
refDate = 2025.08.18
ccyPair = "USDCNY"
quoteTerms = ['1d', '1w', '2w', '3w', '1M', '2M', '3M', '6M', '9M', '1y', '18M', '2y', '3y']
quoteNames = ["ATM", "D25_RR", "D25_BF", "D10_RR", "D10_BF"]
quotes = [0.030000, -0.007500, 0.003500, -0.010000, 0.005500,
          0.020833, -0.004500, 0.002000, -0.006000, 0.003800,
          0.022000, -0.003500, 0.002000, -0.004500, 0.004100,
          0.022350, -0.003500, 0.002000, -0.004500, 0.004150,
          0.024178, -0.003000, 0.002200, -0.004750, 0.005500,
          0.027484, -0.002650, 0.002220, -0.004000, 0.005650,
          0.030479, -0.002500, 0.002400, -0.003500, 0.005750,
          0.035752, -0.000500, 0.002750,  0.000000, 0.006950,
          0.038108,  0.001000, 0.002800,  0.003000, 0.007550,
          0.039492,  0.002250, 0.002950,  0.005000, 0.007550,
          0.040500,  0.004000, 0.003100,  0.007000, 0.007850,
          0.041750,  0.005250, 0.003350,  0.008000, 0.008400,
          0.044750,  0.006250, 0.003400,  0.009000, 0.008550]

quotes = reshape(quotes, size(quoteNames):size(quoteTerms)).transpose()

spot = 7.1627
curveDates = [2025.08.21, 2025.08.27, 2025.09.03, 2025.09.10, 2025.09.22, 2025.10.20,
  2025.11.20, 2026.02.24, 2026.05.20, 2026.08.20, 2027.02.22, 2027.08.20, 2028.08.21]

domesticCurveInfo = {
    "mktDataType": "Curve",
    "curveType": "IrYieldCurve",
    "referenceDate": refDate,
    "currency": "CNY",
    "dayCountConvention": "Actual365",
    "compounding": "Continuous",
    "interpMethod": "Linear",
    "extrapMethod": "Flat",
    "frequency": "Annual",
    "dates": curveDates,
    "values":[1.5113, 1.5402, 1.5660, 1.5574, 1.5556, 1.5655, 1.5703,
              1.5934, 1.6040, 1.6020, 1.5928, 1.5842, 1.6068]/100
}
foreignCurveInfo = {
    "mktDataType": "Curve",
    "curveType": "IrYieldCurve",
    "referenceDate": refDate,
    "currency": "USD",
    "dayCountConvention": "Actual365",
    "compounding": "Continuous",
    "interpMethod": "Linear",
    "extrapMethod": "Flat",
    "frequency": "Annual",
    "dates": curveDates,
    "values":[4.3345, 4.3801, 4.3119, 4.3065, 4.2922, 4.2196, 4.1599,
              4.0443, 4.0244, 3.9698, 3.7740, 3.6289, 3.5003]/100
}

domesticCurve = parseMktData(domesticCurveInfo)
foreignCurve = parseMktData(foreignCurveInfo)

surf = fxVolatilitySurfaceBuilder(refDate, ccyPair, quoteNames, quoteTerms, quotes, spot, domesticCurve, foreignCurve)

optionVolPredict(surf, 2025.10.18, 7)
/* output:
           7
           -----------------
2025.10.18|0.035427722673281
*/
optionVolPredict(surf, 2025.10.18, [7.1,7.2])
/* output:
           7.1               7.2
           ----------------- -----------------
2025.10.18|0.029466799513362 0.029268084254983
*/
optionVolPredict(surf, [2025.10.18, 2026.10.18], 7)
/* output:
           7
           -----------------
2025.10.18|0.035427722673281
2026.10.18|0.040453528763062
*/
optionVolPredict(surf, [2025.10.18, 2026.10.18], [7.1, 7.2])
/* output:
           7.1               7.2
           ----------------- -----------------
2025.10.18|0.029466799513362 0.029268084254983
2026.10.18|0.042188693924168 0.044408563755123
*/
```

## 7. 总结与展望

本教程展示了部分利率曲线和外汇期权波动率曲面的构建理论和方法，并用 DolphinDB 内置函数逐一进行了
使用说明，结果和相关基准进行了对比，同时提供了工具函数方便用户使用。

后续我们会在两个方面不断迭代与更新：

* 增加更多的曲线/曲面构建函数，比如商品远期曲线、CDS 信用利差曲线、商品期权波动率曲面等
* 同一个函数增加更多的标的品种，比如单货币利率互换曲线构建函数（irSingleCurrencyCurveBuilder）目前仅支持 CNY\_FR\_007 和
  CNY\_SHIBOR\_3M，后续会增加 USD\_SOFR / EUR\_ESTR 等曲线

收益率曲线和波动率曲面构建是金融工程的核心功能，这些中间市场数据不仅是定价和风控的前提，也为众多量化策略（参考[6]）提供了帮助。随着中国金融市场的不断崛起，我们会紧跟市场，提供更多的金融工程函数来服务客户，敬请期待！

## 参考

[1] [债券收益率曲线构建](https://mp.weixin.qq.com/s/_3t78s8dY2GnGhvVj2rY7Q?from=industrynews&color_scheme=light)

[2][『曲线构建系列 1』单曲线方法](https://mp.weixin.qq.com/s?__biz=MzIzMjY0MjE1MA==&mid=2247487968&idx=1&sn=9f53f23c280281699a00688622664626&chksm=e89092e9dfe71bff7d8bc6990b393d9f8ca0688052e71f054f61bab911ba6d3b08d77dc8b5d3&scene=21#wechat_redirect)

[3] F. Ametrano and M. Bianchetti. Everything you always wanted to know about
Multiple In terest Rate Curve Bootstrapping but were afraid to ask (April 2, 2013).
Available at SSRN: [Everything You Always Wanted to Know About Multiple Interest
Rate Curve Bootstrapping but Were Afraid to Ask](http://ssrn.com/abstract%3D2219548) or [Everything You Always Wanted to Know About Multiple Interest Rate Curve
Bootstrapping but Were Afraid to Ask](http://dx.doi.org/10.2139/ssrn.2219548) , 2013.

[4] Reiswich, D., & Wystup, U. (2010). FX Volatility Smile Construction. *CPQF
Working Paper Series, No. 20*. Frankfurt School of Finance &
Management.

[5] Clark, I. J. (2011). *Foreign exchange option pricing: A practitioner's
guide*. Chichester, West Sussex, PO19 8SQ, United Kingdom: John Wiley &
Sons Ltd.

[6] 徐寒飞. 债券量化研究系列专题之二：收益率曲线交易[R]. 广州: 广发证券股份有限公司, 2013-01-08.

## 附录

[curve\_volsurf\_builder.dos](script/curve_surface_builder/curve_volsurf_builder.dos)
