# CN ↔ EN keyword map

DolphinDB's upstream docs, tutorials, and real-world user questions
frequently mix Chinese and English. This page maps common Chinese
technical terms to their English DolphinDB equivalent and points to the
relevant skill doc.

## Contents
- SQL / language
- Database / storage
- Streaming
- Backtest / quant finance
- Data types
- Plugins / connectors
- Operations / errors

---

## SQL / language

| 中文 | English | Doc |
|------|---------|-----|
| 向量化 / 分组向量化           | `context by`            | `20-sql/context-by.md` |
| 分组聚合                      | `group by`              | `20-sql/group-by.md` |
| 透视                          | `pivot by`              | `20-sql/pivot-by.md` |
| 窗口函数 / 分析函数           | window function / `over ... order by` | `20-sql/window-functions.md` |
| 连接 / 内连接                 | `ej` / equi join        | `20-sql/joins-overview.md` |
| 左连接                        | `lj` / left join        | `20-sql/joins-overview.md` |
| 时间连接 / asof 连接          | `aj` / asof join        | `20-sql/asof-join.md` |
| 窗口连接                      | `wj` / window join      | `20-sql/asof-join.md` |
| 元编程 / 元代码 / 宏          | metaprogramming / metacode | `10-language/metaprogramming.md` |
| 状态函数 / 有状态函数         | `@state` function       | `backtest/factors.md` |
| JIT 编译                      | `@jit`                  | `70-perf/jit-guide.md` |
| 模块 / 引用 / 使用            | `module` / `use`        | `10-language/modules.md` |
| 高阶函数 / 偏函数应用         | higher-order / partial application `{}` | `10-language/functions.md` |
| 字典                          | dict / dictionary       | `10-language/dict.md` |
| 表                            | table (in-memory) / DFS table | `10-language/data-forms.md`, `30-database/dfs-database.md` |
| 空值 / 判空                   | NULL / `isValid`        | `10-language/null-handling.md` |

## Database / storage

| 中文 | English | Doc |
|------|---------|-----|
| 分布式表 / 分区表             | DFS / partitioned table | `30-database/dfs-database.md` |
| 分区方案                      | partitioning scheme     | `30-database/partitioning.md` |
| 值分区 / 范围 / 哈希 / 列表 / 组合 | VALUE / RANGE / HASH / LIST / COMPO | `30-database/partitioning.md` |
| TSDB 引擎                     | TSDB engine             | `30-database/tsdb-engine.md` |
| OLAP 引擎                     | OLAP engine             | `30-database/olap-engine.md` |
| 主键引擎 / PKEY               | PKEY engine (upsert)    | `30-database/pkey-engine.md` |
| 内存 OLTP 引擎                | IMOLTP engine           | upstream `imoltp_*` |
| 文本引擎 / TextDB             | TextDB engine           | upstream `textdb.md` |
| 排序列                        | `sortColumns`           | `30-database/tsdb-engine.md` |
| 保留重复                      | `keepDuplicates`        | `30-database/tsdb-engine.md` |
| 分区裁剪                      | partition pruning       | `70-perf/partition-pruning.md` |
| 存算分离                      | storage-compute separation | `tutorials/best_practice_for_storage_compute_separation.md` |
| 备份 / 恢复                   | backup / restore        | `90-admin/backup-restore.md` |
| 重平衡                        | rebalance               | `tutorials/Data_Move_Rebalance.md` |

## Streaming

| 中文 | English | Doc |
|------|---------|-----|
| 流表 / 流数据表               | stream table            | `40-streaming/stream-table.md` |
| 订阅                          | subscribe / `subscribeTable` | `40-streaming/subscribe.md` |
| 发布                          | publish                 | `40-streaming/stream-table.md` |
| 响应式状态引擎                | reactive state engine   | `40-streaming/engine-selection.md` |
| 时间序列引擎                  | time-series engine      | `40-streaming/engine-selection.md` |
| 横截面引擎                    | cross-sectional engine  | `40-streaming/engine-selection.md` |
| 异步复制                      | async replication       | `tutorials/async_replication.md` |
| 复杂事件处理 / CEP            | CEP                     | `40-streaming/cep-overview.md` |
| 历史回放                      | historical replay       | `40-streaming/replay.md` |
| 异常检测 / 规则引擎           | anomaly / rule engine   | `40-streaming/engines.md` |
| 告警                          | alert                   | `tutorials/streaming_engine_anomaly_alerts.md` |

## Backtest / quant finance

