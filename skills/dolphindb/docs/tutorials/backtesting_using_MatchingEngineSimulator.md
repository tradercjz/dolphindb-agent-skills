<!-- Auto-mirrored from upstream `documentation-main/tutorials/backtesting_using_MatchingEngineSimulator.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 在 C++ 使用模拟撮合引擎插件实现自定义的高性能回测

DolphinDB 的高性能行情回放与模拟撮合引擎插件，为量化交易者提供了低延迟、高吞吐量的策略验证解决方案。对于已构建 C++
回测框架的机构而言，直接在现有系统中集成撮合引擎，既能复用既有基础设施，又能获得 DolphinDB 的极速计算优势，是高频策略仿真的优选方案。

本文面向熟悉 C++ 开发、具备 DolphinDB 基础知识的量化工程师，重点讲解如何通过 Swordfish 计算库或 C++ API，将 DolphinDB
撮合引擎插件无缝集成到独立 C++ 交易系统中。相较于 DolphinDB
脚本回测，本方案可实现低延迟高并发的回测流程，特别适用于算法交易、做市策略等对时效性敏感的仿真场景。

## 1. 背景介绍

回测是量化交易投研的一个重要环节。量化策略上线之前，必须通过回测评估策略在历史数据上的表现。在中高频策略回测中，并不能简单的假设每个订单以当前价格或日终价格全部成交，需要一个模拟撮合引擎来模拟实际的交易过程，例如考虑订单能否成交、成交价格、成交量以及市场冲击等因素。DolphinDB
提供了模拟撮合引擎插件，支持沪深交易所 Level-2 逐笔行情和快照行情，实现了与交易所一致的 **“价格优先，时间优先”**高精度撮合、支持基于多种行情数据的撮合模式、并提供丰富的撮合配置，模拟真实的实盘交易环境；支持通过 DolphinDB 脚本语言、Python 或
C++语言完成中高频策略的研发和测试，提供了一个性能优异且易扩展的中高频量化交易策略回测解决方案。

Swordfish
是一个专为金融行业设计的高性能数据分析计算函数库，具备卓越的内存处理能力和优化的计算性能。它不仅提供多种通用计算功能，还支持实时流数据处理和用户自定义函数，满足复杂数据分析和低延迟流数据计算的需求。Swordfish
能够在任何支持 C++ 的平台上运行，用户可以通过 C++ 脚本直接调用其接口，实现高效计算。

DolphinDB C++ API 用于连接 DolphinDB 服务端和 C++客户端，从而实现数据的双向传输和脚本的调用执行。 它可以方便您在 C++ 程序中使用
DolphinDB 进行数据的处理、分析和建模等操作，利用其优秀的计算性能和强大的存储能力来帮助您加速数据的处理和分析。

本文依照[《DolphinDB 策略回测白皮书》](https://dolphindb.cn/whitepaper/backtesting)的系统设计，介绍如何在 C++
中封装模拟撮合引擎插件，实现一个简单易拓展高精度撮合的回测框架，从而可以方便地集成到已有的 C++ 回测或者仿真系统中。本文设计了统一的事件型接口，并提供
Swordfish 和 C++ API 两种实现。2 种方式的适用场景如下：

**表 1-1 Swordfish 和 C++ API 实现回测框架场景对比**

| 库 | 适用场景 |
| --- | --- |
| Swordfish | * 对数据处理时延敏感（微秒级），模拟撮合引擎在本地 Swordfish 运行。 * 高倍速回放行情。 * 需要在 C++ 直接调用 DolphinDB 的丰富的函数库进行高性能分析和计算。 |
| C++ API | * 对数据处理时延不敏感（根据网络情况，一般是毫秒级），模拟撮合引擎在远程 DolphinDB 运行。 * 原速回放行情。 |

## 2. 系统设计

在[《DolphinDB 策略回测白皮书》](https://dolphindb.cn/whitepaper/backtesting)中，介绍了中高频量化交易策略回测平台的实现，主要包括三个重要环节：

* 行情数据回放
* 委托订单模拟撮合
* 策略开发与策略回测绩效评估

以此为依据可以设计出以 DolphinDB 为数据源在 C++ 进行回测的整体流程：

1. 创建远程行情流表，并对其进行订阅；
2. 回放行情数据到流表；
3. 在订阅回调中遍历和解析数据，将解析后的行情数据写入到模拟撮合引擎；
4. 触发行情回调，在回调内实现策略逻辑，执行下单等操作；
5. 模拟撮合引擎输出成交明细等信息，并触发相关业务回调，在回调内实现策略逻辑。
6. 回测结束后输出绩效指标。

使用 Swordfish 实现自定义回测的系统架构图如下：

![](images/backtesting_using_MatchingEngineSimulator/1-1.png)

图 1. 图 1-1 Swordfish 自定义回测实现架构图

使用 C++ API 实现自定义回测的系统架构图如下：

![](images/backtesting_using_MatchingEngineSimulator/1-2.png)

图 2. 图 1-2 C++ API 自定义回测实现架构图

## 3. 接口设计

本教程根据 DolphinDB 的模拟撮合接口所具备的功能，设计出了行情和交易接口。主要包括如下功能模块：

* **配置项模块：**负责回测框架实例的相关配置，包括远程连接配置、行情类别配置、并发相关配置等。
* **主动调用接口模块：**提供可在代码中主动调用的接口，包括创建模拟撮合引擎实例、回放数据下单、撤单等接口。
* **回调接口模块：**以回调函数的形式提供接口，包含行情回调、报单应答、成交通知等接口。

注：

本节所介绍的配置项和接口，除非特别声明，在 Swordfish 和 C++ API 均可调用。

### 3.1 配置项

回测框架实例的配置项如下表所示。每个实例可独立配置，从而可以使用多个实例做并发回测。

| 配置名 | 说明 | 备注 |
| --- | --- | --- |
| hostName | DolphinDB 节点 IP |  |
| port | DolphinDB 节点端口号 |  |
| userId | DolphinDB 用户名 |  |
| password | DolphinDB 密码 |  |
| dataType | 行情类别，与模拟撮合引擎的 dataType 参数相同。 |  |
| inputStreamTableName | 输入流表名。默认为 “inputStream”。 | 可通过配置不同流表名实现并发。 |
| engineName | 模拟撮合引擎名。默认为 “matchEngine“。 | 可通过配置不同引擎名实现并发。 |
| orderDetailsOutputStreamTableName | 成交明细输出流表名。默认为 “orderDetailsOutputStream”。 | C++ API 实现特有配置项。可通过配置不同流表名实现并发。 |
| snapshotOutputStreamTableName | 行情快照输出流表名。默认为 “snapshotOutputStream”。 | C++ API 实现特有配置项。可通过配置不同流表名实现并发。 |

### 3.2 相关接口说明

本教程设计的回测框架提供创建模拟撮合引擎实例、回放数据、下单、撤单等主动调用接口，以及行情回调、报单应答、成交通知等回调接口。下面将介绍核心的接口的设计和使用说明，其他更具体的接口说明详见附件源码内注释。

#### 3.2.1 创建模拟撮合引擎

首先，创建模拟撮合引擎实例的接口为 `createMatchEngine`，提供两种接口实现：

```
dolphindb::SmartPointer<MatchingEngineSimulatorWrapper> createMatchEngine(
        dolphindb::ConstantSP name, dolphindb::ConstantSP exchange, dolphindb::DictionarySP config,
        dolphindb::TableSP dummyQuoteTable, dolphindb::DictionarySP quoteColMap, dolphindb::TableSP dummyUserOrderTable,
        dolphindb::DictionarySP userOrderColMap, dolphindb::TableSP dummyOrderDetailsOutput,
        dolphindb::ConstantSP orderDetailsOutputStreamTableName=nullptr)

