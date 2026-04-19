<!-- Auto-mirrored from upstream `documentation-main/tutorials/log_searcher.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# DolphinDB 聚合日志搜索工具使用手册

DolphinDB 提供了聚合日志搜索工具模块 LogSearcher 来实现方便地读取和保存集群各个节点的日志。在向 DolphinDB 技术支持反馈问题时，建议使用
LogSearcher 模块读取问题发生时间段的日志，并打包发送给技术支持来排查问题。模块的具体功能包括：

* 支持多种搜索模式，包括关键词匹配和正则表达式匹配等。
* 支持多种日志类型，包括运行日志，查询日志，写入日志等。
* 支持指定时间范围。
* 支持使用搜索结果缓存来加速重复的搜索。
* 支持保存搜索结果到指定目录。
* 支持在数据节点或计算节点下线时，自动通过在线的 agent 节点读取日志。

## 1. 环境配置

自 2.00.17 和 3.00.4 版本开始，DolphinDB 安装包的 server/modules 目录下已预装
LogSearcher.dom。若是从旧版本升级至最新版，需要手动拷贝 server/modules/LogSearcher.dom 至节点的
[home]/modules 目录下。其中 [home] 目录由系统配置参数 home 决定，可以通过 `getHomeDir()`
函数查看。

更多 DolphinDB 模块的说明，请参阅 DolphinDB 教程：模块。

**注**：LogSearcher.dos 模块兼容 DolpinDB server V2.00.17/V3.00.4 及以上版本。

## 2. 快速使用

首先加载模块，后续脚本均在加载模块后执行：

```
use LogSearcher
```

搜索集群所有节点的过去 24 小时的所有类型的日志：

```
log = searchLog()
```

搜索指定节点（P1-dnode1,
P2-dnode1）的指定时间范围（2025.05.15T00:00:00.000~2025.05.17T00:00:00.000）的包含指定关键字（subscription）的指定等级（ERROR）的运行日志：

```
params = {
    "node": ["P1-dnode1", "P2-dnode1"],
    "startTime": 2025.05.15T00:00:00.000,
    "endTime": 2025.05.17T00:00:00.000,
    "pattern": ["subscription"],
    "logLevel": "ERROR",
    "logType": ["running"]
}
log = searchLog(params)
```

搜索结果示例：

| timestamp | logLevel | node | logType | logFile | content |
| --- | --- | --- | --- | --- | --- |
| 2025.05.16 10:23:07.108123000 | ERROR | P2-dnode1 | running | /hdd/hdd8/ddb\_deploy/server/clusterDemo/log/P2-dnode1.log | 2025-05-16 10:23:07.108123000,cef1 <ERROR> :AsynchronousSubscriberImp::run Shut down the subscription daemon. |

保存日志到指定目录：

```
params["saveDir"] = "/tmp/ddbLog"
saveLog(log, params)
```

保存结果示例：

```
$ tree /tmp/ddbLog/LogSearcher_3.00.4_20250515000000_20250517000000_2025052091727836
/tmp/ddbLog/LogSearcher_3.00.4_20250515000000_20250517000000_2025052091727836
├── 192.168.100.43
│   ├── controller.log
│   └── P1-dnode1.log
├── 192.168.100.44
│   ├── controller.log
│   ├── core.59174.2025051664140780.log
│   ├── dmesg.log
│   ├── P2-dnode1_audit.log
│   ├── P2-dnode1_job.log
│   ├── P2-dnode1.log
│   └── P2-dnode1_query.log
└── 192.168.100.45
    ├── controller.log
    └── P3-dnode1.log
