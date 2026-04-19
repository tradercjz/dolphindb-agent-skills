<!-- Auto-mirrored from upstream `documentation-main/tutorials/instrument_and_mktdata.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# DolphinDB 面向金融交易与定价的统一数据模型

## 1. 背景

近年来，随着人民币国际化进程加快以及中国金融市场与国际市场不断接轨，投资者对各类金融产品的需求显著上升。在交易类型日益丰富、交易规模持续增长的背景下，金融机构面临如何快速把握市场机遇的挑战，无论是在业务布局还是技术体系建设方面，都需要作出有效应对。

在传统金融系统中，各类交易数据通常被分散存储于结构各异的数据表中，不同数据表的字段名称、数量往往不一致。这种异构存储方式导致在查询投资组合的交易信息时，需频繁执行跨表关联操作，不仅增加了查询复杂度，还容易引入错误，严重制约了系统处理的性能和效率。另外一种方式是把所有的交易集中存储在一张表或按大类分成的少数几张表中，由于字段平铺，表中存在大量空数据，可读性比较差，增加新字段也比较麻烦。

为了应对行业内这一顽疾，DolphinDB 将各种金融工具抽象为统一的 INSTRUMENT 类型，每种金融工具均可通过字典类型进行封装，解析后存入金融工具表的
instrument 字段中。同时，表中还提供 instrumentId
字段与交易表关联。通过将全部金融工具信息存储到金融工具表，全部交易数据整合到交易表中，DolphinDB 显著简化了建表流程，并大幅提升了查询效率。

此外，金融产品定价往往依赖于多种市场数据（如 Curve、Surface 等）。为了统一不同类型市场数据的存储与访问，DolphinDB
提供了专门的数据类型，从而在数据库层面实现了对市场数据的高效管理与存取。

## 2. Instrument

Instrument 类是对金融工具的抽象，用于建模各种资产和衍生品，所有金融工具都继承自 Instrument 基类。部分金融工具类名如下：

![](images/instrument_pricer/2_1.png)

通常情况下，市场上交易的金融工具可以分为两类：

**标准型**：包括场内交易的期货、期权等，也包括债券等部分场外产品。这类工具合约条款清晰，有固定的交易代码，合约到期前可以买卖流通。

**非标准型**：绝大部分的场外交易产品，比如利率互换、外汇远期等。这类工具合约条款由交易双方自行约定，持有至到期。

对于标准型金融工具，可将其唯一的交易代码作为 instrumentId，用于存储其基础信息。在交易表中通过 instrumentId 关联相应金融工具的
instrumentId，其基础信息仅需保存一次， tradeId 和 instrumentId
是多对一的关系。而对于非标准化金融工具，由于每笔交易的条款均为定制，无法共享基础信息，因此需单独创建一个 Instrument 对象，生成全局唯一的
instrumentId， tradeId 和 instrumentId 是一对一的关系 。下面是金融工具表 (instrument) 和交易表 (trade)
的一个示例，两者通过 instrumentId 关联。

![](images/instrument_pricer/2_2.png)
![](images/instrument_pricer/2_3.png)

部分代码如下：

```
//Step1: 加载金融工具基础信息
bond1 = {
    "productType": "Cash",
    "assetType": "Bond",
    "bondType": "DiscountBond",
    "instrumentId": "259951.IB",
    "start": 2025.08.14,
    "maturity": 2025.11.13,
    "issuePrice":99.694,
    "frequency": "Once",
    "dayCountConvention": "ActualActualISDA"
}

bond2 = {
    "productType": "Cash",
    "assetType": "Bond",
    "bondType": "FixedRateBond",
    "instrumentId": "2500005.IB",
    "start": 2025.07.15,
    "maturity": 2055.07.15,
    "issuePrice": 100,
    "coupon": 0.019,
    "frequency": "Semiannual",
    "dayCountConvention": "ActualActualISDA"
}

