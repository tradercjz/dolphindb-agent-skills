<!-- Auto-mirrored from upstream `documentation-main/rn/plugin/plg300rn.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 3.00.00

## amdQuote

### 新功能

* `connect` 新增参数
  *dataVersion*，用于指定华锐行情数据的版本号，以根据版本号来确定合适的表结构。（**3.00.0.1**）
* `subscribe` 新增参数
  *seqCheckMode*，用于指定插件在接收到不连续数据后的行为。仅在订阅 orderExecution 或
  bondOrderExecution 类型数据时有效。（**3.00.0.1**）
* amdQuote398 插件支持 Linux X86-64 ABI=1 DolphinDB server。

## Arrow

### 故障修复

* 任务执行过程中若发生续传，可能会出现任务卡住。（**3.00.0.14**）
* 修复了下载超过 8192 行数据的数组向量时插件异常退出的问题。

## AWS

### 新功能

支持设置 REST endpoint 的 URL 地址及其他请求参数，以建立到私有 AWS S3 环境的连接。

### 故障修复

修复了 `deleteS3Object` 在权限不足时仍然返回成功的问题。（**3.00.0.18**）

## Backtest

### 新功能

* 新增两融回测引擎，支持融资融券业务逻辑。（**3.00.0.2**）
* 新增期货回测引擎，支持期货业务逻辑。（**3.00.0.2**）

### 故障修复

股票回测引擎部分计算结果错误。（**3.00.0.2**）

## CTP

### 功能改进

`connect` 和 `queryInstrument`
函数连接时支持传入多个连接地址和端口。（**3.00.0.2**）

## DataFeed

### 新功能

* `createHandle` 的 *config* 参数新增配置项
  “OutputElapsed”，用于设置是否获取插件从收到行情到准备插入流表的时延。（**3.00.0.3**）
* `getSchema` 新增可选参数
  *needElapsedTime*，用于设置存放行情的表结构中是否包含时延列。（**3.00.0.3**）
* `createHandle` 新增参数 *config*，可配置 receiveTime
  字段，以输出接收到数据的时间至输出表。（**3.00.0.1**）

## EFH

首次发布，用于对接盛立 EFH 行情服务软件，将上交所和深交所的 Level-2 实时行情接入 DolphinDB。（**3.00.0.1**）

## gurobi

首次发布，用于求解线性规划、整数规划、混合整数线性规划、二次规划等一些优化问题。（**3.00.0.1**）

## HttpClient

### 新功能

* 新增接口 `httpPut` 和 `httpDelete`
  ，分别用于更新或删除服务器上的资源。（**3.00.0.2**）
* `httpGet` 新增参数 *config*，可配置 proxy，以指定代理地址
  。（**3.00.0.1**）
* HttpClient 插件支持 Windows 系统。

### 功能优化

* 优化 `sendEmail` 函数的功能：（**3.00.0.9**）

  + 新增可选参数 *msg*，支持填入完整的邮件正文信息。
  + 将 *subject*, *body*
    参数改为可选，同时将通过这两个参数发送的邮件正文中的换行符修改为标准换行符。

## insight

### 新功能

* `connect` 的参数 *handles*
  新增支持以下数据品类选项：债券快照（BondTick）、基金快照（FundTick）、期权快照（OptionTick）、融券通（SecurityLending）。（**3.00.0.1**）
* `connect` 新增参数 *backupList*，支持配置多个 Insight
  服务器地址，实现服务高可用。（**3.00.0.1**）
* `subscribe`的参数 *securityIDSource*
  新增以下市场选项：北交所（XBSE），大商所（XDCE），上期所（XSGE），新三板（NEEQ），郑商所（XZCE），港股通（HKSC），H
  股全流通（HGHQ），国证指数（CNI）。（**3.00.0.1**）

### 故障修复

* 集群状态下，无法自动找到 insight 插件加密认证所需的 cert 文件。（**3.00.0.4**）
* 订阅 orderTransaction 类型数据，出现错误的状态显示。（**3.00.0.4**）

## kafka

### 新功能

支持连接启用 SSL 认证的 Kafka server。（**3.00.0.15**）

支持 zstd 压缩算法。（**3.00.0.1**）

## kdb+

### 新功能

支持 kdb+ nested list 类型，对应 DolphinDB 的 arrayVector 类型。（**3.00.0.3**）

### 功能改进

支持读取以 snappy 和 lz4 压缩算法格式的 kdb+ 文件。

### 故障修复

解析部分序列化文件失败。（**3.00.0.3**）

## LDAP

首次发布，用于搜索 LDAP 服务器内的条目信息，进而实现在 DolphinDB 中进行 LDAP 第三方验证登录功能。（**3.00.0.1**）

## MDL

* 所有数据类型支持接收数据包元数据信息。（**3.00.0.17**）
* 首次发布，用于将通联数据提供的高频行情数据接入 DolphinDB 中，以便进行后续的计算或存储。

## MQTT

### 功能优化

* Windows 插件的 `connect`
  接口新增了连接校验和账户、密码等正确性校验。（**3.00.0.2**）
* Linux 插件的 `connect` 接口新增了账户、密码等正确性校验。（**3.00.0.2**）

## MySQL

### 功能优化

* `mysql::load` 和 `mysql::loadEx` 接口支持在加载
  DECIMAL 数据时通过 *schema* 参数指定小数精度。（**3.00.0.0.1**）
* `mysql::extractSchema` 接口支持在提取 DECIMAL
  类型数据时显示其小数精度。（**3.00.0.0.1**）

## NSQ

### 新功能

* 支持 orderTrade 类型，输出数据可以直接写入快照合成引擎中。相关变动接口：`getSchema`,
  `subscribe`。（**3.00.0.3**）
* `connect` 新增参数
  *dataVersion*，用于指定数据字段版本。（**3.00.0.2**）
* `getSubscriptionStatus` 函数新增别名
  `getStatus`。（**3.00.0.2**）

* 接口 `nsq::connect` 新增参数 *username*,
  *password*，支持在建立连接时指定用户名及密码。

### 故障修复

* 在非 sailfish 情况下连接特殊源时，NSQ 宕机。（**3.00.0.3**）
* 连接非法配置文件 server 宕机。（**3.00.0.2**）

## ODBC

### 新功能

* 新增函数 `setLogLevel`用于设置插件输出日志的等级，同时新增函数
  `getLogLevel`，用于获取插件当前的输出日志等级。（**3.00.0.12**）

### 功能优化

* 在创建数据库连接时，仅当 *dataBaseType* 参数指定为 “ClickHouse”
  时，才对连接加锁。（**3.00.0.12**）

## OPC

### 功能优化

增强插件稳定性。（**3.00.0.14**）

### 缺陷修复

执行 `opc::close` 断开连接失败。（**3.00.0.14**）

## OPCUA

### 功能优化

`subscribe` 新增参数 *reconnect* 和
*resubscribeInterval*，支持在订阅断开时自动重连。（**3.00.0.14**）

## parquet

### 功能优化

`parquet::saveParquet` 接口新增用于指定压缩格式的可选参数 compression。

### 故障修复

修复了加载 parquet 时使用 `parquet::loadParquet` 的参数 *schema* 填写错误导致
Server 宕机的问题。

## SSEQuotationFile

* `subscribe` 接口新增 OutputElapsed
  配置项，用于设定是否为行情表增加最后一列。该列包含插件从收到行情开始到准备插入流表为止的延时。（**3.00.0.3**）

* `getSchema` 接口新增参数 *needElapsedTime*，用于设定返回的 shcmea 是否包含
  elapsedTime 列。（**3.00.0.3**）

* 首次发布，用于解析上交所提供的行情文件，并将信息存储到 DolphinDB 的表中。（**3.00.0.1**）

## RabbitMQ

### 功能改进

将可同时存在的最大连接数限定为 100。

## Redis

### 新功能

* 新增接口 `redis::batchHashSet`，可高效率批量执行 Redis 的 HSET 操作。
* 新增支持 Windows x86 平台。（**3.00.0.2**）

## TCPSocket

首次发布用于创建 TCP 连接并与指定 IP 和端口进行数据交互的 TCPSocket 插件。

## WebSocket

### 新功能

新增 WebSocket 插件，支持从 WebSocket 的服务端读取数据以及发送数据到 WebSocket
的服务端。（**3.00.0.2**）

### 故障修复

* WebSocket 插件重连失败，导致 server 宕机。（**3.00.0.12**）
* `WebSocket::createSubJob` 的 *onMessage* 回调函数中的 data
  参数接收到非 table 类型数据。（**3.00.0.3**）

## WindTDF

### 新功能

新增 WindTDF 插件，支持接收万得实时行情数据。（**3.00.0.1**）

## xgboost

### 功能改进

支持 2.0.0 版本的 xgboost。

## XTP

首次发布，用于接收上交所、深交所以及北交所的实时行情，并将数据存储于 DolphinDB 的共享表中。（**3.00.0.1**）

### 新功能

* `createXTPConnection` 接口新增：
  + OutputElapsed
    配置项，用于设定是否为行情表增加最后一列。该列包含插件从收到行情开始到准备插入流表为止的延时。（**3.00.0.3**）
  + ciphertext 配置项，用于设定返回的 shcmea 是否包含 elapsedTime
    列。（**3.00.0.3**）
* `getSchema` 接口新增参数 *needElapsedTime*，用于设定返回的 shcmea 是否包含
  elapsedTime 列。（**3.00.0.3**）
* 新增接口 `generateCiphertextAndIV`，用于获取密文密码以及 iv
  值。（**3.00.0.3**）
* 支持开发逐笔数据。（**3.00.0.2**）

## zip

### 功能优化

增强对参数 *compressionLevel*（压缩等级）, *password*（密码）的校验。

## zmq

### 新功能

新增 `setMonitor` 接口，支持开启 ZeroMQ 的连接监视。（**3.00.0.2**）