```

## 3. 函数说明

### 3.1 searchLog

**语法**

```
searchLog(params=NULL)
```

**详情**

根据关键字聚合搜索指定时间范围的指定类型的日志。

**参数**

* params: 字典，搜索条件。默认值为 NULL，表示读取 1 天前的所有节点的所有类型的日志。字段说明：
  + pattern: 字符串标量或向量，搜索的模式字符串。为向量时，将使用或运算来组合多个模式。默认值为空，表示不做过滤。
  + startTime: 时间戳，日志开始时间。默认值为当前时间 - 1 天。
  + endTime: 时间戳，日志结束时间。默认值为当前时间。
  + logLevel: 字符串标量或向量，日志等级。默认值为所有等级。可选值：
    - INFO
    - ERROR
    - WARNING
    - DEBUG
  + logType: 字符串标量或向量，日志类型。默认值为所有类型。可选值：
    - running: 运行日志。
    - job: job 日志。
    - query: 查询日志。
    - audit: Audit 日志。
    - aclAudit: ACL audit 日志。
    - access: 用户级资源跟踪的 SQL 查询分布式表日志。
    - hardware: 用户级资源跟踪的 CPU 和 内存使用量日志。
    - dmesg: Linux dmesg 系统日志。
    - coredump: Linux coredump 文件的 backtrace 信息。
  + node: 字符串标量或向量，节点别名。默认值为所有节点。
  + mode: 字符串，搜索模式，即搜索使用的函数。默认值为 “strpos” 表示使用 strpos 函数来搜索。可选值：
    - strpos: 关键词匹配。
    - like:
      支持 % 通配符的关键词匹配。
    - ilike: 支持 % 通配符的大小写不敏感的关键词匹配。
    - regexFind: 正则表达式匹配。
  + cacheSize: 整数，单位 MB，每次搜索时提交异步任务从而可以缓存搜索结果，仅缓存大小小于 cacheSize
    的搜索结果以防止结果过大占用磁盘空间。如果当前搜索的范围为某个历史搜索的子范围，则使用上次的搜索结果来作为日志数据源。配置为 0
    时不缓存搜索结果，即每次搜索都是重新搜索。配置为 -1 时每次搜索都会缓存搜索结果。默认值为 1024。
  + adminPassword: 字符串，admin 账号的密码，仅在数据节点或计算节点节点下线时需要提供，此时会使用 xdb
    远程连接到所属的 agent 节点读取日志。若有节点下线而又没有提供 admin 账号的密码，打印 WARNING
    提示跳过读取该节点的日志。
  + dolphindbPath: 字符串，dolphindb 的可执行文件路径，查看 coredump 日志时必须配置。默认值为
    getHomeDir() 的返回值取子串到 server 路径下的 dolphindb，例如
    `/hdd/ddb/server/dolphindb`。

> dmesg 和 coredump 类型的日志需要配置 enableShellFunction 配置项才可以使用，未开启时不读取相关日志。
>
> 缓存功能的实现原理为 submitJob，故在节点重启后缓存即被清理。建议配置
> batchJobFileRetentionTime 配置项来定期自动清理后台任务的返回值文件。

**返回值**

表，字段说明：

* timestamp: 日志时间戳。所有结果根据时间戳升序排序。
* logLevel: STRING，日志等级。注意 query, audit, aclAudit, access 和 hardware 类型的日志等级总是
  INFO，而 coredump 和 dmesg 类型的日志等级总是 ERROR。
* node: SYMBOL，dolphindb 节点名或机器 host。注意 coredump 和 dmesg 类型的日志使用机器 host，其他类型使用
  dolphindb 节点名。
* logType: SYMBOL，日志类型。
* logFile: STRING，日志文件路径。
* content: STRING，日志原始内容。

**例子**

下面介绍各个参数的使用示例，未指定的参数将使用默认值，可以自由组合参数实现更精确的搜索。

搜索包含指定关键词的日志：

```
params = {
    "pattern": ["ERROR", "WARNING"]
}
log = searchLog(params)
```

搜索指定时间范围的日志：

```
params = {
    "startTime": 2025.05.15T00:00:00.000,
    "endTime": 2025.05.17T00:00:00.000
}
log = searchLog(params)
```

搜索指定类型的日志：

```
params = {
    "logType": ["query", "audit"]
}
log = searchLog(params)
```

搜索指定节点的日志：

```
params = {
    "node": ["P1-dnode1", "P2-dnode1"]
}
log = searchLog(params)
```

使用 ilike 来搜索大小写不敏感的关键词：

```
params = {
    "pattern": ["%Error%", "%Warning%"],
    "mode": "ilike"
}
log = searchLog(params)
```

启用和禁用搜索结果缓存：

```
params = {
    "cacheSize": 64 // 启用缓存，只缓存结果小于 64 MB 的表
    // "cacheSize": 0 // 禁用缓存
    // "cacheSize": -1 // 启用缓存，不限制大小
}
log = searchLog(params)
```

在数据节点或计算节点下线时，如果仍需读取该节点的日志，需要配置 adminPassword，从而使模块能够连接下线节点所属的 agent
节点来读取日志。注意该功能会占用 agent 节点的 CPU 和内存资源，而 agent
节点的资源相关配置项往往不高，可能会因日志过大和资源不足导致读取失败，故只建议在需要保留问题现场时使用该功能，否则建议启动节点后再读取日志。

```
params = {
    "adminPassword": "123456"
}
log = searchLog(params) // 在数据节点或计算节点下线时，依然能读取到日志
```

若日志的相关配置项未开启导致无法读取，会在前台打印相关信息。例如，读取 coredump 文件的堆栈信息和 Linux dmesg
系统日志的功能需要执行命令行，因此需要在控制节点和数据节点均配置 enableShellFunction=true 才可以使用。

```
params = {
    "logType": ["coredump", "dmesg"]
}
log = searchLog(params)
```

默认未配置 enableShellFunction=true 时会打印如下 INFO 信息，是符合预期的：

```
2025.06.05T10:29:20.386 <INFO> : The config enableShellFunction is false, searching for coredump is disabled
2025.06.05T10:29:20.459 <INFO> : The config enableShellFunction is false, searching for dmesg is disabled
```

### 3.2 saveLog

**语法**

```
saveLog(log, params=NULL)
```

**详情**

保存日志搜索结果到指定的目录，且按照一定的文件结构来存储不同类型的日志。目录结构如下：

* LogSearcher\_<DolphinDB版本号>\_<开始时间戳>\_<结束时间戳>\_<运行时间戳>
  + <机器 host>
    - controller.log
    - <节点名>.log
    - <节点名>\_job.log
    - <节点名>\_query.log
    - <节点名>\_audit.log
    - <节点名>\_aclAudit.log
    - <coredump 文件原始名称>.时间戳.log
    - dmesg.log

**参数**

* log: 表，searchLog 接口的返回值。
* params: 字典，与 searchLog 接口的 params 参数格式相同，这里介绍 saveLog 接口使用的参数：
  + saveDir: 字符串，日志保存路径。默认值为当前节点的运行日志保存路径。

**返回值**

字符串，实际保存路径，含开始时间戳\_结束时间戳。

**例子**

保存日志到指定路径：

```
params = {
    "saveDir": "/tmp/ddbLog"
}
log = searchLog()
saveLog(log, params) // 返回保存的具体路径，例如 /tmp/ddbLog/LogSearcher_3.00.4_20250515000000_20250517000000_2025052091727836
```

前往 `/tmp/ddbLog` 目录查看目录结构，示例如下：

```
$ tree /tmp/ddbLog/LogSearcher_3.00.4_20250515000000_20250517000000_2025052091727836
/tmp/ddbLog/LogSearcher_3.00.4_20250515000000_20250517000000_2025052091727836
├── 192.168.100.43
│   ├── controller.log
│   └── P1-dnode1.log
├── 192.168.100.44
│   ├── controller.log
│   ├── core.59174.2025051664140780.log
│   ├── dmesg.log
│   ├── P2-dnode1_audit.log
│   ├── P2-dnode1_job.log
│   ├── P2-dnode1.log
│   └── P2-dnode1_query.log
└── 192.168.100.45
    ├── controller.log
    └── P3-dnode1.log