bond3 = {
    "productType": "Cash",
    "assetType": "Bond",
    "bondType": "FixedRateBond",
    "instrumentId": "250018.IB",
    "start": 2025.09.15,
    "maturity": 2032.09.15,
    "issuePrice": 100.0,
    "coupon": 0.0178,
    "frequency": "Annual",
    "dayCountConvention": "ActualActualISDA"
}

bondFutures1 = {
    "productType": "Futures",
    "futuresType": "BondFutures",
    "instrumentId": "TF2512",
    "nominal": 100.0,
    "maturity": 2025.12.12,
    "settlement": 2025.12.16,
    "underlying": bond3,
    "nominalCouponRate": 0.03
}

irs1 = {
    "productType": "Swap",
    "swapType": "IrSwap",
    "irSwapType": "IrFixedFloatingSwap",
    "instrumentId": "IRSWP_00000001",  //场外交易，每笔都是一个instrument，这里是自定义id，要保证unique
    "start": 2025.09.18,
    "maturity": 2030.09.18,
    "frequency": "Quarterly",
    "fixedRate": 0.02,
    "calendar": "CFET",
    "fixedDayCountConvention": "Actual365",
    "floatingDayCountConvention": "Actual365",
    "payReceive": "Receive",
    "iborIndex": "FR_007",
    "spread": 0.00,
    "notional":["CNY", 1E8]
}

//Step2：建表储存金融工具 （用户可以根据需要添加更多字段）
create table instrument (
    instrumentId STRING,
    instrumentType STRING,
    instrument INSTRUMENT,
    isRegular BOOL,      // ture表示有交易代码的金融工具，false表示没有交易代码的金融工具,主要针对instrumentId
    insertTime DATETIME,
    updateTime DATETIME
)
go

//插入instrument
insert into instrument values("259951.IB", "DicountBond", parseInstrument(bond1), true, 2025.08.13 09:00:00, 2025.08.13 09:00:00)
insert into instrument values("2500005.IB", "FixedRateBond", parseInstrument(bond2), true, 2025.07.14 09:00:00, 2025.07.14 09:00:00)
insert into instrument values("250018.IB", "FixedRateBond", parseInstrument(bond3), true, 2025.09.14 09:00:00, 2025.09.14 09:00:00)

insert into instrument values("TF2512", "BondFutures", parseInstrument(bondFutures1), true, 2025.03.16 09:00:00, 2025.03.16 09:00:00)

