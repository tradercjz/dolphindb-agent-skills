<!-- Auto-mirrored from upstream `documentation-main/tutorials/csap.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# CSAP 因子指标库

**CSAP 因子（Cross-Sectional Asset Pricing
Factor）**是金融领域中用于分析和解释不同资产在特定时间点上收益差异的重要工具，广泛应用于资产定价、投资组合优化和金融市场研究。CSAP
截面因子通过提取驱动资产价格变化的核心变量，帮助研究者揭示资产收益的横截面特征，即不同资产之间的价格差异来源。常见的截面因子包括价值因子（如市净率、市盈率等）、规模因子（如市值）、动量因子（基于过去收益率）、盈利性因子（如
ROE、毛利率）以及投资因子（如资本支出增长率），这些因子从不同角度反映了资产收益的潜在驱动因素。

截面因子的构建方法多种多样，从简单的四则运算到回归分析，量化研究者通过系统性的筛选和建模，提取出与资产收益高度相关的因子。投资者可以将这些因子运用在资产定价模型如
Fama-French 三因子模型等，达到优化组合配置的目的。

许多量化研究者和学术界的专家公开了他们在资产定价中使用的因子，推动了因子研究的广泛应用。在《Open Source Cross-Sectional Asset
Pricing》一文中，作者提供了数据的来源和 STATA 代码，成功展现了部分横截面股票收益预测指标。作者使用到的金融数据中的 Compustat 和 CRSP
两部分数据均来自沃顿研究数据服务（Wharton Research Data
Services），该数据服务平台提供了丰富的全球金融、经济和市场数据，常用于金融研究和分析。为了帮助研究者在实际应用中使用这些因子，我们基于文章中所描述的方法，使用
DolphinDB 脚本实现了 195 个因子的函数，并将其封装在 DolphinDB 模块 CSAPFactors.dos 中，可以在附录中进行下载。本模块基于
DolphinDB 3.00.1 及 2.00.14 版本开发，请使用 3.00.1 或 2.00.14 及以上版本进行测试。

## 1. 模块介绍

### 1.1 模块列表

DolphinDB CSAP 模块主要包含以下模块文件：

1. **CSAPFactors**：包含了 195 个标准化因子计算函数。
2. **CSAPPrepare**：
   1. prepare 开头函数：实现原始数据清洗与结构化处理。
   2. calc 开头函数：完成基础指标计算，包含数据清洗和计算两部分。
3. **CSAPHelper**：提供因子计算所需的合成数据模拟生成函数。

### 1.2 函数命名与参数规范

CSAP 因子模块中的所有函数命名规则基于因子的定义， 如 `brandInvest`
为反映公司品牌投资率的自定义因子。每一个因子的入参字段有所不同，具体参考附件中的入参含义参考表格 parameter.csv。部分输入参数字段如下：

| **参数名称** | **参数含义** |
| --- | --- |
| permno | 由证券价格研究中心（CRSP）分配给美国金融市场交易的每一种证券的唯一标识符。 |
| gvkey | 标准普尔 (S&P) Compustat 数据库中的一个唯一标识符，用来识别公司的数据记录。 |
| time\_avail\_m | 时间变量，通常表示数据的时间，可能以月为单位记录。它通常表示某一股票在特定月份的交易数据。 |
| mve\_c | 表示市值（Market Value of Equity），通常按月计算。它是由股票价格乘以流通股数得到的，反映了公司在市场上的总价值。 |
| shrout | 所有股东目前持有的公司股份总数。 |
| vol | 指证券或商品在特定时间内的交易量。 |
| cogs | 直接与生产或购买企业销售的商品相关的成本。 |

## 2. 使用说明

本章节将从环境配置、数据准备、计算函数调用方法等方面，介绍 CSAPFactors.dos 等模块的具体用法。

### 2.1. 环境配置

将附件的 CSAPFactors.dos 放在 [home]/modules 目录下。[home] 目录由系统配置参数 home 设置，可以通过
`getHomeDir()` 函数查看。若要使用模拟生成数据辅助模块，请将 CSAPDataSimulation.dos
放在 CSAPFactors 模块同一目录下。若要使用数据清理辅助模块，请将 CSAPPrepare.dos 放在 CSAPFactors
模块同一目录下。

有关模块使用的更多细节，请参见：DolphinDB
教程：模块。

### 2.2 数据准备

CSAP 的模块中一共使用到包括 Compustat、CRSP 等14 个数据表格，具体的列表可以参照 CSAPFactorTableInfo。

如若没有上述数据，可使用 CSAPDataSimulation 模块中的 `CSAPDataSimulation`
函数用来模拟生成表格数据，并返回一个字典（ key 为表格名称，value 为表格数据）。模拟数据过程中需要提供 permno, gvkey,
startYear, endYear 这四个参数。其中，前两个参数含义在上文已经介绍，startYear 和 endYear 代表模拟数据的时间范围。

如若已有可直接计算的数据，则需要保证数据表中的字段名与因子所需的参数名称保持一致。关于因子所需要的入参表格和参数名称等信息，用户可以到
CSAPFactorTableInfo 中查看。

准备好所需数据源之后，有些特殊表格（例如
SignalMasterTable）需要进行多表连接，并且不同的表格需要进行不同的数据清理步骤。为方便使用，本教程中的辅助模块 CSAPPrepare.dos
来帮助进行数据清理，方便用户可以直接进行因子计算。辅助模块为每一张表都定义了对应的数据清理函数，用户可以根据因子计算所需要的表格，自行调用数据清理函数。

注：

用户在调用 CSAPPrepare 模块函数前，需注意入参条件，某些表格的清理需要使用两张表，例如，创建 SignalMasterTable 需要
monthlyCRSP 和 m\_aCompustat 两张表的入参。

以加载 m\_aCompustat 数据并进行数据清理操作为例。

```
use CSAPDataSimulation
use CSAPPrepare