```

### 3.3 generateDefaultParams

**语法**

```
generateDefaultParams()
```

**详情**

生成 searchLog 接口使用的默认参数字典。

**返回值**

字典，与 searchLog 接口的 params 参数相同。

**例子**

```
params = generateDefaultParams()
log = searchLog(params)
```

### 3.4 getSearchHistory

**语法**

```
getSearchHistory(params=NULL)
```

**详情**

若启用了缓存，获取集群所有节点的搜索历史记录。

**参数**

字典，与 searchLog 接口的 params 参数相同。默认值为空，表示获取所有搜索记录。

**返回值**

表，搜索历史记录，字段说明：

| name | typeString | comment |
| --- | --- | --- |
| logLevel | STRING | 日志等级。 |
| pattern | STRING | 搜索的模式字符串，多个模式用逗号连接。 |
| startTime | TIMESTAMP | 日志开始时间戳 |
| endTime | TIMESTAMP | 日志结束时间戳 |
| logType | STRING | 日志类型，多个类型用逗号连接。 |
| node | STRING | 节点别名，多个节点用逗号连接。 |
| mode | STRING | 搜索模式。 |
| cacheSize | INT | 缓存限制。 |
| jobId | STRING | 搜索任务 ID |
| jobNode | STRING | 搜索任务执行的节点别名。 |
| jobStartTime | TIMESTAMP | 搜索任务开始时间。 |
| jobEndTime | TIMESTAMP | 搜索任务结束时间。 |
| jobErrorMsg | STRING | 搜索任务错误信息。无错误时为空。 |

**例子**

可以结合 getJobReturn 函数获取历史搜索结果。

```
jobId = exec first(jobId) from getSearchHistory() where jobEndTime != NULL
log = getJobReturn(jobId)
```

## 4. 进阶使用

可以解析特定类型的日志来做相关分析和统计，下面是一些常见示例。

### 4.1 统计用户登录情况

可以搜索和解析 ACL audit 日志来统计指定时间范围内的用户登录情况，例如统计过去 24 小时的用户登录次数：

```
params = {
    "logType": "aclAudit"
}
log = searchLog(params)
res = select node, content.split(",") from log
res = select
node,
split_content.at(3).split(" ").at(1).split("=").at(1) as userId,
split_content.at(1) as time,
split_content.at(4) as remoteIp,
split_content.at(5) as remotePort
from res where split_content.at(2) == "login"

