# DStream::pricingEngine

## 语法

`DStream::pricingEngine(timeColumn, typeColumn, securityType, method,
[securityReference], [keyColumn], [extraMetrics])`

## 详情

创建一个估值定价引擎。参考：[createPricingEngine](../c/createpricingengine.md)。

**返回值**：一个 DStream 对象。

## 参数

**timeColumn** 字符串向量，用于指定输入表中的时间列。

**typeColumn** 字符串向量，用于指定表中的债券列。根据债券列，引擎调用 *method*
中相应的方法。

**securityType** 整型向量，用于指定需要定价的债券类型。

**method** 元代码元组，用于指定债券定价算法和参数。注意：

* *method* 指定的方法和 *securityType* 指定的债券列一一对应。
* 可以传入内置函数、自定义函数或表达式。
* 算法中的参数可以是输入表中的列或者是参数 *securityReference* 中的列或者常量，优先查找参数
  *dummyTable* 中的列；如果有重名，可以用列引用的方式，如
  `dummyTable.X`。
* 对于 [vanillaOption](../c/../v/vanillaoption.md) 的 kwargs,
  支持以下几种写法：
  + 单独指定kwargs

    ```
    kwargs = dict(STRING, ANY)
    kwargs['theta'] = <theta>
    kwargs['kappa'] = <kappa>
    kwargs['rho'] = <rho>
    kwargs['sigma'] = <sigma>
    method=[<vanillaOption(settlement, maturity, valDay, spot, strike, riskFree, dividend, volatility, isCall, style, basis, calendar,"heston",kwargs)>]
    ```
  + 直接在method中构造kwargs

    ```
    method=[<vanillaOption(settlement, maturity, valDay, spot, strike, riskFree, dividend, volatility, isCall, style, basis, calendar,"heston",dict(`theta`kappa`rho`sigma, [theta, kappa, rho, sigma]))>]
    ```

**securityReference**
可选参数，内存表，用于指定每个合约基础信息。注意：不同品种的合约基础信息略有不同，如有需要请先整合到一张表里再输入；若没有信息则为空值。如下为表说明：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| type | INT | 整型标量或向量，表示标的类型 |
| assetType | INT | 资产类型 |
| symbol | SYMBOL | 合约名 |
| maturity | DOUBLE | 到期日 |
| coupon | DOUBLE | 票面利率 |
| frequency | INT | 付息频率 |
| underlying | SYMBOL | 表示标的利率，可选值为：”FR007”, “Shibor3M“，“FDR001”，“FDR007”，“ShiborO/N”，“LPR1Y”，“LPR5Y” |
| startDate | DATE | 第一次利率互换的日期 |
| endDate | DATE | 最后一次利率互换的日期。注意：须晚于 *startDay。* |
| fixRate | DOUBLE | 百分数值，表示利率互换中固定利率支付方所支付的利率，在整个利率互换期间该利率不变 |
| interval | INT | 利率互换的间隔时间 |
| basis | INT | 表示要使用的日计数基准类型 |
| Price | DOUBLE | 标的资产的当前价格。 |
| strike | DOUBLE | 标的资产的行权价格 |
| dividendYield | DOUBLE | 表示分红利率 |

**keyColumn** 可选参数，字符串标量或元组（长度为2），用于指定 *dummyTable* 和
*securityReference*  中的合约代码列。注意：需要同时指定或同时不指定参数 *sucurityReference* 和
*keyColumn*。

**extraMetrics**
可选参数，元代码元组，用于指定除定价结果外需要额外输出的信息。该参数可以传入输入列中的部分列、*securityReference*
中的部分列等。注意：不可包含常量。

## 例子

```
if (!existsCatalog("orca")) {
	createCatalog("orca")
}
go
use catalog orca

// 如已存在流图，则先销毁该流图
// dropStreamGraph('engine')
g = createStreamGraph('engine')

typeList=[0,1,2]
start=2022.07.15
maturity=2072.07.15
issuePrice=100
coupon=0.034
frequency="Semiannual"
dayCountConvention="ActualActual"
bondType="FixedRate"
settlement=2025.04.10
price=0.02
priceType="YTM"

methodList=[<bondDirtyPrice(start, maturity, issuePrice, coupon, frequency, dayCountConvention, bondType, settlement, price, priceType)>,
             <bondAccrInt(start, maturity, issuePrice, coupon, frequency, dayCountConvention, bondType, settlement)>,
             <bondDuration(start, maturity, issuePrice, coupon, frequency, dayCountConvention, bondType, settlement, price, priceType)>]
securityReference= table(take(0 1 2, 100) as type, take(1 2 3 4, 100) as assetType,"s"+string(1..100) as symbol, 2025.07.25+1..100 as maturity, rand(10.0, 100) as coupon, rand(10,100) as frequency,take([1],100) as basis )

g.source("trades", 1000:0, `tradeTime`Symbol`realTimeX`predictY`price,[TIMESTAMP,SYMBOL, DOUBLE, DOUBLE, DOUBLE])
.pricingEngine(timeColumn=`tradeTime, typeColumn=`type, securityType=typeList, method=methodList, securityReference=securityReference, keyColumn=`Symbol, extraMetrics=[<price * predictY>, <coupon+price>])
.sink("output")
g.submit()
go

data = table(take(now(), 100)as tradeTime,"s"+string(1..100) as symbol, rand(10.0, 100) as realTimeX,  rand(10.0, 100) as predictY, rand(10.0, 100) as price)

appendOrcaStreamTable("trades", data)
```