gvkeyList = 10970 10910
startYear = 1987
endYear = 2023
//数据模拟及获取
result = CSAPDataSimulation::CSAPDataSimulation(gvkeyList, startYear, endYear)
CCMLinkingTable = result.CCMLinkingTable
CompustatAnnual = result.CompustatAnnual
//表格数据清理
m_aCompustat = CSAPPrepare::prepareM_aCompustat(CompustatAnnual, CCMLinkingTable)
```

### 2.3 单个因子计算

CSAPFactors 模块中所有因子均采用向量化参数设计。用户需首先根据步骤2.2准备目标因子所需的数据集，并通过查询 CSAPFactorTableInfo
数据表确认具体参数需求。由于不同因子所需参数存在差异，建议在计算前完成参数匹配验证。

因子计算过程中的部分因子可以通过公司的财务数据进行计算，而另一部分因子则需要结合市场数据进行计算。为了方便用户计算因子，CSAP 模块提供了两种计算方式：

1. **完整计算：**通过 `prepare` 系列函数执行数据清洗（如 prepareM\_aCompustat 对
   Compustat 年度数据与 CCM 关联表进行合并清洗），再调用 `calc` 函数（如
   calcPctTotAcc）完成计算。例如，`prepareM_aCompustat`
   函数中将两个表格数据进行清洗合并，`calcPctTotAcc` 函数计算了 pctTotAcc 因子。执行
   `calcPctTotAcc`
   函数后输出结果包含三列：证券标识(permno)、数据时点(time\_avail\_m)、因子值(PctTotAcc)。

   ```
   use CSAPPrepare
   // 全流程示例：数据准备+因子计算
   cleaned_data = CSAPPrepare::prepareM_aCompustat(CompustatAnnual, CCMLinkingTable)
   result = CSAPPrepare::calcPctTotAcc(
       cleaned_data,
       startTime=1986.03M,  // 时间参数标准化格式
       endTime=2010.12M
   )
   ```
2. **直接计算**：若已持有标准化数据，可直接调用 CSAPFactors
   的因子函数：

   ```
   use CSAPFactors
   // 直接调用因子函数(需确保输入数据已标准化)
   result = select
       permno,
       time_avail_m,
       pctTotAcc(ni, prstkcc, sstk, dvt, oancf, fincf, ivncf) as PctTotAcc
   from cleaned_data
   ```

   该方式要求输入参数与函数定义严格匹配，建议配合元数据表验证参数完整性。

### 2.4 全量因子计算

当用户完成所有基础数据表的准备后，包括 Compustat 财务报表、CRSP 市场数据、FF
三因子等核心数据源后（具体可以参考附件中的数据源列表），可通过以下标准化流程实现195个因子的自动化计算。其中 varDict
保存了所有的参数，只需要将字典中的 value 替换为对应的数据源后，即可通过 `parseExpr`
动态执行计算所有的因子。

```
// 全量计算
use CSAPPrepare
varDict = dict(
    ["startTime", "endTime", "m_aCompustat", "SignalMasterTable",
     "monthlyCRSP", "monthlyFF", "monthlyLiquidity", "a_aCompustat",
     "m_QCompustat", "CompustatPensions", "CRSPdistributions", "monthlyMarket"],
    [2005.01M , 2011.12M, m_aCompustat, SignalMasterTable,
     monthlyCRSP, monthlyFF, monthlyLiquidity, a_aCompustat,
     m_QCompustat, CompustatPensions, CRSPdistributions, monthlyMarket]
)