select count(*) from res group by node, userId, remoteIp
```

| node | userId | remoteIP | count |
| --- | --- | --- | --- |
| P2-dnode1 | admin | 192.168.0.129 | 1 |
| P2-dnode1 | admin | 192.168.0.77 | 141 |

### 4.2 统计分布式库表写入情况

可以搜索和解析 audit 日志来统计指定时间范围内的分布式库表的写入情况，例如统计过去 24 小时各个用户对库表的写入次数：

```
params = {
    "logType": "audit"
}
log = searchLog(params)
res = select node, content.split(",") from log
res = select
node,
split_content.at(0) as userId,
split_content.at(1) as startTime,
split_content.at(2) as endTime,
split_content.at(3) as dbName,
split_content.at(4) as tbName,
split_content.at(5) as opType,
split_content.at(6) as opDetail,
split_content.at(7) as tid,
split_content.at(8) as cid,
split_content.at(9) as remoteIp,
split_content.at(10) as remotePort
from res

select count(*) from res group by userId, dbName, tbName, opType
```

| node | userId | dbName | tbName | opType | count |
| --- | --- | --- | --- | --- | --- |
| P2-dnode1 | admin | dfs://finance |  | CREATE\_DB | 1 |
| P2-dnode1 | admin | dfs://finance | equity\_data | CREATE\_PARTITIONED\_TABLE | 1 |
| P2-dnode1 | admin | dfs://finance | equity\_data | APPEND | 1 |

### 4.3 统计分布式库表查询情况

可以搜索和解析 query 日志来统计指定时间范围内的分布式库表的查询情况，例如统计过去 24 小时各个用户对库表的查询次数：

```
params = {
    "logType": "query"
}
log = searchLog(params)
res = select content, content.split(",") from log
query = select
split_content.at(0) as node,
split_content.at(1) as userId,
split_content.at(2) as sessionId,
split_content.at(3) as jobId,
split_content.at(4) as rootId,
split_content.at(5) as type,
split_content.at(6) as level,
split_content.at(7) as time,
split_content.at(8) as database,
split_content.at(9) as table,
each(substr, content, content.strFind(",\"") + 2, each(strlen, content) - content.strFind(",\"") - 3) as jobDesc
from res

