<!-- Auto-mirrored from upstream `documentation-main/mcp/examples.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 场景案例

借助 MCP 服务，您可以将 ChatGPT、Claude、DeepSeek 或自建的大模型，借助第三方 MCP Client 平台如 Cherry Studio与
DolphinDB 工具生态无缝结合。通过灵活的 Prompt 设计和工具链编排，快速搭建高效的金融智能应用。

无论是指标选股、因子评价，还是多因子策略回测，MCP 都能让大模型根据您的需求自动调度相应工具，实现端到端的数据分析与决策流程。

下面展示一些典型金融场景案例，供参考。

## 指标选股

| 用户提问 | 平台 | 模型 | 调用结果 | 备注 |
| --- | --- | --- | --- | --- |
| 帮我找出2025年11月11日，净利润增速大于10%，市值小于1000亿大于50亿，在主板或者创业版的股票 | Cherry Studio | DeepSeek-V3.1 | ![](images/stock_mcp/example01.png) | 调用工具：查询指标元数据，指标选股 |
| 找出在2025年11月11日，上市时间满一年（252工作日），无退市风险（ST和S），市值大于10亿，小于100亿，市盈率大于0，小于30，市净率大于0，小于5的股票 | Cherry Studio | DeepSeek-V3.1 | ![](images/stock_mcp/example02.png) | 调用工具：查询指标元数据，指标选股 |
| 我想要找一些股票： 在2025年11月11日，净资产收益率大于8% ，净利润增长率>10% ，资产负债率<50% ，总市值大于100亿 | Cherry Studio | DeepSeek-V3.1 | ![](images/stock_mcp/example03.png) | 调用工具：查询指标元数据，指标选股 |
| 选出2025年11月11日成交量大于200手的股票 | Cherry Studio | DeepSeek-V3.1 | ![](images/stock_mcp/example04.png) | 调用工具：查询指标元数据，指标选股 |
| 给我找出2025年11月11日成交量超过20日平均成交量的1.5倍，并且技术指标出现MACD\_DIF > MACD\_DEA（MACD金叉信号）或KDJ\_K > KDJ\_D（KDJ金叉信号）。 | Cherry Studio | DeepSeek-V3.1 | ![](images/stock_mcp/example05.png) | 调用工具：查询指标元数据，指标选股，查询前一交易日股票信息，导出 CSV |
| 找出2025年11月11日ROC指标>5、MA5>MA20的趋势转折股票 | Cherry Studio | DeepSeek-V3.1 | ![](images/stock_mcp/example06.png) | 调用工具：查询指标元数据，指标选股 |
| 找出2025年11月11日市销率<5、但净利润增长>10%、上市时间满252天、无退市风险的成长型公司 | Cherry Studio | DeepSeek-V3.1 | ![](images/stock_mcp/example07.png) | 调用工具：查询指标元数据，指标选股 |
| 创业板里有哪些在2025年11月11日净利润增长>10%、市值10-500亿的成长股，资产负债率小于50 | Cherry Studio | DeepSeek-V3.1 | ![](images/stock_mcp/example08.png) | 调用工具：查询指标元数据，指标选股 |
| 筛选沪深300成分股中，2025年11月11日股息率超过3%、净利润增长的非ST价值股 | Cherry Studio | DeepSeek-V3.1 | ![](images/stock_mcp/example09.png) | 调用工具：查询指标元数据，指标选股 |
| 找出2025年11月11日MACD\_DIF > 0 且 MACD\_DIF > MACD\_DEA、KDJ K指标在50-80强势区域、股价高于所有主要均线（MA5/MA20/MA50）、同时基本面PE<30倍、利润增长的股票 | Cherry Studio | DeepSeek-V3.1 | ![](images/stock_mcp/example10.png) | 调用工具：查询指标元数据，指标选股 |

**DeepSeek-V3.1 使用案例**

[](videos/video_01.mp4)

**Gemini 3 Pro 使用案例**

[](videos/video_02.mp4)

**Doubao 1.5 Pro使用案例**

[](videos/video_03.mp4)

## 单因子评价

| 用户提问 | 平台 | 模型 | 调用结果 | 备注 |
| --- | --- | --- | --- | --- |
| 帮我分析pe因子在半导体行业从2025年1月1日到2025年11月11日的有效性，持有期为5天 | Cherry Studio | DeepSeek-V3.1 | ![](images/stock_mcp/example11.png)![](images/stock_mcp/example12.png) | 调用工具：查询指标元数据、单因子回测、清理内存 |
| ROE因子在半导体行业从2025年1月1日到2025年11月11日的有效性分析，持有期为5天 | Cherry Studio | DeepSeek-V3.1 | ![](images/stock_mcp/example13.png) | 调用工具：查询指标元数据、单因子回测、清理内存 |
| 帮我分析资产负债率因子在白酒行业从2023年1月1号到2025年11月11日的表现情况，持有期为10天 | Cherry Studio | DeepSeek-V3.1 | ![](images/stock_mcp/example14.png) | 调用工具：查询指标元数据、单因子回测、清理内存 |
| 帮我分析2022年1月1日到2025年11月11日MASS因子对白酒行业的有效性，持有期为10天 | Cherry Studio | DeepSeek-V3.1 | ![](images/stock_mcp/example15.png) | 调用工具：查询指标元数据、单因子回测、清理内存 |
| 帮我分析股息率因子在2021年1月1日到2025年11月11日的银行板块的有效性，持有期为10天 | Cherry Studio | DeepSeek-V3.1 | ![](images/stock_mcp/example16.png)![](images/stock_mcp/example17.png) | 调用工具：查询指标元数据、单因子回测、清理内存 |

**DeepSeek-V3.1 使用案例**

[](videos/video_04.mp4)

**Gemini 3 Pro 使用案例**

[](videos/video_05.mp4)

**Doubao 1.5 Pro使用案例**

[](videos/video_06.mp4)

## 多因子策略回测

| 用户提问 | 平台 | 模型 | 调用结果 | 备注 |
| --- | --- | --- | --- | --- |
| 我想要回测一个复合策略：  选股范围：中证1000成分股  筛选条件：流通市值小于50亿 + PE小于30 + PB小于2 + 上市时间超过1年 的非ST/S股  持仓规则：选择流通市值最小的15只股票，等权重配置  调仓频率：持仓10个交易日 在每周一调仓  回测期间：2023.01.01-2024.12.31 基准指数：000852.SH（中证1000）  初始资金：100万元  手续费：万分之3 | Cherry Studio | DeepSeek-V3.1 | ![](images/stock_mcp/example18.png) | 调用工具：查询指标元数据、指标选股、股票多因子回测、清理内存 |
| 帮我回测一个简单的低PE策略：  选股条件：主板里PE小于15大于0 + 排除掉停牌和退市风险股票  选股数量：PE最低的20只股票  调仓频率：持仓21天个交易日，周二调仓  回测时间：2023年1月1日到2023年12月31日  基准指数：沪深300  初始资金：100万  手续费：万分之1.5 | Cherry Studio | DeepSeek-V3.1 | ![](images/stock_mcp/example19.png)![](images/stock_mcp/example20.png) | 调用工具：查询指标元数据、指标选股、股票多因子回测、清理内存 |
| 帮我回测这个多条件价值策略  估值指标：0< PE < 20  净资产质量：0< PB < 2  财务健康度：资产负债率 < 60%  市场表现：非ST股票，非停牌股  流动性要求：日均成交额 > 1000万元  持仓配置：符合条件的股票中选15只资产负债率最小的，等权重  调仓周期：20个交易日调仓，周二调仓  回测时间：2020.01.01-2024.12.31  基准：沪深300指数  初始资金：200万元  手续费：万分之1.5 | Cherry Studio | DeepSeek-V3.1 | ![](images/stock_mcp/example21.png)![](images/stock_mcp/example22.png) | 调用工具：查询指标元数据、指标选股、股票多因子回测、清理内存 |
| 回测这个衍生因子策略：  股票池条件：  基础估值：PE < 25 , PB < 2.5  MACD\_DIF > 0 且 MACD\_DIF > MACD\_DEA ，close > BOLL\_UPPER\_20\_2  ma5 > ma20 的非ST股票，非停牌股  回测条件：  基准指数：沪深300  选股数量：符合条件的前25只成交量最大的股票 等权  回测日期：从2023年一月一日到2025年11月11日  调仓频率：持仓15个交易日 周三调仓  手续费：万分之一 | Cherry Studio | DeepSeek-V3.1 | ![](images/stock_mcp/example23.png)![](images/stock_mcp/example24.png) | 调用工具：查询指标元数据、指标选股、股票多因子回测、清理内存 |
| 帮我做一个小市值多因子选股策略，满足如下要求  股票只从中证 1000 指数成分股里选  按照下述条件，进一步剔除我认为高风险的坏股票  第一个条件是上市时间满 1 年  第二个条件是非 ST 股、无退市风险  第三个条件是非停牌股  第四个条件是非涨跌停股  第五个条件是主板或创业板股票  持仓条件  选多因子拟合后排名前10的票  流通市值因子：越小越好  净利润增长率：越大越好  资产负债率：越小越好  净资产收益率ROE：越大越好  回测时间范围 2020 年1月1日至2025年12月4日  初始资金为100万  指定每周二进行调仓动作，持仓周期为5个交易日  每次调仓，10只股票的持仓是等权重分配  手续费是万分之1.5 | Cherry Studio | DeepSeek-V3.1 | ![](images/stock_mcp/example25.png)![](images/stock_mcp/example26.png) | 调用工具：查询指标元数据、指标选股、股票多因子回测、清理内存 |

**DeepSeek-V3.1 使用案例**

[](videos/video_07.mp4)

**Gemini 3 Pro 使用案例**

[](videos/video_08.mp4)

**Doubao 1.5 Pro 使用案例**

[](videos/video_09.mp4)

## 其它场景案例

| 场景 | 用户提问 | 平台 | 模型 | 调用结果 | 备注 |
| --- | --- | --- | --- | --- | --- |
| 股票信息解读 | 帮忙对比分析一下300748.SZ和002202.SZ两只股票的各项指标表现 | Cherry Studio | DeepSeek-V3.1 | ![](images/stock_mcp/example27.png) | 调用工具：查询股票基础信息 |
| 投资建议 | 帮我做出一个年化10%的策略 | Cherry Studio | DeepSeek-V3.1 | ![](images/stock_mcp/example28.png)![](images/stock_mcp/example29.png) | 调用工具：查询指标元数据、股票多因子回测、股票多因子回测、清理内存 |
