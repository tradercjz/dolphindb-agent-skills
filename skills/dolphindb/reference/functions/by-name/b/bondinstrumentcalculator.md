# bondInstrumentCalculator

首发版本：3.00.4.1

## 语法

`bondInstrumentCalculator(bond, settlement, price, priceType,
[calcRisk=false], [benchmark='Qeubee'], [isExercised])`

## 详情

债券计算器，实现债券价格 (ytm / cleanPrice / dirtyPrice) 三者互算，同时计算久期、凸度等风险指标。

## 参数

**bond** INSTRUMENT 类型标量或向量，表示债券金融工具。

注：

bond instrument 的
instrumentId 字段如果指定了后缀，且后缀为 .SH 或者 .SZ， 则债券会被视为交易所债券，它的应计利息计算会增加一天。

**settlement** DATE 类型标量或向量，表示债券的结算日，即购买日期。

**price** 数值型标量或向量，具体含义取决于 priceType 的取值：

* 当 *priceType* 为 "YTM" 时，*price* 表示债券的到期收益率；
* 当 *priceType* 为 "CleanPrice" 时，*price* 表示债券的净价；
* 当 *priceType* 为 "DirtyPrice" 时，*price* 表示债券的全价。
* 当 *priceType* 为 "YTE" 时，*price* 表示债券的行权收益率。

**priceType** STRING 类型的标量或向量，用于指定债券价格类型，可选值为：

* "YTM"：到期收益率
* "CleanPrice"：净价
* "DirtyPrice"：全价
* "YTE"：行权收益率，仅在 bond 为 OptionBond 时可用。

**calcRisk** 可选参数，布尔值，默认为 false，只计算输出全价、净价、应计利息和收益率。若设置为
true，除上述4项外，还会计算并输出麦考利久期、修正久期、凸度、基点价值。

**benchmark** 可选参数，STRING 类型标量，表示算法参考基准。目前支持：

* "Qeubee"（默认值）：表示终端算法。
* "CSI"：表示中证算法。

**isExercised** 可选参数，BOOL 类型标量，表示是否行权。

* 如果不指定则会自动判断是否行权。
* 如果指定为 true，则按照行权来计算。
* 如果指定为 false 则按照不行权来计算。

## 返回值

一个字典或元组。

## 例子

例1. 计算固定利率债券的价格、到期收益率、应计利息和风险指标。

```
fixedRateBondDict = {
    "productType": "Cash",
    "assetType": "Bond",
    "bondType": "FixedRateBond",
    "start": 2022.07.15,
    "maturity": 2072.07.15,
    "issuePrice": 100.0,
    "coupon": 0.034,
    "dayCountConvention": "ActualActualISMA",
    "calendar": "CFET",
    "frequency": "Semiannual"
}
fixedRateBond = parseInstrument(fixedRateBondDict);
bondInstrumentCalculator(fixedRateBond, settlement=2025.04.10, price=0.02, priceType="YTM", calcRisk=true);

/* Output:
dirtyPrice->143.4689
cleanPrice->142.6705
ytm->0.02
accruedInterest->0.7983
macaulayDuration->27.4761
modifiedDuration->27.2041
convexity->1025.4003
pvbp->0.3902
*/

bondInstrumentCalculator(fixedRateBond, settlement=2072.04.18, price=100.2143, priceType="CleanPrice", calcRisk=false);

/* Output:
dirtyPrice: 101.0923
cleanPrice: 100.2143
ytm: 0.0250
accruedInterest: 0.8780
*/
```

例2. 计算零息债券的价格、到期收益率、应计利息和风险指标。

```
zeroCouponBondDict = {
    "productType": "Cash",
    "assetType": "Bond",
    "bondType": "ZeroCouponBond",
    "coupon": 0.0119,
    "start": 2025.01.09,
    "maturity": 2026.02.05,
    "issuePrice": 100.0,
    "dayCountConvention": "ActualActualISMA",
    "calendar": "CFET"
}
zeroCouponBond = parseInstrument(zeroCouponBondDict);
bondInstrumentCalculator(zeroCouponBond, settlement=2025.04.10, price=0.025, priceType="YTM", calcRisk=true);

/* Output:
dirtyPrice->99.2322
cleanPrice->98.9355
ytm->0.025
accruedInterest->0.2966
macaulayDuration->0.8246
modifiedDuration->0.8079
convexity->1.3057
pvbp->0.0080
*/
```

例3. 计算贴现债券的价格、到期收益率、应计利息和风险指标。

```
discountBondDict = {
    "productType": "Cash",
    "assetType": "Bond",
    "bondType": "Discount",
    "start": 2025.02.13,
    "maturity": 2025.05.15,
    "issuePrice": 99.663,
    "dayCountConvention": "ActualActualISMA",
    "calendar": "CFET"
}
discountBond = parseInstrument(discountBondDict);
bondInstrumentCalculator(discountBond, settlement=2025.04.10, price=0.02, priceType="YTM", calcRisk=true);

/* Output:
dirtyPrice->99.8085
cleanPrice->99.6012
ytm->0.02
accruedInterest->0.2073
macaulayDuration->0.0958
modifiedDuration->0.0957
convexity->0.0183
pvbp->0.0009
*/
```

例4. 同时计算多种债券的价格、到期收益率、应计利息和风险指标。

```
result = bondInstrumentCalculator([discountBond, zeroCouponBond, fixedRateBond], settlement=[2025.04.10, 2025.04.10, 2072.04.18], price=[0.02, 0.025, 100.2143], priceType=["YTM", "YTM", "CleanPrice"], calcRisk=true);

print result

/* Output:
(dirtyPrice->99.808599999999998
cleanPrice->99.601200000000005
ytm->0.02
accruedInterest->0.2074
macaulayDuration->0.0959
modifiedDuration->0.0957
convexity->0.0183
pvbp->0.001
,dirtyPrice->99.232200000000005
cleanPrice->98.935500000000004
ytm->0.025
accruedInterest->0.2967
macaulayDuration->0.8247
modifiedDuration->0.808
convexity->1.3057
pvbp->0.008
,dirtyPrice->101.092299999999994
cleanPrice->100.214299999999994
ytm->0.025
accruedInterest->0.878
macaulayDuration->0.2404
modifiedDuration->0.239
convexity->0.1142
pvbp->0.0024
*/
```

例5. 计算含权债券的价格、到期收益率、应计利息和风险指标。

```
optionBond = {
    "productType": "Cash",
    "assetType": "Bond",
    "bondType": "OptionBond",
    "version": 0,
    "instrumentId": "242659.SH",
    "nominal": 100.0,
    "start": 2025.03.26,
    "maturity": 2030.03.26,
    "coupon": 0.0207,
    "frequency": "Annual",
    "exerciseDates": [2028.03.26],
    "hasCallOption": true,
    "hasPutOption": true,
    "hasCouponAdjust": true,
    "dayCountConvention": "ActualActualISMA"
}
ins = parseInstrument(optionBond)

bondInstrumentCalculator(ins, settlement=2025.12.19, price=0.0195216, priceType="YTM", calcRisk=true, benchmark="CSI");

/* Output:
dirtyPrice: 101.99383706183775
cleanPrice: 100.46827541800214
accruedInterest: 1.5255616438356157
ytm: 0.0195216
yte: 0.018527802311956366
macaulayDuration: 2.20553110943836
modifiedDuration: 2.1654108060987873
convexity: 6.908516501810582
pvbp: 0.02208585569291825
*/
```

相关函数：bondPricer
