<!-- Auto-mirrored from upstream `documentation-main/mcp/tools.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 工具列表

目前发布的 MCP 工具主要包含：

* **通用工具：**临时内存变量清理、CSV 导出、获取最新交易日等
* **行业数据：**自动查询行业相关数据
* **股票数据：**自动获取个股数据
* **投研能力：**指标选股、因子评价、多因子选股策略回测等

如果您有其它需求或希望新增工具，可以添加小助手进入交流群，随时反馈您的需求，我们将持续优化工具库。

| 分组 | 工具/接口名称 | 描述 | 提问示例 |
| --- | --- | --- | --- |
| **通用工具** | `clean_memory` | 清理投研过程中产生的中间表 | 清理投研过程中产生的所有中间表，释放内存 |
| `export_table_to_csv` | 将共享内存表导出为 CSV 文件，并返回 HTTP 下载链接。 | 将共享内存表导出为 csv 文件 |
| `get_date_info` | 获取系统当前日期和 day\_factor 表中的最新交易日期。 | 告诉我最新交易日期 |
| **行业数据** | `get_industry_code_by_name` | 从 DolphinDB 股票基础信息表 stock\_index\_basic 中，根据指定关键字获取模糊匹配的行业板块代码 ，并将结果保存为共享内存表。返回结果包括 ts\_code，name 两列。 | 告诉我银行行业板块的代码 |
| `select_industries_by_factors` | 根据用户输入的指标和筛选条件进行行业选择。所用指标必须存在于moneyflow\_ind\_ths 表中。 | 帮我筛选出2025年11月20日资金净流入最大的行业板块 |
| **股票数据** | `get_financial_statements_balancesheet` | 获取资产负债表信息，支持按季度或年度返回。 | 告诉我000001.SZ 的2024年的营收和总资产 |
| `get_industry_info` | 从 DolphinDB 指数基础信息表 index\_basic 中加载指定指数代码的基础信息。 | 告诉我000134.SH的基本信息 |
| `get_industry_moneyflow` | 获取行业维度的资金流向，分析板块热度与轮动趋势。 | 告诉我881101.TI昨天资金流入多少 |
| `get_financial_statements_cashflow` | 根据股票代码和日期获取对应的现金流表现数据，包括经营、投资、融资活动等，并将结果保存为共享内存表。 | 告诉我00001.SZ 2024年的现金有多少 |
| `get_financial_statements_income` | 根据股票代码和日期获取对应的财务表现数据，包括收入、利润等，并将结果保存为共享内存表。 | 告诉我00001.SZ 2024年的净利润有多少 |
| `get_stock_basic_info` | 获取单只或多只股票的基础信息（代码、名称、行业、市值、上市日期、退市日期等）。 | 我要 000001.SZ 的基本资料 |
| `get_stock_code_by_name` | 从 DolphinDB 股票基础信息表 stock\_basic 中，根据指定股票名关键字获取模糊匹配的股票代码 ，并将结果保存为共享内存表。返回结果包括 ts\_code，symbol 和 name三列。 | 查看贵州茅台的股票代码 |
| `get_stock_daily_prev` | 获取指定股票代码和日期范围的每日行情数据，包括开盘价、收盘价、最高价、最低价等。 | 查询 600519.SH 和 000001.SZ 在 2025-01-01 至 2025-01-02 的每日行情数据 |
| `get_stock_info` | 获取指定股票代码和日期范围的更多基础信息，包括股本、资产、净利率等。 | 查询 600519.SH 和 000001.SZ 在 2025-01-01 至 2025-01-02 的基础信息” |
| `get_stock_moneyflow` | 获取单只股票资金流向（主力净流入、超大单买入、散户流出等），可按日、周、月聚合。 | 今天 [300750.SZ](http://300750.sz/) 主力资金净流入是多少 |
| `search_stock_factor_meta_by_keywords` | 从 DolphinDB 股票因子元数据表中混合检索与指定关键词相关的因子信息。该工具支持通过多个关键词（以空格分隔）进行关键词匹配 + 向量检索，快速定位库内的因子定义及其描述信息。 | 告诉我净利润的相关因子信息 |
| **投研工具** | `create_backtest_config` | 用于创建量化回测策略配置，将配置参数插入到 backtest\_config 表中。所有配置项均为 JSON 格式字符串。 | 帮我创建一个选股策略配置，满足如下要求:  股票只从上中证1000指数成分股里选  按照下述条件，进一步剔除我认为高风险的坏股票  。第一个条件是上市时间满1年  。第二个条件是非 ST 股、无退市风险  。第三个条件是非停牌股  。第四个条件是非涨跌停股  。第五个条件是主板或创业板股票  持仓条件  。选多因子拟合后排名前10的票  。流通市值因子:越小越好  。股息率(%):越大越好  回测时间范围 2020 年1月1日至今  调仓周期是5个交易日，指定每周二进行调仓动作  每次调仓，10只股票的持仓是等权重分配 |
| `evaluate_stock_factor` | 评估指定因子在不同行业中的表现，支持计算因子收益、IC（信息系数）、因子分层收益及多空组合收益。 | 评价一下ROE这个因子在银行板块的表现 |
| `run_backtest` | 根据回测 ID 执行回测。 | 根据`BT_20251121_155600`去回测。 |
| `select_stocks_by_conditions` | 根据用户输入的筛选条件进行股票选择。 | 帮我筛选出roe>10%，pe>10的股票 |

当前 Stock MCP 项目所使用的全部 DolphinDB 建库建表脚本和 MCP 工具的注册代码均通过 github/gitee 进行维护更新，可点击 <https://github.com/dolphindb/StockMCP> 或
<https://gitee.com/dolphindb/StockMCP>
进行查看。