dolphindb::SmartPointer<MatchingEngineSimulatorWrapper> createMatchEngine(
        std::vector<dolphindb::ConstantSP> args)
```

第一种实现为展开的参数列表，第二种实现将第一种实现的所有参数放在一个数组里。该接口的参数要求与模拟撮合引擎插件的
createMatchEngine 接口基本相同，这里只介绍有区别的参数：

* dummyOrderDetailsOutput：Table 类指针，成交明细输出表的实际结构，用于给 Swordfish/DolphinDB
  创建输出流表提供参考结构。
* orderDetailsOutputStreamTableName：String 类指针，成交明细输出表的流表名称，默认为
  “orderDetailsOutputStream”，用于给 DolphinDB 创建流表指定名称。**C++ API
  特有参数**。

返回值为 MatchingEngineSimulatorWrapper 对象指针，引擎实例，可用来做写入行情、下单、获取成交明细等操作。

注：

注意在 C++ API 实现时，由于模拟撮合引擎实例存在于 DolphinDB，每次调用
`createMatchEngine` 都会新建一个 DolphinDB
远程连接以绑定，故建议不要频繁调用，而应该将接口返回的实例保存下来重复使用。

#### 3.2.2 回放行情数据

创建好模拟撮合引擎后，使用 `replayQuoteToMatchEngine`
接口回放指定股票代码和天数的行情数据到指定引擎，可以指定回放速率。

```
void Interface::replayQuoteToMatchEngine(VectorSP codes, ConstantSP startDate, ConstantSP endDate,
                                         SmartPointer<MatchingEngineSimulatorWrapper> engine, int replayRate)