select count(*) from query group by node, userId, database, table
```

| node | userId | database | table | count |
| --- | --- | --- | --- | --- |
| P2-dnode1 | admin | dfs://finance | equity\_data | 1 |
| P2-dnode1 | admin | dfs://merge\_TB | merge\_snapshotTB | 1 |

### 4.4 慢 SQL 统计

可以搜索和解析 query 和 job 日志并做连接来做慢查询统计，例如统计过去 24 小时执行的 SQL 的耗时：

```
params = {
    "logType": ["query", "job"]
}
log = searchLog(params)
res = select content, content.split(",") from log where logType == "query"
query = select
split_content.at(0) as node,
split_content.at(1) as userId,
split_content.at(2) as sessionId,
split_content.at(3) as jobId,
split_content.at(4) as rootId,
split_content.at(5) as type,
split_content.at(6) as level,
nanotimestamp(split_content.at(7)) as time,
split_content.at(8) as database,
split_content.at(9) as table,
each(substr, content, content.strFind(",\"") + 2, each(strlen, content) - content.strFind(",\"") - 3) as jobDesc
from res

res = select node, content, content.split(",") from log where logType == "job"
job = select
split_content.at(0) as node,
split_content.at(1) as userId,
split_content.at(2) as sessionId,
split_content.at(3) as jobId,
split_content.at(4) as rootId,
split_content.at(5) as type,
split_content.at(6) as level,
nanotimestamp(split_content.at(7)) as startTime,
nanotimestamp(split_content.at(8)) as endTime,
each(substr, content, content.strFind(",\"") + 2, content.strFind("\",") - content.strFind(",\"") - 2) as jobDesc,
each(last, split_content) as errorMsg
from res

select node, userId, database, table, query.jobDesc as sql, (job.endTime - job.startTime) \ 1024 \ 1024 as elapsedMs from query join job on query.jobId == job.jobId order by job.endTime - job.startTime desc
```

| node | userId | database | table | sql | elapsedMs |
| --- | --- | --- | --- | --- | --- |
| P2-dnode1 | admin | dfs://\_\_trading\_stock\_1747240188933\_\_ | STOCK\_QUOTE | select [8196] top 100 id,date,value from STOCK\_QUOTE | 225.8648796081543 |
| P2-dnode1 | admin | dfs://SH\_kminute | sh\_stock\_kline\_minute | select [8196] top 100 SecurityID,Date,Time,PreClosePx,LastPx from sh\_stock\_kline\_minute | 37.64671039581299 |
| P2-dnode1 | admin | dfs://QUOTATION\_TSDB | OS\_OPTION\_QUOTATION\_LV1 | select [8196] top 100 STOCK\_ID,CLASS\_ID,INSTRUMENT\_ID,NORMALIZED\_SYMBOL,MARKET,TRADEDATE,UNDERLYING\_PRICE,UNDERLYING\_TIME,BID\_PRICE,BID\_VOLUME,BID\_TIME,ASK\_PRICE,ASK\_VOLUME,ASK\_TIME,UPDATETIME from OS\_OPTION\_QUOTATION\_LV1 | 35.06101894378662 |