| 中文 | English | Doc |
|------|---------|-----|
| 回测 / 策略回测               | backtest                | `backtest/README.md` |
| 回测插件                      | Backtest plugin         | `backtest/backtest-plugin-guide.md` |
| 撮合引擎 / 撮合模拟           | matching engine / MatchingEngineSimulator | `backtest/matching-engine-guide.md` |
| 订单管理引擎 / OME            | Order Management Engine | `plugins/order_management_engine.md` |
| 模拟交易所                    | simulatedexchangeengine | `plugins/simulatedexchangeengine.md` |
| 因子                          | factor / alpha          | `backtest/factors.md` |
| 前视偏差                      | look-ahead bias         | `backtest/traps.md` |
| 滑点 / 手续费 / 佣金          | slippage / commission   | `backtest/backtest-plugin-guide.md` |
| 保证金 / 融资融券             | margin / margin-trading | `backtest/assets.md` |
| 开仓 / 平仓 / 多头 / 空头     | open / close / long / short | `patterns/backtest-signal-to-order.md` |
| 结算                          | settlement              | `backtest/assets.md` |
| 期货 / 期权 / 债券            | future / option / bond  | `backtest/assets.md` |
| 挂单 / 限价单 / 市价单        | limit / market order    | `backtest/backtest-plugin-guide.md` |
| CTA 策略                      | CTA strategy            | `tutorials/cta_strategy_implementation_and_backtesting.md` |
| 多因子                        | multi-factor            | `tutorials/best_practices_for_multi_factor.md` |
| IC / 分位回测                 | rank-IC / quantile backtest | `backtest/factors.md` |
| 组合优化 / MVO / SOCP         | portfolio optimization  | `tutorials/MVO.md`, `tutorials/socp_usage_case.md` |
| 指数 / 股票 / 现金            | index / stock / cash    | `backtest/assets.md` |

## Data types

| 中文 | English |
|------|---------|
| 布尔 / 字符 / 短整 / 整型 / 长整 | BOOL / CHAR / SHORT / INT / LONG |
| 浮点 / 双精度                  | FLOAT / DOUBLE |
| 精确小数                       | DECIMAL32 / DECIMAL64 / DECIMAL128 |
| 字符串 / 符号                  | STRING / SYMBOL |
| 日期 / 月 / 时间 / 时间戳      | DATE / MONTH / TIME / TIMESTAMP |
| 纳秒时间戳                     | NANOTIMESTAMP |
| 数据形式（标量/向量/矩阵/表/字典/集合/元组/张量） | scalar / vector / matrix / table / dict / set / tuple / tensor |

## Plugins / connectors

| 中文 | English | Doc |
|------|---------|-----|
| 插件                          | plugin                  | `plugins/README.md` |
| 内置模块                      | built-in module         | `modules/README.md` |
| 行情插件                      | market-data plugin      | `plugins/README.md` (market data section) |
| 华鑫证券 / INSIGHT           | HuaXin INSIGHT          | `plugins/insight/` |
| 上交所行情文件                | SSE quotation file      | `plugins/SSEQuotationFile.md` |
| 万得 Wind                     | Wind TDF                | `plugins/windtdf.md` |
| 上期技术 CTP                  | CTP                     | `plugins/ctp.md` |
| 中信建投 XTP                  | XTP                     | `plugins/xtp.md` |
| 订单簿快照                    | orderBookSnapshot       | `tutorials/orderBookSnapshotEngine.md` |
| 消息队列 / Kafka / MQTT       | messaging               | `50-ingestion/kafka-mqtt.md` |

## Operations / errors

| 中文 | English | Doc |
|------|---------|-----|
| 错误码 / 报错 / 异常          | error code / RefId / exception | `reference/error-codes/INDEX.md`, `10-language/error-handling.md` |
| 权限 / 用户 / 角色            | ACL / user / role       | `90-admin/security.md` |
| 集群 / 控制节点 / 数据节点    | cluster / controller / data node | `90-admin/cluster.md` |
| 计算节点                      | compute node            | `tutorials/Compute_Node.md` |
| 调度任务 / 定时任务           | scheduled job           | `patterns/scheduled-job-template.md` |
| 监控                          | monitoring              | `tutorials/cluster_monitor.md` |
| 日志                          | log                     | `tutorials/log_analysis_tool_user_manual.md` |
| 内存 / OOM                    | memory / OOM            | `70-perf/memory-threading.md`, `tutorials/oom_settlement.md` |
| 线程 / worker                 | threading / worker      | `70-perf/memory-threading.md` |
| 查询优化 / EXPLAIN            | query optimization / `explain` | `70-perf/query-optimization.md`, `70-perf/slow-query-diagnosis.md` |
| 备份 / 恢复                   | backup / restore        | `90-admin/backup-restore.md` |

## See also

- `cheatsheet.md` — compressed top-traps reference.
- `../SKILL.md` — full routing table.
