# createOrderReconstituteEngine

首发版本：3.00.4

## 语法

`createSSEOrderReconstructionEngine(name, dummyTable,
outputTable, inputColMap)`

别名：createOrderReconstituteEngine

## 详情

上交所的逐笔数据中：

* 如果一笔委托单在提交时立即全部成交，则会记录成交数据，而不会记录原始委托。
* 如果一笔委托单在提交时立即部分成交，则会记录对应的成交数据，未成交的部分记录为一笔委托。

此函数定义一个订单还原引擎，根据上交所逐笔数据（一个包含逐笔成交与逐笔委托的数据表），实时还原缺失的原始委托信息。

## 参数

**name** 字符串标量，表示引擎的名称，作为其在一个数据节点/计算节点上的唯一标识。可包含字母，数字和下划线，但必须以字母开头。

**dummyTable** 一个表对象，和输入的流数据表的 schema 一致，可以含有数据，亦可为空表。

**outputTable** 一个表对象，计算结果的输出表，可以是内存表或者分布式表。表结构比 dummyTable 多两列：

* 倒数第二列：INT 类型，标记该条逐笔数据的来源，不同标记值的含义如下：

| 标记值 | 逐笔委托 | 逐笔成交 |
| --- | --- | --- |
| 0 | 原始委托 | 原始成交 |
| 1 | 根据全部即时成交还原的委托 | 即时全部成交 |
| 2 | 根据部分即时成交还原的委托 | 即时部分成交 |

* 最后一列：LONG 类型，记录输出顺序，从 0 开始递增。

**inputColMap** 一个字典，用于将输入表中的列名映射到引擎计算所需的字段：

* **key** 为 STRING 类型，表示引擎所需的字段，字段及其说明见下表。注意，字段名大小写敏感，顺序不限但必须全部指定。
* **value** 为 STRING 类型，必须是 *dummyTable* 的列名。

| key | 字段类型 | 字段说明 |
| --- | --- | --- |
| "codeColumn" | SYMBOL | 证券代码 |
| "typeColumn" | INT | 交易类型：   * 如果是逐笔委托单，则：1 表示市价；2 表示限价；3 表示本方最优；10 表示撤单（仅上交所）；11   表示市场状态（仅上交所） * 如果是逐笔成交单，则：0 表示成交；1 表示撤单（仅深交所） |
| "priceColumn" | LONG | 价格 |
| "qtyColumn" | LONG | 数量（股数） |
| "buyOrderColumn" | LONG | * 逐笔成交：对应其原始成交中的买方委托序号。 * 上交所逐笔委托：填充原始委托中的原始订单号，即上交所在新增、删除订单时用以标识订单的唯一编号 * 深交所逐笔委托：填充 0。此字段为深交所为了补全上交所数据格式而增加的冗余列 |
| "sellOrderColumn" | LONG | * 逐笔成交：对应其原始成交中的卖方委托序号。 * 上交所逐笔委托：填充原始委托中的原始订单号，即上交所在新增、删除订单时用以标识订单的唯一编号 * 深交所逐笔委托：填充 0。此字段深交所为了补全上交所数据格式而增加的冗余列 |
| "sideColumn" | INT | 买卖方向：1 表示买单；2 表示卖单  说明：   * 委托单的 BSFlag，必填 * 撤单的 BSFlag 由原始委托单决定买卖方向，必填 * 成交单的 BSFlag，不影响结果，非必填 |
| "msgTypeColumn" | INT | 数据类型：   * 0 表示逐笔委托； * 1 表示逐笔成交； * -1 表示产品状态。 |

## 返回值

返回一个表对象，通过向该表对象写入，将数据注入引擎进行计算。

## 例子

运行以下示例前，请先下载 <demoData.tar.gz>

```
// 定义引擎参数 dummyTable，即指定输入表的表结构
colNames = `SecurityID`Date`Time`SourceType`Type`Price`Qty`BSFlag`BuyNo`SellNo`ApplSeqNum`ChannelNo
colTypes = [SYMBOL, DATE, TIME, INT, INT, LONG, LONG, INT, LONG, LONG, LONG, INT]
dummyOrderTrans = table(1:0, colNames, colTypes)

// 定义引擎参数 colMap，即指定输入表各字段的含义
colMap = dict(`codeColumn`typeColumn`priceColumn`qtyColumn`buyOrderColumn`sellOrderColumn`sideColumn`msgTypeColumn, `SecurityID`Type`Price`Qty`BuyNo`SellNo`BSFlag`SourceType)

// 定义引擎参数 outputTable ，即输出表
outTable =  table(1:0, colNames join ["mark","index"], colTypes join [INT,LONG])

// 定义引擎
engine1 = createSSEOrderReconstructionEngine(name="demo", dummyTable=dummyOrderTrans, outputTable=outTable, inputColMap=colMap)

// 向引擎插入数据，注意修改filename
schemaTB = select name, typeString as type from dummyOrderTrans.schema().colDefs
tmp = select * from loadText(filename="/home/data/orderReconstituteDemoInput.csv",schema=schemaTB) order by ApplSeqNum
engine1.append!(tmp)
```

outTable 是将 tmp 中数据还原出原始委托后的结果。例如：

**完全成交还原**

tmp 中 600125 标的在 09:30:02.710 时刻有四条成交记录，其中三条记录的卖单号均为 761962，一条记录的卖单号为
643170，均没有对应的委托记录![](../images/createSSEOrderReconstructionEngine1.png)。

经过引擎还原后，可以看到 outTable 中 index 分别为 5927 和 5931 的两条记录即为原始的委托信息，委托量分别为
5000（1500+200+3300）和 600，它们在提交时就立即全部成交。

![](../images/createSSEOrderReconstructionEngine2.png)

**部分成交还原**

tmp 中 600125 标的在 09:30:09.280 时刻有三条成交记录和一条委托记录，卖单号均为 829709。![](../images/createSSEOrderReconstructionEngine3.png)

经过引擎还原后，可以看到 outTable 中，index 为 6593 的记录为原始委托，原始委托量为 81900，等于 tmp 中的委托量 81600 与立即成交量
100 和 200 之和；index 为 6596 的记录为原始委托，在提交时立即全部成交。![](../images/createSSEOrderReconstructionEngine4.png)