insert into instrument values("IRSWP_00000001", "IrFixedFloatingSwap", parseInstrument(irs1), false, 2025.09.18 10:10:10, 2025.09.18 10:10:10)
```

### 2.1 解析和提取

每个金融工具的详细字段定义和示例参考 parseInstrument。可以通过 parseInstrument 函数对一个金融工具字典进行解析，并通过 extractInstrument 函数将
Instrument 对象提取为字典。

![](images/instrument_pricer/2_4.png)

图 1. 解析（parse）

![](images/instrument_pricer/2_5.png)

图 2. 提取（extract）

### 2.2 添加额外字段

parseInstrument
文档中规定了每种金融工具的数据成员（必填和选填）。除了各自规定的字段外，用户也可以根据自身需要增加字段。对于用户添加的额外字段，我们也可以进行解析和提取。

![](images/instrument_pricer/2_6.png)

图中的发行方 issuer 是额外添加的字段，同样可以被解析和提取。

### 2.3 Instrument 字段查询

解析后存储简化了建表流程，但是存储之后，如何能方便快速地查询金融工具信息，是我们急需解决的问题。DolphinDB
针对此问题，提供了一系列工具函数，方便用户进行查询，具体可以分为三类接口：

**第一类**：直接读取单个属性。

对于名义金额、频率、到期日等常见字段，系统提供专用接口，例如：`getInstrumentNominal(instrument)`、`getInstrumentFrequency(instrument)`、`getInstrumentMaturity(instrument)`
等。

用户无需了解字典内部结构，只需传入 instrument，即可返回相应的属性值。

详见 getInstrumentNominal， getInstrumentFrequency，getInstrumentMaturity。

**第二类**： 查看 instrument 包含的所有字段。

使用 `getInstrumentKeys(instrument)` 可以查看 instrument 中每个元素包含哪些键。

详见 getInstrumentKeys。

**第三类**：根据 key 批量查找数据成员。

使用 `getInstrumentField(instrument, key, [default])` 可以查看
instrument 参数中每个元素对应 key 的值。其中，default 为默认值参数，用于确定输出的数据类型。

详见 getInstrumentField。

一般来说，第一类和第三类接口查询效率是等价的：

| 第一类接口 | 第三类接口 |
| --- | --- |
| getInstrumentNominal(instrument) | getInstrumentField(instrument, “nominal”) |
| getInstrumentFrequency(instrument) | getInstrumentField(instrument, “frequency”) |
| getInstrumentMaturity(instrument) | getInstrumentField(instrument, “maturity”) |

构建一个 instrument 组合（60% 债券，20% 国债期货， 20% 利率互换），相关性能指标如下：

| 字段类型 | 函数调用 | 10万条 | 100万条 |
| --- | --- | --- | --- |
| DOUBLE | getInstrumentField(instrument, “nominal”) | 4ms | 8ms |
| STRING | getInstrumentField(instrument, “frequency”) | 10ms | 60ms |
| DATE | getInstrumentField(instrument, “maturity”) | 4ms | 8ms |

测试代码见附录。

### 2.4 Instrument 条件查询

条件查询是数据库的常见操作。即便将 instrument
的全部属性统一存储在单一字段中，基于属性的条件过滤也不会出现明显的性能退化。用户只需对原有条件语句进行少量改写，即可获得与结构化字段相同的查询效果，比如

```
select * from t where coupon > 0.01 and maturity > 2025.10.30;
```

改为

```
select * from t where getInstrumentField(instrument, "coupon") > 0.01 and
getInstrumentField(instrument, "maturity") > 2025.10.30;
```

或者

```
select * from t where getInstrumentCoupon(instrument) > 0.01 and
getInstrumentMaturity(instrument) > 2025.10.30;
```

就能得到相同的结果，性能结果如下：

| 条件 | 10万条instrument | 100万条instrument |
| --- | --- | --- |
| coupon > 0.015 | 4ms | 15ms |
| coupon > 0.015 and maturity > 2027.01.01 | 6ms | 20ms |
| coupon > 0.015 and frequency = “Annual“ | 8ms | 30ms |

测试代码见附录。

### 2.5 用户自定义 Instrument 类型

为了解决大宽表字段过多的问题，有些用户采用 JSON 的方式存取整个 Instrument
对象，但是查询数据的时候遇到了性能问题（与多表关联查询性能差不多）。为了适配这种需求，我们给出一个用户自定义 Instrument 类型 ——
UserDefined，除了必填 {“productType”： “UserDefined”} 外，其他字段可以完全由用户自定义。

采用自定义 Instrument 类型存储后，查询某个字段的性能对比 JSON 方案性能提升十倍以上。以下为一个测试案例：

```
inst = {
    "productType": "UserDefined",
    "asset": "黄金",
    "code": "au2512C568",
    "start": 2025.03.04,
    "maturity": 2025.11.24,
    "underlying": "au2512",
    "payoffType": "Call",
    "strike": 568,
    "optionType": "American",
    "exchange":"上海期货交易所"
}
instrument = parseInstrument(inst)
n = 100000 //instrument测试个数
instrument_list = []
for (i in 0:n) {
    instrument_list.append!(instrument)
}
json_list = take(toStdJson(inst), n)
t = table(instrument_list as ins_col, json_list as json_col)

def getDictValue(dict_list, key) {
    res = array(STRING, 0, dict_list.size())
    for (d in dict_list) {
        res.append!(d[key])
    }
    return res
}