```

注：

请注意本教程仅提供回放 Level2
股票快照行情的示例。用户可参考代码实现其他类型的行情回放。

#### 3.2.3 行情回调

行情开始写入引擎后，会触发 `onQuote` 行情回调，参数为一条行情的字典，可通过 getMember(“key“)
读取字段，例如读取股票代码：

```
virtual void onQuote(const ConstantSP &quote){
    string symbol = quote->getMember("symbol")->getString();
}
```

#### 3.2.4 策略实现

在实现策略时，可以使用 `getMatchEngine` 接口来获取指定名称的模拟撮合引擎，用来下单或撤单等。

```
SmartPointer<MatchingEngineSimulatorWrapper> Interface::getMatchEngine(ConstantSP name)
```

报单请求接口为 `submitOrder`，撤单请求接口为
`cancelOrder`，参数为引擎实例和订单数据。订单数据类型为
`OrderField`，是一个 struct，与模拟撮合引擎插件的用户订单表字段格式相同，字段说明：

* symbol：字符串，标的代码。
* timestamp：long long，下单时间戳，**非必填，不填时即时撮合。**
* orderType：int，订单类型。
* price：double，订单委托价格。
* orderQty：long long，委托数量。
* direction：int，买卖方向，1（买 ），2（卖）。
* orderId：int，用户订单 ID，非必填，仅撤单时需要。
* userOrderId：int，用户自定义订单 ID，**非必填，不填时自动填一个递增的 ID。需要保证每次报单时对一个引擎填写的
  userOrderId 是唯一的。**

返回值为一个 long long，下单或撤单成功时返回用户订单 ID，失败时返回 -1。

```
long long Interface::submitOrder(SmartPointer<MatchingEngineSimulatorWrapper> engine, const OrderField &order)
long long Interface::cancelOrder(SmartPointer<MatchingEngineSimulatorWrapper> engine, const OrderField &order
```

#### 3.2.5 报单/撤单应答和通知

报单或撤单后，将触发应答和通知。报单应答的回调接口为 `onOrderSubmit`，撤单应答的回调接口为
`onOrderCancel`，包含订单数据和错误码。委托通知的回调接口为
`onOrder`，成交通知的回调接口为
`onMatch`，参数为一条委托或成交明细的字典，字段格式与模拟撮合引擎的成交明细表相同。

```
virtual void onOrder(dolphindb::DictionarySP orderDetail);
virtual void onMatch(dolphindb::DictionarySP tradeDetail);
```

## 4. 回测平台系统实现

根据系统设计和接口设计，设计如下功能模块来实现回测和仿真交易系统：

* 远程连接：远程连接 DolphinDB 并执行脚本，实现回放数据和清理远程环境等接口。
* 插件加载和使用：加载模拟撮合插件，封装模拟撮合插件的相关脚本方法为 C++ 接口，实现下单和撤单等主动调用接口，以及报单委托和成交委托等回调。
* 流数据订阅、解析和回调：订阅 DolphinDB 的流表作为数据源，解析流数据并写入到模拟撮合引擎，实现行情回调。

下面分别介绍使用 Swordfish 和 C++ API 实现的逻辑。

### 4.1 使用 Swordfish 实现

Swordfish 支持加载插件，支持使用 C++ 函数指针调用插件方法，入参和返回值均为以 Constant 类为基类的 DolphinDB
数据类型。我们可以通过在 Swordfish 本地调用模拟撮合引擎的方法来实现自定义回测逻辑。下面介绍主要逻辑的实现设计。

#### 4.1.1 远程连接

在 Swordfish 中可以使用 xdb 方法远程连接
DolphinDB 节点，然后使用 remoteRun
方法执行脚本。为了实现便捷的远程连接操作，我们封装了 xdb 和 remoteRun，定义了**远程连接类
DDBConnection**。该类专门用于远程连接指定的 DolphinDB 节点、执行脚本和订阅流表。参数和返回值参考了 C++ API
远程连接类的设计，具体说明见源码注释。

#### 4.1.2 插件加载和使用

在 Swordfish 中本地加载和使用模拟撮合引擎插件，可以通过 loadPlugin 方法加载并获得其接口的函数指针。为了实现便捷的插件加载和调用相关接口操作，我们封装了 loadPlugin
方法，定义了**插件类 DDBPlugin**，用于加载指定的插件和调用插件的接口。继承插件类实现**模拟撮合引擎插件类
MatchingEngineSimulatorWrapper**，调用模拟撮合引擎的相关接口实现下单和撤单等主动调用接口。具体使用说明见源码注释。

#### 4.1.3 流数据订阅、解析和回调

在 Swordfish 中可以使用 subscribeTable 方法订阅远程 DolphinDB 的流表，该方法的一个关键参数是 handler，
用于处理订阅数据的函数指针。我们封装 **Swordfish 函数定义类 SwordfishFunctionDef**，用于将 C++
函数指针方便地转换为 Swordfish 函数指针，从而可以在 C++ 的自定义方法内解析流数据并调用相关业务回调。具体使用说明见源码注释。

### 4.2 使用 C++ API 实现

在 DolphinDB 加载模拟撮合插件后，可以使用 C++ API 远程连接
DolphinDB，上传参数并调用相关脚本方法来实现自定义回测逻辑。下面介绍主要逻辑的实现设计。

#### 4.2.1 远程连接

在 C++ API 可以使用 DBConnection 类远程连接 DolphinDB 和执行脚本。具体接口使用说明请参考 C++ API 官方文档。

#### 4.2.2 插件加载和使用

在 C++ API 实现时，模拟撮合引擎插件在 DolphinDB 远程加载和使用，可以远程执行 loadPlugin 方法加载插件到
DolphinDB，然后封装远程连接类的 run
接口执行模拟撮合引擎的接口脚本，实现模拟撮合引擎插件类
MatchingEngineSimulatorWrapper，实现下单和撤单等主动调用接口。具体接口使用说明请参考 C++ API 官方文档。

#### 4.2.3 流数据订阅、解析和回调

在 C++ API 可以使用 ThreadedClient 类订阅远程 DolphinDB 的流表，该类提供的 subscribe 方法可以直接以 C++
的函数指针作为订阅回调，从而可以在 C++ 的自定义方法内解析流数据并调用相关业务回调。具体接口使用说明请参考 C++ API 官方文档。

## 5. 回测案例

基于前述设计与实现方案，本节通过核心代码示例详细阐述简易回测策略的实现逻辑，具体策略为在实时处理每笔行情快照数据后自动生成限价委托订单。完整代码请查看附件源码。

1. **定义接口类并实现策略**

   继承 Interface 类为 `CustomInterface` 类，并重写
   `onQuote` 方法，在收到一笔行情时调用 `getMatchEngine`
   方法获取引擎实例，然后调用 `submitOrder`
   下单：

   ```
   class CustomInterface : public Interface {
     public:
       CustomInterface(unordered_map<string, string> config) : Interface(config) {}

       void onQuote(const ConstantSP &quote) override {
           ...
           engine = getMatchEngine(new String(matchEngineName_));
           string symbol = quote->getMember("symbol")->getString();
           OrderField order;
           order.symbol = symbol;
           order.orderType = 5;
           order.price = bidPrice->getLong();
           order.orderQty = 200;
           order.direction = 1;
           submitOrder(engine, order);
       }
   };
   ```
2. **创建模拟撮合引擎**在 main 函数中，创建 `CustomInterface` 类，使用
   `getExampleMatchEngineArgs` 方法获取模拟撮合引擎的示例参数，然后使用
   `createMatchEngine`
   方法创建模拟撮合引擎。

   ```
   interface = new CustomInterface(config);
   auto args = interface->getExampleMatchEngineArgs();
   engine = interface->createMatchEngine(args);
   ```
3. **订阅行情数据**使用 `subQuoteTable`
   方法订阅行情数据，从而使行情回调方法生效。

   ```
   interface->subQuoteTable();
   ```
4. **回放行情数据**

   使用 `replayQuoteToMatchEngine`
   方法回放指定股票代码和日期时间范围的数据到引擎。

   ```
   interface->replayQuoteToMatchEngine(codes, startDate, endDate, engine, -1);
   ```
5. **等待回测结束**

   使用 `isBacktestEnd`
   方法等待回测结束。

   ```
   interface->isBacktestEnd(true);
   ```
6. **输出绩效指标**

   以使用 `getPosition` 方法输出持仓为例。可以在
   `CustomInterface`
   类中实现自定义指标的计算和输出。

   ```
   cout << interface->getPosition() << endl;
   ```

## 6. 性能测试

本文使用的测试环境配置为：

* DolphinDB v3.00.2.2 单节点
* Swordfish v3.00.2 ABI0
* CPU：Intel(R) Xeon(R) Silver 4216 CPU @ 2.10GHz 64核
* 内存：400G
* 硬盘：SSD 12 Gbps

统计 Swordfish 实现的回测框架进行多并发全速回放的总耗时。下单策略为对每笔快照行情下 1 单限价单。性能统计如下：

**表 6-1 Swordfish 实现的回测框架性能测试统计**

| 数据量 | 并发数 | 耗时（s） |
| --- | --- | --- |
| 2000支股票快照（7,039,909 行，2.6 GB） | 1 | 175 |
| 2000支股票快照（7,039,909 行，2.6 GB） | 2 | 95 |
| 2000支股票快照（7,039,909 行，2.6 GB） | 4 | 50 |
| 2000支股票快照（7,039,909 行，2.6 GB） | 8 | 29 |

可见多线程并行能够有效提高性能，但并不是线性的提升，因为服务端的数据回放到流表和发送到客户端需要一定的耗时。

由于 C++ API 实现下模拟撮合引擎位于远程
DolphinDB，故下单和撤单等操作存在网络时延，倍速回放时会出现客户端操作时刻服务端已回放到更后面的时间的情况，故只能原速回放，无法进行倍速回放性能测试。

## 7. 总结

本文展示了如何通过使用 Swordfish 或 C++ API 在 C++ 环境下调用模拟撮合引擎插件实现自定义的高性能回测，并封装了统一的接口，从而实现将
DolphinDB 回测逻辑方便地集成到已有的 C++ 回测系统。其中，Swordfish
可以本地运行模拟撮合引擎，具有更高的灵活性，并支持倍速回放，在性能方面表现更优。

## 8. 附件

[CppApiBacktest.zip](https://cdn.dolphindb.cn/zh/tutorials/script/backtesting_using_MatchingEngineSimulator/CppApiBacktest.zip)

[SwordfishBacktest.zip](https://cdn.dolphindb.cn/zh/tutorials/script/backtesting_using_MatchingEngineSimulator/SwordfishBacktest.zip)

注：

请注意 Swordfish 实现需要将支持 Swordfish 的授权文件 dolphindb.lic 放到 asset
文件夹后才能编译和执行。
