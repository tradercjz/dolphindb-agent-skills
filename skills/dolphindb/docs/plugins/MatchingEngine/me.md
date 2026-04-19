<!-- Auto-mirrored from upstream `documentation-main/plugins/MatchingEngine/me.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# MatchingEngine

（该插件已停用，新模拟交易所插件详见 SimulatedExchangeEngine）

MatchingEngine 插件模拟一个通用交易所的行为，用户可以将交易所的逐笔委托订单数据输入到该插件中，该插件会计算输出成交结果以及订单簿。

## 安装插件

### 版本要求

DolphinDB Server 2.00.10 及更高版本，支持 Linux x64, Linux JIT。

### 安装步骤

1. 在 DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   注意：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可[自行编译](https://gitee.com/dolphindb/DolphinDBPlugin)（请选择对应分支下的插件）或在 [DolphinDB 用户社区](https://ask.dolphindb.cn/)进行反馈。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   ```
   installPlugin("MatchingEngine")
   ```
3. 使用 `loadPlugin` 命令加载插件。

   ```
   loadPlugin("MatchingEngine")
   ```

## 接口说明

### setupGlobalConfig

**语法**

```
MatchingEngine::setupGlobalConfig(inputScheme, mapping, pricePrecision, bookDepth)
```

**详情**

配置各项参数，必须在调用 `createExchange` 之前调用。

**参数**

**inputScheme** 一个表，表示输入的订单的原始表结构。

**mapping** 一个字典，key 和 value 的类型都是字符串标量。表示列名的映射关系。将原始表结构的列名和插件中使用的列名逐一对应。插件在计算时需要如下几列信息，原始表中必须包含，但是原始表中的列名可以不同，通过 mapping 进行映射即可。

| **插件中使用的列名** | **类型** | **含义** |
| --- | --- | --- |
| op | INT | 订单类型 0： 新增订单；1：修改订单；2：取消订单 |
| symbol | SYMBOL | 订单标的 |
| id | LONG | 订单 ID，要求唯一 |
| quantity | LONG | 数量，正整数 |
| condition | INT | 订单标志，由下面这些标志求和得到 0： 卖出；1：买入；2： AON订单；4：IOC订单；8：stop-loss；16：take-profit；32：trailing-stop |
| price | LONG | 价格 |
| thresholdPrice | LONG | 如果是 stop-loss/take-profit/trailing-stop 订单，那么就是该订单的价格阈值 |
| expiredTime | LONG | 订单的有效时间 |

**pricePrecision** 整型标量，表示价格中小数点移动的位数。例如价格为 6500，当 *pricePrecision* 为 3 时，真实价格为 6.5。在计算成交额时使用。

**bookDepth** 整型标量，表示订单簿的最大深度。

### createExchange

**语法**

```
MatchingEngine::createExchange(sym, output,depthOutput)
```

**详情**

创建一个模拟交易所，返回交易所对象，可以通过 DolphinDB 中向表中插入数据的接口向其中插入订单数据。

**参数**

**sym** 字符串类型标量，表示该交易所可以处理的订单标的。同一个标的只能创建一个交易所。

**output** 一个表，表示成交结果的输出表。目前表结构固定如下：

| **列名** | **类型** | **含义** |
| --- | --- | --- |
| symbol | SYMBOL | 订单标的 |
| id | LONG | 订单 ID |
| status | STRING | 订单状态 |
| condition | INT | 订单标志 |
| quantity | LONG | 订单数量 |
| filledQuantity | LONG | 成交数量 |
| cost | DOUBLE | 成交额 |

**depthOutput** 一个表，表示订单簿的输出表。目前表结构固定如下：

| **列名** | **类型** | **含义** |
| --- | --- | --- |
| is\_sell | BOOL | 是否是卖出方向订单簿 |
| level | INT | 等级 |
| price | LONG | 价格 |
| aggregate\_qty | LONG | 数量 |
| order\_count | LONG | 订单数 |
| market\_price | LONG | 市场价 |

### dropExchange

**语法**

```
MatchingEngine::dropExchange(exchange)
```

**详情**

删除指定模拟交易所。

**参数**

**exchange** 可以是 `createExchange` 返回的交易所对象，也可以是一个字符串（表示该易所可处理的订单标的）。

## 使用示例

```
ORDER_ADD = 0
ORDER_MOD = 1
ORDER_CAN = 2

ORDER_SEL = 0
ORDER_BUY = 1
ORDER_AON = 2
ORDER_IOC = 4
ORDER_SL  = 8
ORDER_TP  = 16
ORDER_TS  = 32

inputScheme = table(1:0, `op`symbol`id`quantity`condition`price`thresholdPrice`expiredTime, [INT,SYMBOL,LONG,LONG,INT,LONG,LONG,LONG])
pricePrecision = 0
bookDepth = 10
MatchingEngine::setupGlobalConfig(inputScheme, , pricePrecision, bookDepth)

sym = 'AAPL'
output = table(10000:0,`symbol`id`status`condition`quantity`filledQuantity`cost, [SYMBOL,LONG,STRING,INT,LONG,LONG,DOUBLE])
depthOutput = table(10000:0,`is_sell`level`price`aggregate_qty`order_count`market_price,[BOOL,INT,LONG,LONG,LONG,LONG])
exchange = MatchingEngine::createExchange(sym, output,depthOutput)

insert into exchange values(ORDER_ADD,`AAPL,0,100,ORDER_BUY,100,0,0)
insert into exchange values(ORDER_ADD,`AAPL,1,100,ORDER_SEL,0,0,0)

MatchingEngine::dropExchange(exchange)
```