funcList = select name, syntax from defs("CSAPPrepare::calc%")
resultDict = dict(STRING,ANY)
for (func in funcList) {
    try{
        factor_name = func.name.split("::")[1]
        resultDict[factor_name] = parseExpr(func.name + func.syntax, varDict = varDict).eval()
    }catch(ex){
        print func
        print(ex)
    }
}
```

## 3. 因子示例

在前几节中，本文已经详细地介绍了如何使用 CSAP 模块在 DolphinDB 中进行因子计算。在这一节中，我们将深入了解平方贝塔因子以及它在 DolphinDB
CSAP 中实现的方式。该因子作为典型的市场风险暴露指标，展示了如何利用向量化计算与内置统计函数构建复杂金融指标。

**因子定义**

平方贝塔因子 `betaSquared`
通过计算资产超额收益对市场超额收益平方的回归系数平方值，量化收益对非线性市场波动的敏感度。其经济学含义为资产收益率对市场二次波动的风险敞口。

**实现逻辑**

```
def betaSquared(ret, rf, ewretd){
    //Beta squared
    retrf = ret - rf  // 资产超额收益率
    ewmktrf = ewretd- rf  // 市场超额收益率

    // 执行滚动回归计算（60个月窗口，20个月最小观测值）
    return pow(mbeta(retrf, ewmktrf,60,20), 2)
}
```

从上方的代码实现来看，所有输入参数（ret, rf, ewretd）均为向量，并且 `mbeta`
函数使得窗口的滑动线性回归分析变得非常简洁，开发者无需再开发滑动回归函数即可获得贝塔值。因此，最终的完整计算方法为：

```
use CSAPPrepare
gvkeyList = 10970 10910
startYear = 1987
endYear = 2023
// 数据模拟（需要替换为真实数据）
data_simulate = CSAPDataSimulation::CSAPDataSimulation(gvkeyList, startYear, endYear)
monthlyCRSP = data_simulate.monthlyCRSP
monthlyFF = data_simulate.monthlyFF
monthlyMarket = data_simulate.monthlyMarket
// 因子计算
result = calcBetaSquared(
    prepareMonthlyCRSP(monthlyCRSP),
    prepareMonthlyFF(monthlyFF),
    prepareMonthlyMarket(monthlyMarket),
    startTime=1987.01M,
    endTime=2023.12M
)
```

除了上述展示的例子以外，在 CSAP
因子中多次使用到滑动窗口系列函数和截面函数，提升了因子函数的可读性和计算效率。这些因子能够在高效处理时序数据和截面数据时，显著提高计算效率，适应多变的数据需求。

## 4. 正确性验证

基于2005年1月至2011年12月的全样本测试数据，DolphinDB CSAP 模块的 195 个因子计算结果与 STATA 结果保持完全一致或者相关性达到 0.99
以上。针对少数存在统计差异的因子，差异主要源自以下三个维度的技术实现差异：

* ​**回归空值处理差异**​：STATA在回归计算中自动排除含空值的观测记录，而 DolphinDB
  为保持向量计算完整性，默认将空值替换为零值参与运算。该差异主要影响依赖滚动回归计算的因子：
  + 涉及因子：Beta, BetaLiquidityPS, BetaSquared, VolumeTrend
* **滑动窗口逻辑差异**​：在时序窗口计算场景中，STATA 严格要求窗口期内不得出现空值记录，否则自动跳过该窗口计算。DolphinDB
  则是全采用的计算方式。
  + 涉及因子：DivInit, DivOmit, Investment, Mom12mOffSeason, MomOffSeason
    系列(6/11/16YrPlus), VarCF, ZZ2AbnormalAccruals 系列, roavol
* **浮点数精度误差**​：DolphinDB 与 STATA 在极端小数位处理上存在细微的精度差异：
  + 涉及因子：EarnSupBig

## 5. 小结

本教程详细介绍了 CSAP 相关模块中函数的命名规则，表信息，字段含义和用法。除了常规的定义和用法介绍，这些模块本身还有一些基于 DolphinDB
实现方式的优势：例如，在因子模块 CSAPFactors 中多次使用 DolphinDB 内置函数例如 m
系列和高阶函数获取不同窗口内的计算结果，因此在代码效率以及简洁度上都提供了一个很大的提升。

## 6. 参考文献

CSAP论文：[Open Source Cross-Sectional Asset Pricing by
Andrew Y. Chen, Tom Zimmermann :: SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3604626)

GitHub链接：[GitHub - OpenSourceAP/CrossSection: Code to accompany our paper
Chen and Zimmermann (2020), "Open source cross-sectional asset
pricing"](https://github.com/OpenSourceAP/CrossSection)

## 7. 附录

### 7.1 CSAP 模块

数据源列表： [CSAPFactorTableInfo.xlsx](script/csap/CSAPFactorTableInfo.xlsx)

参数意义：[parameter.csv](script/csap/parameter.csv)

因子模块：[CSAPFactors.dos](script/csap/CSAPFactors.dos)

数据清洗及因子计算模块： [CSAPPrepare.dos](script/csap/CSAPPrepare.dos)

模拟数据模块： [CSAPDataSimulation.dos](script/csap/CSAPDataSimulation.dos)

### 7.2 因子列表

下面的因子介绍表格包含了所有因子的解释和出处。

| 论文中因子名 | 模块中因子名 | 类别 | 作者 | 年份 | 描述 |
| --- | --- | --- | --- | --- | --- |
| Accruals | accruals | Predictor | Sloan | 1996 | Accruals |
| AccrualsBM | accrualsBM | Predictor | Bartov and Kim | 2004 | Book-to-market and accruals |
| AM | am | Predictor | Fama and French | 1992 | Total assets to market |
| AssetGrowth | assetGrowth | Predictor | Cooper, Gulen and Schill | 2008 | Asset growth |
| BetaLiquidityPS | betaLiquidityPS | Predictor | Pastor and Stambaugh | 2003 | Pastor-Stambaugh liquidity beta |
| BM | bm | Predictor | Stattman | 1980 | Book to market, original (Stattman 1980) |
| BMdec | bMdec | Predictor | Fama and French | 1992 | Book to market using December ME |
| BookLeverage | bookLeverage | Predictor | Fama and French | 1992 | Book leverage (annual) |
| Cash | cash | Predictor | Palazzo | 2012 | Cash to assets |
| CashProd | cashProd | Predictor | Chandrashekar and Rao | 2009 | Cash Productivity |
| CF | cf | Predictor | Lakonishok, Shleifer, Vishny | 1994 | Cash flow to market |
| cfp | cfp | Predictor | Desai, Rajgopal, Venkatachalam | 2004 | Operating Cash flows to price |
| ChAssetTurnover | chAssetTurnover | Predictor | Soliman | 2008 | Change in Asset Turnover |
| ChEQ | chEQ | Predictor | Lockwood and Prombutr | 2010 | Growth in book equity |
| ChInv | chInv | Predictor | Thomas and Zhang | 2002 | Inventory Growth |
| ChNNCOA | chNNCOA | Predictor | Soliman | 2008 | Change in Net Noncurrent Op Assets |
| ChNWC | chNWC | Predictor | Soliman | 2008 | Change in Net Working Capital |
| ChTax | chTax | Predictor | Thomas and Zhang | 2011 | Change in Taxes |
| CompEquIss | compEquIss | Predictor | Daniel and Titman | 2006 | Composite equity issuance |
| CompositeDebtIssuance | compositeDebtIssuance | Predictor | Lyandres, Sun and Zhang | 2008 | Composite debt issuance |
| DelCOA | delCOA | Predictor | Richardson et al. | 2005 | Change in current operating assets |
| DelCOL | delCOL | Predictor | Richardson et al. | 2005 | Change in current operating liabilities |
| DelEqu | delEqu | Predictor | Richardson et al. | 2005 | Change in equity to assets |
| DelLTI | delLTI | Predictor | Richardson et al. | 2005 | Change in long-term investment |
| DelNetFin | delNetFin | Predictor | Richardson et al. | 2005 | Change in net financial assets |
| DivInit | divInit | Predictor | Michaely, Thaler and Womack | 1995 | Dividend Initiation |
| DivOmit | divOmit | Predictor | Michaely, Thaler and Womack | 1995 | Dividend Omission |
| dNoa | dNoa | Predictor | Hirshleifer, Hou, Teoh, Zhang | 2004 | change in net operating assets |
| DolVol | dolVol | Predictor | Brennan, Chordia, Subra | 1998 | Past trading volume |
| EarningsConsistency | earningsConsistency | Predictor | Alwathainani | 2009 | Earnings consistency |
| EarningsSurprise | earningsSurprise | Predictor | Foster, Olsen and Shevlin | 1984 | Earnings Surprise |
| EarnSupBig | earnSupBig | Predictor | Hou | 2007 | Earnings surprise of big firms |
| EP | ep | Predictor | Basu | 1977 | Earnings-to-Price Ratio |
| EquityDuration | equityDuration | Predictor | Dechow, Sloan and Soliman | 2004 | Equity Duration |
| ExchSwitch | exchSwitch | Predictor | Dharan and Ikenberry | 1995 | Exchange Switch |
| FirmAgeMom | firmAgeMom | Predictor | Zhang | 2006 | Firm Age - Momentum |
| GP | gp | Predictor | Novy-Marx | 2013 | gross profits / total assets |
| hire | hire | Predictor | Bazdresch, Belo and Lin | 2014 | Employment growth |
| IntMom | intMom | Predictor | Novy-Marx | 2012 | Intermediate Momentum |
| IntanBM | zz1IntanBM | Predictor | Daniel and Titman | 2006 | Intangible return using BM |
| IntanCFP | zz1IntanCFP | Predictor | Daniel and Titman | 2006 | Intangible return using CFtoP |
| IntanEP | zz1IntanEP | Predictor | Daniel and Titman | 2006 | Intangible return using EP |
| IntanSP | zz1IntanSP | Predictor | Daniel and Titman | 2006 | Intangible return using Sale2P |
| Investment | investment | Predictor | Titman, Wei and Xie | 2004 | Investment to revenue |
| InvestPPEInv | investPPEInv | Predictor | Lyandres, Sun and Zhang | 2008 | change in ppe and inv/assets |
| Leverage | leverage | Predictor | Bhandari | 1988 | Market leverage |
| LRreversal | lRreversal | Predictor | De Bondt and Thaler | 1985 | Long-run reversal |
| MeanRankRevGrowth | meanRankRevGrowth | Predictor | Lakonishok, Shleifer, Vishny | 1994 | Revenue Growth Rank |
| Mom12m | mom12m | Predictor | Jegadeesh and Titman | 1993 | Momentum (12 month) |
| Mom12mOffSeason | mom12mOffSeason | Predictor | Heston and Sadka | 2008 | Momentum without the seasonal part |
| Mom6m | mom6m | Predictor | Jegadeesh and Titman | 1993 | Momentum (6 month) |
| MomOffSeason | momOffSeason | Predictor | Heston and Sadka | 2008 | Off season long-term reversal |
| MomOffSeason06YrPlus | momOffSeason06YrPlus | Predictor | Heston and Sadka | 2008 | Off season reversal years 6 to 10 |
| MomOffSeason16YrPlus | momOffSeason16YrPlus | Predictor | Heston and Sadka | 2008 | Off season reversal years 16 to 20 |
| MomRev | momRev | Predictor | Chan and Ko | 2006 | Momentum and LT Reversal |
| MomSeason | momSeason | Predictor | Heston and Sadka | 2008 | Return seasonality years 2 to 5 |
| MomSeason06YrPlus | momSeason06YrPlus | Predictor | Heston and Sadka | 2008 | Return seasonality years 6 to 10 |
| MomSeason11YrPlus | momSeason11YrPlus | Predictor | Heston and Sadka | 2008 | Return seasonality years 11 to 15 |
| MomSeason16YrPlus | momSeason16YrPlus | Predictor | Heston and Sadka | 2008 | Return seasonality years 16 to 20 |
| MomSeasonShort | momSeasonShort | Predictor | Heston and Sadka | 2008 | Return seasonality last year |
| MomVol | momVol | Predictor | Lee and Swaminathan | 2000 | Momentum in high volume stocks |
| NetDebtFinance | netDebtFinance | Predictor | Bradshaw, Richardson, Sloan | 2006 | Net debt financing |
| NetDebtPrice | netDebtPrice | Predictor | Penman, Richardson and Tuna | 2007 | Net debt to price |
| NetEquityFinance | netEquityFinance | Predictor | Bradshaw, Richardson, Sloan | 2006 | Net equity financing |
| NetPayoutYield | netPayoutYield | Predictor | Boudoukh et al. | 2007 | Net Payout Yield |
| OPLeverage | opLeverage | Predictor | Novy-Marx | 2011 | Operating leverage |
| OrderBacklog | orderBacklog | Predictor | Rajgopal, Shevlin, Venkatachalam | 2003 | Order backlog |
| OrderBacklogChg | orderBacklogChg | Predictor | Baik and Ahn | 2007 | Change in order backlog |
| PayoutYield | payoutYield | Predictor | Boudoukh et al. | 2007 | Payout Yield |
| PctAcc | pctAcc | Predictor | Hafzalla, Lundholm, Van Winkle | 2011 | Percent Operating Accruals |
| PctTotAcc | pctTotAcc | Predictor | Hafzalla, Lundholm, Van Winkle | 2011 | Percent Total Accruals |
| Price | price | Predictor | Blume and Husic | 1973 | Price |
| PS | ps | Predictor | Piotroski | 2000 | Piotroski F-score |
| RD | rd | Predictor | Chan, Lakonishok and Sougiannis | 2001 | R&D over market cap |
| RDAbility | rdAbility | Predictor | Cohen, Diether and Malloy | 2013 | R&D ability |
| RDcap | rDcap | Predictor | Li | 2011 | R&D capital-to-assets |
| RDS | rDS | Predictor | Landsman et al. | 2011 | Real dirty surplus |
| RevenueSurprise | revenueSurprise | Predictor | Jegadeesh and Livnat | 2006 | Revenue Surprise |
| roaq | roaq | Predictor | Balakrishnan, Bartov and Faurel | 2010 | Return on assets (qtrly) |
| ShareIss1Y | shareIss1Y | Predictor | Pontiff and Woodgate | 2008 | Share issuance (1 year) |
| ShareIss5Y | shareIss5Y | Predictor | Daniel and Titman | 2006 | Share issuance (5 year) |
| ShareVol | shareVol | Predictor | Datar, Naik and Radcliffe | 1998 | Share Volume |
| Size | size | Predictor | Banz | 1981 | Size |
| std\_turn | stdTurn | Predictor | Chordia, Subra, Anshuman | 2001 | Share turnover volatility |
| STreversal | sTreversal | Predictor | Jegadeesh | 1990 | Short term reversal |
| SurpriseRD | surpriseRD | Predictor | Eberhart, Maxwell and Siddique | 2004 | Unexpected R&D increase |
| tang | tang | Predictor | Hahn and Lee | 2009 | Tangibility |
| Tax | tax | Predictor | Lev and Nissim | 2004 | Taxable income to income |
| TotalAccruals | totalAccruals | Predictor | Richardson et al. | 2005 | Total accruals |
| VolSD | volSD | Predictor | Chordia, Subra, Anshuman | 2001 | Volume Variance |
| XFIN | xFin | Predictor | Bradshaw, Richardson, Sloan | 2006 | Net external financing |
| AdExp | adExp | Predictor | Chan, Lakonishok and Sougiannis | 2001 | Advertising Expense |
| Beta | beta | Predictor | Fama and MacBeth | 1973 | CAPM beta |
| BrandInvest | brandInvest | Predictor | Belo, Lin and Vitorino | 2014 | Brand capital investment |
| DelDRC | delDRC | Predictor | Prakash and Sinha | 2013 | Deferred Revenue |
| FirmAge | firmAge | Predictor | Barry and Brown | 1984 | Firm age based on CRSP |
| GrLTNOA | grLTNOA | Predictor | Fairfield, Whisenant and Yohn | 2003 | Growth in long term operating assets |
| GrSaleToGrInv | grSaleToGrInv | Predictor | Abarbanell and Bushee | 1998 | Sales growth over inventory growth |
| GrSaleToGrOverhead | grSaleToGrOverhead | Predictor | Abarbanell and Bushee | 1998 | Sales growth over overhead growth |
| MomOffSeason11YrPlus | momOffSeason11YrPlus | Predictor | Heston and Sadka | 2008 | Off season reversal years 11 to 15 |
| MRreversal | mRreversal | Predictor | De Bondt and Thaler | 1985 | Medium-run reversal |
| NumEarnIncrease | numEarnIncrease | Predictor | Loh and Warachka | 2012 | Earnings streak length |
| OperProf | operProf | Predictor | Fama and French | 2006 | operating profits / book equity |
| RoE | roe | Predictor | Haugen and Baker | 1996 | net income / book equity |
| ResidualMomentum6m | zz1ResidualMomentum6mResidualMomentum/ zz1ResidualMomentum11mResidualMomentum | Predictor | Blitz, Huij and Martens | 2011 | 6 month residual momentum |
| ShareRepurchase | shareRepurchase | Predictor | Ikenberry, Lakonishok, Vermaelen | 1995 | Share repurchases |
| SP | sp | Predictor | Barbee, Mukherji and Raines | 1996 | Sales-to-price |
| VarCF | varCF | Predictor | Haugen and Baker | 1996 | Cash-flow to price variance |
| VolMkt | volMkt | Predictor | Haugen and Baker | 1996 | Volume to market equity |
| VolumeTrend | volumeTrend | Predictor | Haugen and Baker | 1996 | Volume Trend |
| AbnormalAccrualsPercent | zz2AbnormalAccrualsPercent | Placebo | Hafzalla, Lundholm, Van Winkle | 2011 | Percent Abnormal Accruals |
| AccrualQuality | zz2AccrualQuality | Placebo | Francis, LaFond, Olsson, Schipper | 2005 | Accrual Quality |
| AccrualQualityJune | zz2AccrualQualityJune | Placebo | Francis, LaFond, Olsson, Schipper | 2005 | Accrual Quality in June |
| BetaSquared | betaSquared | Placebo | Fama and MacBeth | 1973 | CAPM beta squred |
| DelSTI | delSTI | Placebo | Richardson et al. | 2005 | Change in short-term investment |
| KZ | kz | Placebo | Lamont, Polk and Saa-Requejo | 2001 | Kaplan Zingales index |
| roic | roIc | Placebo | Brown and Rowe | 2007 | Return on invested capital |
| ZScore | zScore | Placebo | Dichev | 1998 | Altman Z-Score |
| AMq | aMq | Placebo | Fama and French | 1992 | Total assets to market (quarterly) |
| AssetGrowth\_q | assetGrowthQ | Placebo | Cooper, Gulen and Schill | 2008 | Asset growth quarterly |
| AssetLiquidityBook | assetLiquidityBook | Placebo | Ortiz-Molina and Phillips | 2014 | Asset liquidity over book assets |
| AssetLiquidityBookQuart | assetLiquidityBookQuart | Placebo | Ortiz-Molina and Phillips | 2014 | Asset liquidity over book (qtrly) |
| AssetLiquidityMarket | assetLiquidityMarket | Placebo | Ortiz-Molina and Phillips | 2014 | Asset liquidity over market |
| AssetLiquidityMarketQuart | assetLiquidityMarketQuart | Placebo | Ortiz-Molina and Phillips | 2014 | Asset liquidity over market (qtrly) |
| AssetTurnover | assetTurnover | Placebo | Soliman | 2008 | Asset Turnover |
| AssetTurnover\_q | assetTurnoverQ | Placebo | Soliman | 2008 | Asset Turnover |
| BMq | bMq | Placebo | Rosenberg, Reid, and Lanstein | 1985 | Book to market (quarterly) |
| BookLeverageQuarterly | bookLeverageQuarterly | Placebo | Fama and French | 1992 | Book leverage (quarterly) |
| BrandCapital | brandCapital | Placebo | Belo, Lin and Vitorino | 2014 | Brand capital to assets |
| CapTurnover | capTurnover | Placebo | Haugen and Baker | 1996 | Capital turnover |
| CapTurnover\_q | capTurnoverQ | Placebo | Haugen and Baker | 1996 | Capital turnover (quarterly) |
| cashdebt | cashDebt | Placebo | Ou and Penman | 1989 | CF to debt |
| CBOperProfLagAT\_q | cbOperProfLagATQ | Placebo | Ball et al. | 2016 | Cash-based oper prof lagged assets qtrly |
| cfpq | cfpq | Placebo | Desai, Rajgopal, Venkatachalam | 2004 | Operating Cash flows to price quarterly |
| CFq | cFq | Placebo | Lakonishok, Shleifer, Vishny | 1994 | Cash flow to market quarterly |
| ChangeRoA | changeRoA | Placebo | Balakrishnan, Bartov and Faurel | 2010 | Change in Return on assets |
| ChangeRoE | changeRoE | Placebo | Balakrishnan, Bartov and Faurel | 2010 | Change in Return on equity |
| ChNCOA | chNCOA | Placebo | Soliman | 2008 | Change in Noncurrent Operating Assets |
| ChNCOL | chNCOL | Placebo | Soliman | 2008 | Change in Noncurrent Operating Liab |
| ChPM | zz1PMChPM | Placebo | Soliman | 2008 | Change in Profit Margin |
| depr | depr | Placebo | Holthausen and Larcker | 1992 | Depreciation to PPE |
| DivYield | divYield | Placebo | Naranjo, Nimalendran, Ryngaert | 1998 | Dividend yield for small stocks |
| DivYieldAnn | divYieldAnn | Placebo | Naranjo, Nimalendran, Ryngaert | 1998 | Last year's dividends over price |
| EarningsSmoothness | earningsSmoothness | Placebo | Francis, LaFond, Olsson, Schipper | 2004 | Earnings Smoothness |
| EarningsPersistence | zz1EarningsPersistence | Placebo | Francis, LaFond, Olsson, Schipper | 2004 | Earnings persistence |
| EarningsPredictability | zz1EarningsPredictability | Placebo | Francis, LaFond, Olsson, Schipper | 2004 | Earnings Predictability |
| EarningsValueRelevance | zZ1EarningsValueRelevance | Placebo | Francis, LaFond, Olsson, Schipper | 2004 | Value relevance of earnings |
| EarningsTimeliness | zZ1EarningsTimeliness | Placebo | Francis, LaFond, Olsson, Schipper | 2004 | Earnings timeliness |
| EarningsConservatism | zZ1EarningsConservatism | Placebo | Francis, LaFond, Olsson, Schipper | 2004 | Earnings conservatism |
| EBM\_q | eBMQ | Placebo | Penman, Richardson and Tuna | 2007 | Enterprise component of BM |
| EntMult\_q | entMultQ | Placebo | Loughran and Wellman | 2011 | Enterprise Multiple quarterly |
| EPq | ePq | Placebo | Basu | 1977 | Earnings-to-Price Ratio |
| ETR | eTr | Placebo | Abarbanell and Bushee | 1998 | Effective Tax Rate |
| FRbook | zz1frfrBook | Placebo | Franzoni and Marin | 2006 | Pension Funding Status |
| GPlag | gPlag | Placebo | Novy-Marx | 2013 | gross profits / total assets |
| GPlag\_q | gPlagQ | Placebo | Novy-Marx | 2013 | gross profits / total assets |
| GrGMToGrSales | grGMToGrSales | Placebo | Abarbanell and Bushee | 1998 | Gross margin growth to sales growth |
| GrSaleToGrReceivables | grSaleToGrReceivables | Placebo | Abarbanell and Bushee | 1998 | Change in sales vs change in receiv |
| KZ\_q | kZQ | Placebo | Lamont, Polk and Saa-Requejo | 2001 | Kaplan Zingales index quarterly |
| LaborforceEfficiency | laborforceEfficiency | Placebo | Abarbanell and Bushee | 1998 | Laborforce efficiency |
| Leverage\_q | leverageQ | Placebo | Bhandari | 1988 | Market leverage quarterly |
| NetDebtPrice\_q | netDebtPriceQ | Placebo | Penman, Richardson and Tuna | 2007 | Net debt to price |
| NetPayoutYield\_q | netPayoutYieldQ | Placebo | Boudoukh et al. | 2007 | Net Payout Yield quarterly |
| OperProfLag | operProfLag | Placebo | Fama and French | 2006 | operating profits / book equity |
| OperProfLag\_q | operProfLagQ | Placebo | Fama and French | 2006 | operating profits / book equity |
| OperProfRDLagAT | operProfRDLagAT | Placebo | Ball et al. | 2016 | Oper prof R&D adj lagged assets |
| OperProfRDLagAT\_q | operProfRDLagATQ | Placebo | Ball et al. | 2016 | Oper prof R&D adj lagged assets (qtrly) |
| OPLeverage\_q | opLeverageQ | Placebo | Novy-Marx | 2011 | Operating leverage (qtrly) |
| PayoutYield\_q | payoutYieldQ | Placebo | Boudoukh et al. | 2007 | Payout Yield quarterly |
| pchcurrat | zz1CurratPchcurrat | Placebo | Ou and Penman | 1989 | Change in Current Ratio |
| pchdepr | pchDepr | Placebo | Holthausen and Larcker | 1992 | Change in depreciation to PPE |
| pchgm\_pchsale | pchgmPchSale | Placebo | Abarbanell and Bushee | 1998 | Change in gross margin vs sales |
| pchquick | pchQuick | Placebo | Ou and Penman | 1989 | Change in quick ratio |
| pchsaleinv | pchSaleInv | Placebo | Ou and Penman | 1989 | Change in sales to inventory |
| PM\_q | pMQ | Placebo | Soliman | 2008 | Profit Margin |
| PS\_q | pSQ | Placebo | Piotroski | 2000 | Piotroski F-score |
| quick | quick | Placebo | Ou and Penman | 1989 | Quick ratio |
| RD\_q | rDQ | Placebo | Chan, Lakonishok and Sougiannis | 2001 | R&D over market cap quarterly |
| rd\_sale | rdSale | Placebo | Chan, Lakonishok and Sougiannis | 2001 | R&D to sales |
| rd\_sale\_q | rdSaleQ | Placebo | Chan, Lakonishok and Sougiannis | 2001 | R&D to sales quarterly |
| RetNOA | retNOA | Placebo | Soliman | 2008 | Return on Net Operating Assets |
| RetNOA\_q | retNOAQ | Placebo | Soliman | 2008 | Return on Net Operating Assets |
| roavol | roaVol | Placebo | Francis, LaFond, Olsson, Schipper | 2004 | RoA volatility |
| salecash | saleCash | Placebo | Ou and Penman | 1989 | Sales to cash ratio |
| saleinv | saleInv | Placebo | Ou and Penman | 1989 | Sales to inventory |
| salerec | saleRec | Placebo | Ou and Penman | 1989 | Sales to receivables |
| secured | secured | Placebo | Valta | 2016 | Secured debt |
| securedind | securedInd | Placebo | Valta | 2016 | Secured debt indicator |
| sgr | sgr | Placebo | Lakonishok, Shleifer, Vishny | 1994 | Annual sales growth |
| sgr\_q | sgrQ | Placebo | Lakonishok, Shleifer, Vishny | 1994 | Annual sales growth quarterly |
| SP\_q | sPQ | Placebo | Barbee, Mukherji and Raines | 1996 | Sales-to-price quarterly |
| tang\_q | tangQ | Placebo | Hahn and Lee | 2009 | Tangibility quarterly |
| Tax\_q | taxQ | Placebo | Lev and Nissim | 2004 | Taxable income to income (qtrly) |