//全部用JSON存储后取strike字段
timer{  //409.603 ms
    t["json_dict"] = fromStdJson(t["json_col"])
    res1 = select * from t where getDictValue(json_dict, "strike")$DOUBLE > 560.0
}

//全部用自定义Instrument存储后取strike字段
timer{ //39.776 ms
    res2 = select * from t where getInstrumentField(instrument, "strike")$DOUBLE > 560.0
}
```

上面的例子测试了 10 万个 Instrument 分别按照 JSON 和自定义 Instrument 类型存储，查询某个 DOUBLE
类型字段的结果是：JSON 存储的查询耗时 409.6 ms，DolphinDB 自定义 Instrument 类型存储的查询耗时 39.8 ms，
后者性能提升十倍以上。

### 2.6 Instrument 目前的一些应用

上面介绍了 instrument 存储方案。下面会介绍基于 instrument 对象的一些业务函数。

#### 2.6.1 基于 instrument 对象的债券计算器

bondInstrumentCalculator 函数的第一个参数是
instrument，不同种类的债券都可以按照一定的结构封装到 instrument 中。

```
// 通过 ytm 计算多只债券的全价和风险指标
// 假设所有债券信息都parse后存储在金融工具表（Instrument）的 instrument 字段中

select bondInstrumentCalculator(t.instrument, settlement=2025.04.10, price=0.02, \
priceType="YTM", calcRisk=true) from Instrument as t where t.maturity > 2025.04.10;
```

#### 2.6.2 定价函数

从 DolphinDB V3.00.4 开始，我们会提供一些列 FICC&Equity 定价函数，每个函数的第一个参数统一为Instrument
对象，可参考 bondPricer，irFixedFloatingSwapPricer，fxEuropeanOptionPricer 等。

#### 2.6.3 特殊定价函数

instrumentPricer 和 portfolioPricer 是
DolphinDB 提供的两个特殊定价函数，它们的第一个参数为 instrument，可以填入 INSTRUMENT
标量或者向量，来分别对一个金融工具或者多个金融工具进行定价。因为所有金融工具都是 INSTRUMENT
类型，所以不同类型的金融工具可以放到同一个向量中进行批量定价。

```
// 对投资组合定价，假设组合里只有国债和以FR007为参考利率的利率互换交易
// 假设所有债券和利率互换基础信息存储在金融工具表（Instrument）的 instrument 字段中
// 假设曲线数据存储在市场数据表（MarketData）表中的 data 字段中
pricingDate = 2025.08.18

mktData = select data from MarketData where date = pricingDate and name in \
          ["CNY_TREASURY_BOND", "CNY_FR_007"]
npvs = select instrumentPricer(t.instrument, pricingDate, mktData) from Instrument as t;
```

## 3. MktData

金融工具的定价需要用到即期/曲线/曲面等市场数据，DolphinDB 的 MktData 类是对市场数据的抽象，目前支持的市场数据都继承自 MktData
基类，目前支持的市场数据类型如下：

![](images/instrument_pricer/3.png)

每个市场数据的详细字段定义和示例参考 parseMktData。可以通过 parseMktData 函数对一个市场数据字典进行解析，并通过 extractMktData 函数将
MktData 对象提取为字典。

```
curve = {
    "mktDataType": "Curve",
    "curveType": "IrYieldCurve",
    "referenceDate": 2025.07.01,
    "currency": "CNY",
    "curveName": "CNY_FR_007",
    "dayCountConvention": "Actual365",
    "compounding": "Continuous",
    "interpMethod": "Linear",
    "extrapMethod": "Flat",
    "dates":[2025.07.07,2025.07.10,2025.07.17,2025.07.24,2025.08.04,2025.09.03,2025.10.09,2026.01.05,
        2026.04.03,2026.07.03,2027.01.04,2027.07.05,2028.07.03],
    "values":[0.015785,0.015931,0.016183,0.016381,0.016493,0.016503,0.016478,0.016234,0.016321,
        0.016378,0.015508,0.015185,0.014901],
    "settlement": 2025.07.01
}

