<!-- Auto-mirrored from upstream `documentation-main/tutorials/ImportTLData_toturial.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 通联历史数据导入教程

通联数据的原始历史数据包含多层次市场结构与高频时序特征，因此在标准化入库过程中，需要完成库表分区设计、数据处理转换和分布式存储等多个环节。针对通联数据特有的多层次结构和高频时序特征，DolphinDB
提供了高效数据导入解决方案 —— **ImportTLData 模块**。ImportTLData
通过结构化数据处理流水线，实现了多品种金融数据的高效导入。该导入方案采用模块化设计，能够有效存储复杂的金融数据，并为量化投研提供高质量的基础数据支持。本文将详细介绍
ImportTLData 模块的实现过程及最佳实践。

目前该模块已覆盖以下几类核心数据源：

1. 证券基础行情：涵盖沪深市场股票、债券、可转债逐笔委托/成交数据及行情快照
2. 衍生品数据：包含期货期权 L2 行情快照及期货 L1 行情快照
3. 时序聚合数据：权益、债券、指数等品种 1-60 分钟多粒度 K 线数据
4. 特色数据集：深交所 ETF 实时申赎行情、指数盘后数据

注：

本教程代码基于 DolphinDB 2.00.12.5 开发，建议用户使用 2.00.12.5 及以上版本 。

## 1. 数据导入模块

### 1.1 模块结构与功能

注：

在数据导入操作中，只需调用 loadTL<DataType>.dos 这些模块里面的函数，其它均为**内部辅助**模块，其中
<DataType> 的全部取值以及含义参照附件中的**数据类别部分**。

| **模块名** | **模块功能** |
| --- | --- |
| loadTL<DataType>.dos | 定义导入通联原始数据到 DolphinDB 的函数，其中 <DataType> 为相应的数据类型 |
| createTable.dos | 定义创建相关数据库表的函数 |
| process<DataType>.dos | 定义通联原始数据结构和数据转换规则的函数，其中 <DataType> 为相应的数据类型 |
| utils.dos | 定义模块中使用的工具函数 |
| setting.dos | 定义源数据映射函数及数据导入相关辅助函数 |
| dataCheck.dos | 定义股票数据校验的函数 |

### 1.2 模块同步

下载附件中的通联数据导入模块 ImportTLData 之后，需要将其同步到服务器上。当在 DolphinDB
调用模块时，会到相应路径下查找需要的模块文件。

**同步路径**

将模块放置于**节点所在 Home 目录的 module 目录下**。节点所在 Home 目录可通过 `getHomeDir`
函数获取， 假设 Home 目录为 /DolphinDB/server，那么可以将模块文件放置于 /DolphinDB/server/modules/
路径下。

**如何同步**

* 使用 xftp 等传输软件，将模块传输至服务器上指定的路径。
* 使用 scp 命令：`scp -r ImportTLData
  <user>@<服务器ip>:/DolphinDB/server/modules/`。
* 使用 vscode 的 DolphinDB 插件，参考：VS
  Code 插件。
* 使用 DolphinDB 的 GUI 客户端，参考：GUI
  客户端。

## 2. 数据导入操作

将数据导入模块同步到服务器相应目录之后，就可以使用 DolphinDB 脚本调用该模块。使用模块中的函数可以将通联原始数据导入到 DolphinDB
数据库表中。需要操作的具体步骤有：

1. 设定所需参数，定义数据导入函数。参考附件中的 example.dos 文件，修改相应参数后直接执行即可定义相关数据导入函数。
2. 设定需要导入数据的起止时间，调用定义的导入函数，执行数据导入任务。

本部分内容首先介绍如何通过 ImportTLData 定义符合自有环境的数据导入函数，然后介绍通过前台任务、后台任务、定时任务等方式来导入历史数据和增量数据。

### 2.1 数据导入步骤

**前置条件**

* 进行数据导入之前，首先要确保目标时间段的通联原始数据压缩文件已经保存到服务器下，需要注意的是: **原始数据要保存在执行导入任务的 DolphinDB
  节点所在的服务器**。
* 需要记住原始数据保存路径，后续导入时需要将其作为参数，比如原始数据保存在：/data/20231007/<具体数据 zip 文件>
  ，那么，作为参数的路径可设为：/data。数据导入模块会在这个路径下根据数据类型和日期查找具体的数据文件。

**数据导入**

通联数据导入模块提供了多个导入函数，每个导入函数的功能为导入特定类型的通联历史数据，具体函数名和介绍参照**附件中的数据导入函数**部分。

以下部分将详细介绍**如何通过 ImportTLData 的函数**进行数据导入。所有数据导入的函数定义示例请参考附件中的 example.dos
文件。

**数据导入函数参数介绍**

每个数据导入函数的命名格式为 loadTL<DataType>，其中 <DataType>
为具体的数据类型名称。每个数据导入函数所需参数及其含义如下所示：

| **参数名** | **参数含义** |
| --- | --- |
| *userName* | DolphinDB 用户名 |
| *password* | DolphinDB 用户密码 |
| *startDate* | 数据导入开始日期 |
| *endDate* | 数据导入结束日期 |
| *dbName* | 数据库名 |
| *tableName* | 数据表名 |
| *filePath* | 数据目录，存放数据的路径 |
| *loadType* | 导入类型，如果是每日增量导入则为 “**daily**”，如果是历史批量导入则为 “**batch**” |

**返回值**

| 返回类型 | 返回值含义 |
| --- | --- |
| 表(N 行 1 列) | 表的每一行对应于相应数据导入任务中产生的一条运行日志信息 |

**数据导入示例**

以导入股票逐笔委托数据为例，分别介绍如何定义导入函数和导入数据。

* **定义导入函数**

```
// 导入模块
use ImportTLData::loadTLEntrust
// 定义数据导入函数
def loadEntrustStock(startDate, endDate, loadType){
	// 设定参数, 需根据实际情况改动
	userName = "admin"
	password = "123456"
	dbname = "dfs://level2_tl"
	tableName = "entrust"
	filePath = "/hdd/hdd3/customer/tlData/"

	// 增量导入
	if(loadType == "daily"){
		idate = today()
		infoTb = loadTLEntrustStock(userName, password, idate, idate, dbname, tableName, filePath, loadType)
	}
	// 批量导入
	else if (loadType == "batch"){
		infoTb = loadTLEntrustStock(userName, password, date(startDate), date(endDate), dbname, tableName, filePath, loadType)
	}
	return infoTb
}
```

### 2.2 通过前台任务导入数据

定义好数据导入函数之后，即可调用函数进行数据导入。

```
startDate = 2024.08.07
endDate = 2024.08.07
loadType = "batch"
infoTb = loadEntrustStock(startDate, endDate, loadType)
```

### 2.3 通过后台任务和定时任务导入数据

在实际导入操作中，历史数据批量导入通常采用**后台任务**，而每日数据增量导入采用**定时任务**的方式进行。以下以**导入股票委托历史数据和增量数据**为例依次进行介绍。

**后台任务**

通过 `submitJob` 提交后台任务导入 2023.02.01 - 2023.02.01 股票委托数据。
`submitJob` 函数的用法可参考：submitJob。

```
jobId = "loadEntrust20230201_20230201"
jobDesc = "loadEntrust20230201_20230201"
// 后台执行上文定义的 loadEntrustStock 函数
submitJob(jobId,jobDesc,loadEntrustStock{2023.02.01,2023.02.01,"batch"})
```

**定时任务**

通过 `scheduleJob` 提交定时任务导入每日增量股票委托数据。假设从 2025.01.01 -
2025.12.31，每周一到周五的 17:00 定时执行股票委托数据导入任务。 `scheduleJob` 函数的用法可参考：
scheduleJob。

```
jobId = "loadEntrustDaily"
jobDesc = "loadEntrustDaily"
scheduleTime = 17:00m
beginDate = 2025.01.01
endDate = 2025.12.31
frequency = "W"
days = [1,2,3,4,5]
​
// 设定定时任务，定时执行上文执行的 loadEntrustStock 函数
scheduleJob(jobId,jobDesc,loadEntrustStock{NULL,NULL,"daily"},scheduleTime,beginDate,endDate,frequency,days)
```

## 3. 数据导入流程与处理逻辑

### 3.1 数据导入流程

通过本模块将通联各类历史数据导入 DolphinDB ，**均经过如下步骤**：

1. 检查系统配置。由于解压数据文件需要用到 `shell` 函数，因此需要在 DolphinDB 配置文件中设置
   `enableShellFunction=true` ，如果未设置，则会报错。
2. 函数会扫描服务器上开始日期和结束日期之间交易日期的相应数据文件，如果缺失某些交易日期的数据文件，则函数会**报错，报错内容为缺失的数据文件**。需要注意的是：**必须保证
   DolphinDB 安装包的交易日历使用的是最新的版本**，否则需先更新交易日历再执行数据导入任务。
3. 如果不存在共享表
   tlDataLoadInfo，则创建。该表用于记录数据导入的信息，主要有三列，分别表示数据类别、数据文件的日期和报错信息。这个表的作用是：**可以方便查看当前的数据导入进度和报错信息**。
4. 对于每一个需要导入数据的交易日，经过如下流程：
   1. 如果 DolphinDB 中不存在相应库表，则根据相应数据类别进行**建库建表**。
   2. 如果原始数据只存在 zip 格式，则进行数据的**解压缩**操作。
   3. 如果 DolphinDB 相应数据库表中已存在即将导入的数据，则会先**删除相应数据**。
   4. 将原始数据载入到内存，进行**数据处理后导入到 DolphinDB** 相应数据库表中。
   5. 导入完成或导入报错时，执行以下操作：
      1. 将解压缩后的数据文件删除，节省磁盘空间。
      2. 更新共享表 tlDataLoadInfo，记录导入情况。

### 3.2 数据处理逻辑

**通用处理逻辑**

本文主要介绍导入通联数据到 DolphinDB 库表的数据处理逻辑。通联不同类别的原始数据存在以下特征：

* 部分原始数据在不同时间段会有所变更，比如增加新数据列、旧数据列不再使用等。
* 对于同一数据类别，如股票逐笔委托数据，上交所和深交所分别提供 csv 数据文件。

考虑到以上情况，模块中的数据处理函数做了如下设计：

* 对于每一个数据类别，考虑数据字段的历史变更，设计兼容的表结构。
* 对于同时含有上交所和深交所数据的数据类别，合并它们相同含义的表字段，并在表结构中分别添加它们的独特字段，并添加字段 Market
  用于辨识市场类别，以此将上交所和深交所的相同类别数据**导入到同一张表中**。

**快照数据处理逻辑**

由于通联的股票和债券的快照数据分成两部分，一个是快照主体数据，一个是最优买卖价前50笔委托，分别存储在不同的 csv
文件中。因此，股票和债券的快照数据处理逻辑除了遵循上文介绍的通用处理逻辑之外，还需要根据不同交易所进行以下处理：

* 如果最优买价和最优卖价前 50 笔委托数据存储在不同文件，则根据交易时间和股票 ID 进行左连接操作，合并成一张表。
* 根据交易时间和股票 ID ，将快照主体数据和最优买卖价前 50 笔委托数据进行左连接操作，合并成一张表。
* 对于当天的每一支股票， 判断 TotalVolumeTrade
  字段是否递增（该字段表示截止当前快照时间点的成交总量），如果不满足递增条件，说明快照数据存在问题，则报错。

## 4. 数据库表设计

### 4.1 原始数据文件与数据库表

通联各类历史数据文件根据一定规则命名，而且在不同时间段可能存在表结构的变化。因此，要把这些不同时间段的同一类数据导入到 DolphinDB
同一张表中，需要考虑到所有变化，并设计出兼容所有数据的库表结构。本部分详细介绍通联原始数据文件在不同时间段的文件名与含义，以及与 DolphinDB
数据库表的映射关系。其中文件名涉及到日期表示的以 **20231007** 为例：

| **默认导入数据库名** | **默认导入数据表名（数据表含义）** | **文件名** | **文件描述** |
| --- | --- | --- | --- |
| dfs://level2\_tl | entrust（沪深股票委托） | 20231007\_Order.csv | 深交所股票逐笔委托(**201005-20160506**) |
| mdl\_6\_33\_0.csv | 深交所股票逐笔委托(**20160507及之后**) |
| mdl\_4\_19\_0.csv | 上交所股票逐笔委托(**20210607-20231126**) |
| entrust/trade（上交所股票委托和股票快照） | mdl\_4\_24\_0.csv | 上交所股票合并逐笔(**20231127新增)** |
| snapshot（股票快照） | MarketData.csv | 深交所股票快照行情(**201005-20160506**) |
| OrderQueue.csv | 深交所股票最优买卖价前50笔委托(**201005-20160506**) |
| mdl\_6\_28\_0.csv | 深交所股票快照行情(**20160507及之后)** |
| mdl\_6\_28\_1.csv | 深交所股票最优卖价前50笔委托(**20160507及之后**) |
| mdl\_6\_28\_2.csv | 深交所股票最优买价前50笔委托(**20160507及之后**) |
| 20231017\_MarketData.csv | 上交所股票快照行情 |
| 20231017\_OrderQueue.csv | 上交所股票最优买卖价前50委托 |
| trade（股票成交） | mdl\_6\_36\_0.csv | 深交所股票逐笔成交(**20160507及之后**) |
| 20231017\_Trade.csv | 深交所股票逐笔成交(**201005-20160506**) |
| 20231017\_Transaction | 上交所股票逐笔成交 |
| mdl\_4\_17\_0.csv | 上交所股票盘后固定价格交易逐笔成交 |
| equityMf（权益分钟线数据） | equity\_mf20231017.txt | 权益分钟线因子 |
| dfs://level2\_tlExtra | index（沪深指数数据） | mdl\_6\_29\_0.csv | 深交所指数快照行情 |
| 20231017\_Index.csv | 上交所指数快照行情 |
| afterTrade（沪深盘后数据） | mdl\_6\_31\_0.csv | 深交所盘后定价交易业务行情快照 |
| mdl\_4\_16\_0.csv | 上交所盘后固定价格交易行情快照 |
| szTradeStat（深交所成交量统计指标） | mdl\_6\_30\_0.csv | 深交所成交量统计指标 |
| etfSellBuy（深交所 ETF 行情数据） | mdl\_6\_50\_0.csv | 深交所 ETF 实时申赎行情 |
| dfs://level2\_tlBond | entrust/trade（上交所债券逐笔委托和成交） | mdl\_4\_21\_0.csv | 上交所债券逐笔委托和成交 |
| entrust（深交所债券逐笔委托） | mdl\_6\_43\_0.csv | 深交所债券逐笔委托 |
| trade（深交所债券逐笔成交） | mdl\_6\_44\_0.csv | 深交所债券逐笔成交 |
| snapshot（沪深债券快照数据） | mdl\_4\_20\_0.csv | 上交所债券快照行情 |
| mdl\_4\_22\_0.csv | 上交所债券最优买卖价前50笔委托 |
| mdl\_6\_42\_0.csv | 深交所债券行情快照 |
| mdl\_6\_47\_0.csv | 深交所债券最优买卖价前50笔委托 |
| dfs://level2\_tlPrice1\_5Min | equityPrice1Min（权益价格 1 分钟线） | equity\_pricemin20231017.txt | equity 价格数据1分钟线因子 |
| equityPrice3Min（权益价格 3 分钟线） | equity\_price03min20231017.txt | equity 价格数据3分钟线因子 |
| equityPrice5Min（权益价格 5 分钟线） | equity\_price05min20231017.txt | equity 价格数据5分钟线因子 |
| dfs://level2\_tlPrice15\_60Min | equityPrice15Min（权益价格 15 分钟线） | equity\_price15min20231017.txt | equity 价格数据15分钟线因子 |
| equityPrice30Min（权益价格 30 分钟线） | equity\_price30min20231017.txt | equity 价格数据30分钟线因子 |
| equityPrice60Min（权益价格 60 分钟线） | equity\_price60min20231017.txt | equity 价格数据60分钟线因子 |
| dfs://level2\_tlPrice1\_5Min | bondPrice1Min（债券价格 1 分钟线） | bond\_pricemin20231017.txt | bond 价格数据1分钟线因子 |
| bondPrice3Min（债券价格 3 分钟线） | bond\_price03min20231017.txt | bond 价格数据3分钟线因子 |
| bondPrice5Min（债券价格 5 分钟线） | bond\_price05min20231017.txt | bond 价格数据5分钟线因子 |
| dfs://level2\_tlPrice15\_60Min | bondPrice15Min（债券价格 15 分钟线） | bond\_price15min20231017.txt | bond价格数据15分钟线因子 |
| bondPrice30Min（债券价格 30 分钟线） | bond\_price30min20231017.txt | bond价格数据30分钟线因子 |
| bondPrice60Min（债券价格 60 分钟线） | bond\_price60min20231017.txt | bond价格数据60分钟线因子 |
| dfs://level2\_tlPrice1\_5Min | idxPrice1Min（指数价格 1 分钟线） | idx\_pricemin20231017.txt | idx价格数据1分钟线因子 |
| idxPrice3Min（指数价格 3 分钟线） | idx\_price03min20231017.txt | idx价格数据3分钟线因子 |
| idxPrice5Min（指数价格 5 分钟线） | idx\_price05min20231017.txt | idx价格数据5分钟线因子 |
| dfs://level2\_tlPrice15\_60Min | idxPrice15Min（指数价格 15 分钟线） | idx\_price15min20231017.txt | idx价格数据15分钟线因子 |
| idxPrice30Min（指数价格 30 分钟线） | idx\_price30min20231017.txt | idx价格数据30分钟线因子 |
| idxPrice60Min（指数价格 60 分钟线） | idx\_price60min20231017.txt | idx价格数据60分钟线因子 |
| dfs://level2\_tlFutOptTick | optionTick（期权 tick 数据） | opt\_**[xsge|xsie|xzce|xdce|xgfe|ccfx]**l2\_20231017.csv | 上期所、上能所、郑商所、大商所、广期所、中金所的期权tick 行情数据 |
| futureTick（期货 tick 数据） | future\_**[xsge|xsie|xzce|xdce|xgfe|ccfx]**l2\_20231017.csv | 上期所、上能所、郑商所、大商所、广期所、中金所的期货tick行情数据 |
| dfs://level2\_tlFutOptOthers | optionTqs（期权成交量统计） | opttqs\_**[xdce|xgfe]**l2\_20231017.csv | 大商所、广期所的期权成交量统计 |
| optionOrderq（期权最优价十笔委托） | optorderq\_**[xdce|xgfe]**l2\_20231017.csv | 大商所、广期所的期权最优价十笔委托 |
| futureCmb（期货组合行情） | futcmb\_**[xzce|xdce|xgfe]**l2\_20231017.csv | 郑商所、大商所、广期所的期货组合行情 |
| futureTqs（期货成交量统计） | futtqs\_**[xdce|xgfe]**l2\_20231017.csv | 大商所、广期所的期货成交量统计 |
| futureOrderq（期货最优价十笔委托） | futorderq\_**[xdce|xgfe]**l2\_20231017.csv | 大商所、广期所的期货最优价十笔委托 |
| dfs://level2\_tlFutL1 | futureL1（期货L1数据） | future\_price20231017.zip(解压后存在多个数据文件) | 期货 L1 数据 |
| dfs://level2\_tlFutMins | min1（期货数据1分钟线） | future\_pricemin20231017.zip(解压后存在多个数据文件) | 期货1分钟线数据 |

### 4.2 部分数据表结构

以下列出了通联数据中股票逐笔委托、行情快照、逐笔成交表的详细字段名、字段类型和字段含义。

**股票委托(dfs://level2\_tl : entrust)**

| 字段名 | 字段类型 | 字段含义 |
| --- | --- | --- |
| ChannelNo | INT | 频道代码 |
| ApplSeqNum | LONG | 消息记录号，从 1 开始计数 |
| MDStreamID | INT | 行情类别：   * 011 现货（股票，基金，债券等）集中竞价交易逐笔行情 * 021 质押式回购交易逐笔行情 |
| SecurityID | SYMBOL | 证券代码 |
| SecurityIDSource | INT | 证券代码源 |
| Price | DOUBLE | 委托价格 |
| OrderQty | INT | 委托数量 |
| Side | SYMBOL | 买卖方向：   * 深交所：   + B -买单   + S -卖单 * 上交所：   + 若为新增或删除委托订单：     - B -买单     - S -卖单   + 若为产品状态订单：     - START 启动     - OCALL 开市集合竞价     - TRADE 连续自动撮合     - SUSP 停牌     - CCALL 收盘集合竞价     - CLOSE 闭市     - ENDTR 交易结束 |
| TradeTime | TIMESTAMP | 委托时间 |
| OrderType | SYMBOL | 订单类别：   * 深交所：   + ‘1’=市价   + ‘2’=限价   + ‘U’=本方最优 * 上交所：   + A-新增委托订单   + D-删除委托订单 |
| OrderIndex | INT | 委托序号 |
| LocalTime | TIME | 接收时间戳 |
| SeqNo | LONG | 接收序列号 |
| Market | SYMBOL | 交易所代号：sz | sh |
| DataStatus | INT | 数据状态 |
| BizIndex | LONG | 业务序列号 |
| TradedQty | DOUBLE | 已成交的委托数量 |

**股票快照(dfs://level2\_tl : snapshot)**

| 字段名 | 字段类型 | 字段含义 |
| --- | --- | --- |
| Market | SYMBOL | 交易所代号：sz | sh |
| TradeTime | TIMESTAMP | 数据生成时间 |
| MDStreamID | INT | 行情类别:   * 010 现货（股票，基金，债券等）集中竞价交易快照行 * 020 质押式回购交易快照行情 * 030 债券分销快照行情 |
| SecurityID | SYMBOL | 证券代码 |
| NumImageStatus | INT | 快照状态（2015.08.24 之前值为空）：   * 1: 全量行情 * 2: 增量行情，客户端不会接收到该值 * 3: 增量和上一次全量合并后的行情 |
| SecurityIDSource | INT | 证券代码源 |
| TradingPhaseCode | SYMBOL | 产品所处的交易阶段代码   * 第 0 位：   + S=启动（开市前）   + O=开盘集合竞价   + T=连续竞价   + B=休市   + C=收盘集合竞价   + E=已闭市   + H=临时停牌   + A=盘后交易   + V=波动性中断 * 第 1 位：   + 0=正常状态   + 1=全天停牌 |
| PreCloPrice | DOUBLE | 昨收价 |
| NumTrades | INT | 成交笔数 |
| TotalVolumeTrade | LONG | 成交总量 |
| TotalValueTrade | DOUBLE | 成交总金额 |
| LastPrice | DOUBLE | 最新价 |
| OpenPrice | DOUBLE | 开盘价 |
| HighPrice | DOUBLE | 最高价 |
| LowPrice | DOUBLE | 最低价 |
| ClosePrice | DOUBLE | 今收盘价 |
| DifPrice1 | DOUBLE | 升跌 1（最新价-昨收价） |
| DifPrice2 | DOUBLE | 升跌 2（最新价-上一最新价） |
| PE1 | DOUBLE | 股票市盈率 1 |
| PE2 | DOUBLE | 股票市盈率 2 |
| PreCloseIOPV | DOUBLE | 基金 T-1 日净值 |
| IOPV | DOUBLE | 基金实时参考净值（包括 ETF的 IOPV） |
| TotalBidQty | LONG | 委托买入总量（有效竞价范围内） |
| WeightedAvgBidPx | DOUBLE | 加权平均买入价格（有效竞价范围内） |
| TotalOfferQty | LONG | 委托卖出总量（有效竞价范围内） |
| WeightedAvgOfferPx | DOUBLE | 加权平均卖出价格（有效竞价范围内） |
| UpLimitPx | DOUBLE | 涨停价，999999999.9999 表示无涨停价格限制。 |
| DownLimitPx | DOUBLE | 跌停价，对于价格可以为负数的业务，-999999999.9999 表示无跌停价格限制 |
| OpenInt | LONG | 持仓量 |
| OptPremiumRatio | DOUBLE | 权证溢价率 |
| OfferPrice | DOUBLE[] | 申卖价10档 |
| BidPrice | DOUBLE[] | 申买价10档 |
| OfferOrderQty | LONG[] | 申卖量10档 |
| BidOrderQty | LONG[] | 申买量10档 |
| BidNumOrders | LONG[] | 申买委托笔数10档 |
| OfferNumOrders | LONG[] | 申卖委托笔数10档 |
| ETFBuyNumber | INT | ETF 申购笔数 |
| ETFBuyAmount | LONG | ETF 申购数量 |
| ETFBuyMoney | DOUBLE | ETF 申购金额 |
| ETFSellNumber | INT | ETF 赎回笔数 |
| ETFSellAmount | LONG | ETF 赎回数量 |
| ETFSellMoney | DOUBLE | ETF 赎回金额 |
| YieldToMatu | DOUBLE | 债券到期收益率 |
| WithdrawBuyNumber | INT | 买入撤单笔数 |
| WithdrawBuyAmount | LONG | 买入撤单数量 |
| WithdrawBuyMoney | DOUBLE | 买入撤单金额 |
| WithdrawSellNumber | INT | 卖出撤单笔数 |
| WithdrawSellAmount | LONG | 卖出撤单数量 |
| WithdrawSellMoney | DOUBLE | 卖出撤单金额 |
| TotalBidNumber | INT | 买入总笔数 |
| TotalOfferNumber | INT | 卖出总笔数 |
| MaxBidDur | INT | 买入委托成交最大等待时间 |
| MaxSellDur | INT | 卖出委托最大等待时间 |
| BidNum | INT | 买方委托价位数 |
| SellNum | INT | 卖方委托价位数 |
| LocalTime | TIME | 接收时间戳 |
| SeqNo | INT | 接收序列号 |
| OfferOrders | LONG[] | 委卖量50档 |
| BidOrders | LONG[] | 委买量50档 |

**股票成交(dfs://level2\_tl : trade)**

| 字段名 | 字段类型 | 字段含义 |
| --- | --- | --- |
| ChannelNo | INT | 频道代码 |
| ApplSeqNum | LONG | 消息记录号，从 1 开始计数 |
| MDStreamID | INT | 行情类别：  * 011 现货（股票，基金，债券等）集中竞价交易逐笔行情 * 021 质押式回购交易逐笔行情 |
| BidApplSeqNum | INT | 买方委托索引：从 1 开始计数， 0 表示无对应委托 |
| OfferApplSeqNum | INT | 卖方委托索引：从 1 开始计数， 0 表示无对应委托 |
| SecurityID | SYMBOL | 证券代码 |
| SecurityIDSource | INT | 证券代码源 |
| TradePrice | DOUBLE | 成交价格 |
| TradeQty | LONG | 成交数量 |
| ExecType | INT | 成交类别：  * ‘4’=撤销 (本地 ASCII 码自动转码为 52) * ‘F’=成交 (本地 ASCII 码自动转码为 70) |
| TradeTime | TIMESTAMP | 成交时间 |
| LocalTime | TIME | 接收时间戳 |
| SeqNo | INT | 接收序列号 |
| TradeBSFlag | SYMBOL | 标识：  * B 外盘 主动买 * S 内盘 主动卖 * N 未知 |
| Market | SYMBOL | 交易所代号：sz | sh |
| DataStatus | INT | 数据状态 |
| TradeIndex | INT | 成交序号 |
| TradeMoney | DOUBLE | 成交金额 |
| BizIndex | LONG | 逐笔序号：从 1 开始，按 Channel 连续 |

## 5. 常见问题

### 5.1 是否可以并发执行同一时间段多个数据导入任务？

可以。

假设要将 2023.01.01 - 2023.11.01 这一时间段内的股票委托数据、股票快照数据、股票成交数据、指数数据、盘后数据以及 equity
分钟线数据同时导入 DolphinDB 。由于每个任务导入不同的数据表，不会产生冲突，因此修改参数之后就可以直接通过后台任务并发执行多个数据导入任务。

需要注意的是，在并发导入过程中应**注意内存情况**，避免产生内存溢出。

### 5.2 是否可以根据时间段的不同，并发执行同一数据导入任务？

依情况而定。

DolphinDB
按分区存储数据。当一个写入任务涉及多个分区时，系统会首先锁定这些分区。如果在该任务完成之前，其他写入任务也涉及这些分区，由于锁定状态，这些任务会因分区冲突而报错
S00002，从而导致任务失败。

尽管数据导入任务已根据不同时间段划分，但仍可能出现因同时写入同一分区而导致冲突的情况。接下来，我们将介绍每个库的分区类型，并探讨如何设计并发任务以避免分区冲突。

**分区类型**

| 库名 | 分区类型 | 时间分区粒度 |
| --- | --- | --- |
| dfs://level2\_tl | 复合分区，第一层为按日划分的值分区，第二层为按证券代号划分的哈希分区 | 日 |
| dfs://level2\_tlBond | 复合分区，第一层为按日划分的值分区，第二层为按证券代号划分的哈希分区 | 日 |
| dfs://level2\_tlExtra | 按日划分的值分区 | 日 |
| dfs://level2\_tlEquity1\_5Min | 按月划分的值分区 | 月 |
| dfs://level2\_tlEquity15\_60Min | 按年划分的范围分区 | 年 |
| dfs://level2\_tlETF | 按月划分的值分区 | 月 |
| dfs://level2\_tlFutOptTick | 复合分区，第一层为按日划分的值分区，第二层为按证券代号划分的哈希分区 | 日 |
| dfs://level2\_tlFutOptOthers | 按日划分的值分区 | 日 |
| dfs://level2\_tlFutL1 | 按日划分的值分区 | 日 |
| dfs://level2\_tlFutMins | 按五年划分的范围分区 | 五年 |

**避免分区冲突**

根据以上每个数据库的分区类型可以得知，dfs://level2\_tl 和 dfs://level2\_tlExtra
的时间分区粒度为日，所以不用担心分区冲突问题，只需保证多个并发任务之间的时间段不产生重合即可。

dfs://level2\_tlEquity1\_5Min 以月分区。为了避免分区冲突，应保证每个任务的导入时间段不产生月份重合。假设任务 A 的导入时间段为
`2023.01.01 - 2023.01.15` ，任务B的导入时间段为 `2023.01.16 -
2023.02.15` ，会产生分区冲突。应该改为：任务 A 的导入时间段为 `2023.01.01 -
2023.01.31` ，任务 B 的导入时间段为 `2023.02.01 -
2023.02.15`。

以此类推，dfs://level2\_tlEquity15\_60Min 以年分区，为了避免分区冲突，应保证每个任务的导入时间段不产生年份重合，假设任务 A
的导入时间段为 `2023.01.01 - 2023.05.15` ，任务B的导入时间段为 `2023.05.16
- 2024.04.15`，会产生分区冲突，应该改为：任务 A 的导入时间段为 `2023.01.01 -
2023.12.31` ，任务 B 的导入时间段为 `2024.01.01 -
2024.04.15`。

### 5.3 如何获取具体数据导入任务的运行信息？

**前台任务**

以深交所交易统计数据导入为例，通过以下代码获取数据导入任务的运行信息：

```
infoTb = loadSZTradeStat(startDate, endDate, loadType)
```

这里的 infoTb 为一张表。该表只有一列 msg ，每一行记录深交所交易统计数据导入过程中的每一条运行信息：

| msg |
| --- |
| 2024.08.08T10:30:09.862 : [info]-[szTradeStat]-[20230206\_20230206]: ---------------------- [BEGIN] ---------------------- |
| 2024.08.08T10:30:09.904 : [info]-[szTradeStat]-[20230206\_20230206]: 开始载入2023.02.06\_2023.02.06 [szTradeStat] ... |
| 2024.08.08T10:30:09.905 : [warn]-[szTradeStat]-[20230206\_20230206]: 2023.02.06 缺失数据文件, 但是存在相应压缩文件, 共 1 个文件, 正在解压中... |
| 2024.08.08T10:30:10.189 : [info]-[szTradeStat]-[20230206\_20230206]: 已解压 1 / 1 个文件... |
| 2024.08.08T10:30:12.190 : [info]-[szTradeStat]-[20230206\_20230206]: [checkSuccess] 依赖的 csv 文件全部存在, 准备进行导入操作... |
| 2024.08.08T10:30:12.192 : [info]-[szTradeStat]-[20230206\_20230206]: 即将导入 20230206/mdl\_6\_30\_0.csv 到内存... |
| 2024.08.08T10:30:12.244 : [info]-[szTradeStat]-[20230206\_20230206]: 导入 20230206/mdl\_6\_30\_0.csv 到内存成功, 即将根据规则处理该表... |
| 2024.08.08T10:30:12.340 : [info]-[szTradeStat]-[20230206\_20230206]: 20230206/mdl\_6\_30\_0.csv 处理成功！处理前共 43863 条数据, 处理后共 43863 条数据... |
| 2024.08.08T10:30:12.342 : [info]-[szTradeStat]-[20230206\_20230206]: 库表在当前日期无数据，跳过删除... |
| 2024.08.08T10:30:12.461 : [info]-[szTradeStat]-[20230206\_20230206]: 成功入库 , 导入: dfs://level2\_tlExtra szTradeStat 共 43863条数据... |
| 2024.08.08T10:30:12.462 : [info]-[szTradeStat]-[20230206\_20230206]: 20230206szTradeStat导入成功！ |
| 2024.08.08T10:30:12.464 : [info]-[szTradeStat]-[20230206\_20230206]: 准备删除已有的 csv 数据文件共 1 个... |
| 2024.08.08T10:30:12.717 : [info]-[szTradeStat]-[20230206\_20230206]: 删除成功... |
| 2024.08.08T10:30:12.717 : [info]-[szTradeStat]-[20230206\_20230206]: [success]2023.02.06\_2023.02.06szTradeStat载入成功... |
| 2024.08.08T10:30:12.717 : [info]-[szTradeStat]-[20230206\_20230206]: ---------------------- [END] ---------------------- |

**后台任务和定时任务**

* 获取后台任务的状态

  ```
  getRecentJobs()
  ```
* 通过以上函数返回的结果查询所需的 jobId ，再通过以下函数获取相应的运行信息
  + `getJobMessage(jobId)` ：以字符串形式返回运行信息
  + `getJobReturn(jobId)` ：以表的形式返回运行信息

## 附件

### 数据类别

| **数据类别名** | **含义** |
| --- | --- |
| Entrust | 沪深股票、债券委托数据 |
| Snapshot | 沪深股票、债券快照数据 |
| Trade | 沪深股票、债券成交数据 |
| Equity | 权益数据 |
| Extra | 沪深指数、盘后、深交所成交量统计指标数据 |
| ETFBuySell | 深交所ETF基金实时申购赎回数据 |
| FutureOption | 期货期权数据 |

### 数据导入函数

| **函数名** | **功能** |
| --- | --- |
| `loadTLEntrustStock` | 导入沪深股票委托数据 |
| `loadTLEntrustBond` | 导入沪深债券委托数据 |
| `loadTLEntrustCbond` | 导入沪深可转债委托数据 |
| `loadTLSnapshotStock` | 导入沪深股票快照数据 |
| `loadTLSnapshotBond` | 导入沪深债券快照数据 |
| `loadTLSnapshotCbond` | 导入沪深可转债快照数据 |
| `loadTLTradeStock` | 导入沪深股票成交数据 |
| `loadTLTradeBond` | 导入沪深债券成交数据 |
| `loadTLTradeCbond` | 导入沪深可转债成交数据 |
| `loadTLIndex` | 导入沪深指数数据 |
| `loadTLAfterTrade` | 导入沪深盘后数据 |
| `loadTLSzTradeStat` | 导入深交所成交量统计指标数据 |
| `loadTLETFBuySell` | 导入深交所ETF基金实时申购赎回数据 |
| `loadTLEquityMf` | 导入权益分钟数据 |
| `loadTLEquity1_5Min` | 导入权益价格 1、3、5 分钟线数据 |
| `loadTLEquity15_60Min` | 导入权益价格 15、30、60 分钟线数据 |
| `loadTLBond1_5Min` | 导入债券价格 1、3、5 分钟线数据 |
| `loadTLBond15_60Min` | 导入债券价格 15、30、60 分钟线数据 |
| `loadTLIdx1_5Min` | 导入指数价格 1、3、5 分钟线数据 |
| `loadTLIdx15_60Min` | 导入指数价格 15、30、60 分钟线数据 |
| `loadTLFutTick` | 导入期货 L2 tick 数据 |
| `loadTLFutCmb` | 导入期货 L2 组合行情 |
| `loadTLFutOrderq` | 导入期货 L2 最优价十笔委托 |
| `loadTLFutTqs` | 导入期货 L2 成交量统计 |
| `loadTLOptTick` | 导入期权 L2 tick 数据 |
| `loadTLOptOrderq` | 导入期权 L2 最优价十笔委托 |
| `loadTLOptTqs` | 导入期权 L2 成交量统计 |
| `loadTLFutL1` | 导入期货 L1 数据 |
| `loadTLFut<1,3,5,15,30,60>Min` | 导入期货 1、3、5、15、30、60 分钟线数据 |

### 通联历史数据导入模块与脚本

* 通联历史数据导入模块：[ImportTLData.zip](https://cdn.dolphindb.cn/zh/tutorials/script/ImportTLData_toturials/ImportTLData.zip)
* 数据导入函数定义示例脚本：[example.dos](https://cdn.dolphindb.cn/zh/tutorials/script/ImportTLData_toturials/example.dos)