mktData = parseMktData(curve)
//打印mktData数据类型
print(typestr(mktData))  //MKTDATA

//提取mktData里面的信息
d = extractMktData(mktData)
print(d)
/*
  mktDataType->Curve
  version->1
  curveType->IrYieldCurve
  referenceDate->2025.07.01
  dayCountConvention->Actual365
  curveName->CNY_FR_007
  dates->[2025.07.07,2025.07.10,2025.07.17,2025.07.24,2025.08.04,2025.09.03,2025.10.09,2026.01.05,2026.04.03,2026.07.03,2027.01.04,2027.07.05,2028.07.03]
  years->[0.016438356164384,0.024657534246575,0.043835616438356,0.063013698630137,0.093150684931507,0.175342465753425,0.273972602739726,0.515068493150685,0.756164383561644,1.005479452054794,1.512328767123288,2.010958904109589,3.008219178082192]
  values->[0.015785,0.015931,0.016183,0.016381,0.016493,0.016503,0.016478,0.016234,0.016321,0.016378,0.015508,0.015185,0.014901]
  interpMethod->Linear
  extrapMethod->Flat
  currency->CNY
  compounding->Continuous
  curveModel->Bootstrap
  settlement->2025.07.01
  frequency->Annual
*/
```

**这样设计的好处**

* 所有定价所需的市场数据可以统一存储在一张表中，便于管理和查询。
* 该表可进一步保存为流表，支持实时定价场景。

## 4. 多资产建模在组合管理上的应用

组合管理是金融机构投资部门的核心能力。如何有效的管理交易，实现实时指标计算、实时估值、实时风控，已成为金融机构数字化转型的关键挑战。

传统的组合管理数据建立在关系型数据库上，数据模型复杂，对金融产品（股票、债券、衍生品等和交易没有很好的抽象。每种资产需要不同的表进行资产定义、指标、交易、行情的管理。需要几十上百张表才能实现多资产的描述，数据难以管理和使用。我们的
INSTRUMENT 数据类型解决了这一问题。

传统的定价需要用到的曲线/曲面分别存储在不同的数据表中。定价的时候需要经过“查询->组装->交易匹配->定价” 等诸多步骤，流程比较繁琐和低效。我们提供的 MKTDATA
数据类型可以提前把曲线/曲面等数据封装存储到一张表中，定价的时候只需要一条简单的 SQL 查询语句就可以取出。

前文介绍了 Instrument 和 MktData 的基本概念和用法，
下面我们利用这套数据模型，说明一下多资产建模在组合管理上的应用。我们通过一个简化的架构图，来说明我们的解决方案。

![](images/instrument_pricer/4.png)

整个存储与计算过程可以简化为五张表，其中：

* **Instrument**：金融工具表，用于存储金融工具的基本信息。其中 instrumentId 为 unique 的，对于标准型金融工具，一个
  id 可以对应多笔交易；对于非标准型金融工具，一个 id
  只能对应一笔交易。金融工具的基本信息，包括定价需要用到的市场数据（Curve/Surface）名称可以解析后放到 instrument
  字段中，也可以放在外面， 方便定价时与 MarketData 表关联 。
* **MarketData**：市场数据表，用于存储定价需要依赖的曲线/曲面信息。 其中 ，data 字段存储解析后的曲线/曲面数据， 通过参考日期
  referenceDate 与定价函数的 pricingDate 关联，通过 name 和具体的 instrument 关联。
* **Trade**：交易表，用于存储各类金融产品的交易信息。其中 instrumentId 与 Instrument
  表关联，获取金融工具基本信息。
* **Indicator**：指标表，用于存储用户需要计算的指标。每个投资组合可以定制化指标列表。
* **Portfolio**：投资组合表，用于存储投资组合的基本信息，通过 tradeIds 字段和交易表关联， indicatorIds
  和指标表关联。

上述五张表可以作为组合管理平台的数据基座，加上 DolphinDB 内置的指标计算和金融产品定价函数，我们可以实现组合管理的基本功能。

表 1. 与传统关系型数据建模对比

| 维度 | 传统关系型方案 | DolphinDB 统一数据模型 |
| --- | --- | --- |
| 资产定义表数量 | 数十～上百张 | `Instrument` 1 张 |
| 市场数据表 | 多张按类型拆分 | `MarketData` 1 张 |
| 新增一种资产 | 新建多张表 + 程序改动 | 新增 Instrument 结构并 parse 入库 |
| 定价所需市场数据 | 多表查询 + 手工组装 | 一次查询 `MarketData`，直接传给 pricer |
| 实时估值 | 困难（关系型不擅长流数据） | 可用流表 + 内存计算 |

INSTRUMENT 和 MKTDATA 这类对象建模，并非 DolphinDB 首创。高盛（Goldman Sachs）自 20 世纪90 年代起内部使用的
SecDB（Securities
DataBase）​系统，就被广泛认为是这一领域的先驱，它通过统一的对象模型极大地简化了跨资产的风险管理与交易流程。除此之外，我们也有客户用 Java
对象来表示INSTRUMENT，将 Java 对象存储在 Cassandra 中。在大量拜访金融机构的需求和总结国内外相关建模经验的基础上，我们在 DolphinDB
V3.00.4 版本上推出这套建模方法。我们在工程上做了一些优化，比如对象的检索，债券计算器、定价函数的适配等，极大方便了用户在 SQL 中调用。

在可扩展性上，这套数据模型也比较有优势。无论是新增加一种金融工具，还是新增加一条曲线，我们几乎不用修改应用逻辑，只需要做好以下事情：

* 按照新增加的金融工具结构封装，解析，入库（Instrument 表）
* 按照新增加的曲线结构封装，解析，入库（MarketData表）
* 适配新的金融工具定价函数（xxxPricer） 和相关的指标计算定义。

## 5. 总结

工欲善其事，必先利其器。DolphinDB 为多资产交易和定价提供了一套统一的数据模型—— Instrument 和 MktData 。下面是这套数据模型的特点：

**降低系统复杂性与维护成本**

传统系统需为每类资产设计独立表结构，动辄数十上百张表，维护困难。DolphinDB
通过统一模型将组合管理相关表数量压缩至5张核心表，简化架构，降低开发与运维负担。

**支持多资产统一管理与实时定价**

所有金融工具（债券、期货、互换等）均可用同一套模型表示，便于跨资产组合管理。结合实时市场数据流，支持投资组合的实时估值与风险计算，助力机构快速响应市场变化。

**增强业务敏捷性与产品创新能力。**

新增金融工具或市场曲线时，无需修改数据库结构，只需按规范封装数据并入库。定价函数可直接调用，支持快速上线新产品，缩短从设计到交易的周期。

**提升风险管理与合规能力**

统一数据模型便于全面、一致地计算各类资产的风险指标（如久期、凸性、希腊字母等）。所有定价与风险计算可追溯、可复核，符合内部审计与监管要求。

**大幅提升数据查询与处理效率**

通过统一数据模型（Instrument +
MktData），将分散在多表中的金融工具与市场数据整合存储，减少跨表关联操作。实测显示，百万级金融工具查询可在数十毫秒内完成，显著提升交易分析、定价与风控的响应速度。

**借鉴国际领先实践，提升行业竞争力**

模型设计参考高盛 SecDB 等国际先进系统，融合国内金融机构实战需求，具备行业前瞻性与落地性。帮助机构在数据架构层面接轨国际，提升在全球市场中的竞争力。

简言之，DolphinDB的统一数据模型不仅仅是一项技术升级，更是一次金融数据治理和运营模式的革新。它直接服务于高管层最关心的业务敏捷性、风险控制、成本优化和数据价值四大战略目标，是金融机构在数字化竞争中构建核心优势的关键基础设施。

## 附录

[instrumentTest.dos](script/instrument_pricer/instrumentTest.dos)
