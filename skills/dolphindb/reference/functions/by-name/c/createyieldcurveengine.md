# createYieldCurveEngine

## 语法

`createYieldCurveEngine(name, dummyTable, assetType, fitMethod, keyColumn,
modelOutput, frequency, [timeColumn], [predictDummyTable],[predictInputColumn],
[predictKeyColumn],[predictTimeColumn], [predictOutput],
[extraMetrics],[fitAfterPredict=false])`

## 详情

创建利率（或收益率）曲线引擎，将曲线拟合到输入资产值。主要用于金融领域，对各种金融工具的利率和剩余期限之间的关系进行建模。也可以根据所需的剩余期限进行收益率预测。当前支持的资产类型为债券。

引擎根据指定的拟合方法（*fitMethod*）采用不同的插值或拟合技术来构建和预测收益率曲线。支持的方法包括：线性插值、三次样条插值、Krogh
插值、分段回归、多项式拟合和 NS/NSS 模型。

## 参数

**name** 字符串标量，表示引擎的名称。该参数是引擎在一个数据/计算节点上的唯一标识，可包含字母，数字和下划线，但必须以字母开头。

**dummyTable** 表，用于指定输入数据的表结构。如：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| symbol | SYMBOL | 合约名 |
| sendingTime | TIMESTAMP | 行情时间 |
| askDirtyprice1 | DECIMAL | 卖一全价 |
| bidDirtyprice1 | DECIMAL | 买一全价 |
| midDirtyprice1 | DECIMAL | 中间价全价 |
| askyield1 | DECIMAL | 卖一收益率 |
| bidyield1 | DECIMAL | 买一收益率 |
| midyield1 | DECIMAL | 中间价收益率 |
| timetoMaturity | DOUBLE | 剩余到期期限 |
| assetType | INT/STRING | 资产类型，用户可以自定义，例如 1 或 “CDB” 表示国开 |
| dataSource | INT | 数据源，用户可以自定义，例如 0 表示 X-Bond，1 表示 ESP |
| clearRate | STRING | 清算速度，例如 "T0”，“T1”，“T2” |

**assetType** 整型/字符串向量，表示资产类型，必须和 *dummyTable* 中的 assetType 里的类型保持一致。通过该参数可以和
*fitMethod* 指定的拟合方法建立映射关系。输入示例：[0,1,2]。

**fitMethod**元代码元组，用于指定不同资产对应的拟合算法和对应参数。目前支持的算法如下：cubicSpline,
cubicHermiteSplineFit, kroghInterpFit, linearInterpolateFit, ns, nss,
piecewiseLinFit, polyFit。

注： 该参数的长度须和参数 *assetType*
保持一致。

**keyColumn**字符串标量（“assetType”）或向量。若为字符串向量，则第一个元素是
“assetType”，其他元素作为一个资产内部的分组列，引擎将在分组内拟合模型。

**modelOutput** 模型输出表，输出列顺序应遵守下述顺序：

1. 时间列，表示模型更新时间。
2. 分组列，列顺序与 *keyColumn* 设置的顺序一致。
3. 模型，BLOB 类型。

**frequency** 一个正整数或 DOURATION 类型标量，表示模型的更新频率：

* 指定为正整数，将按照数据条数更新模型，即每组未参与模型拟合的数据条数累计到设定值后更新模型。
* 指定为 DURATION 标量，若同时指定
  *timeColumn*，则根据每组未参与模型拟合的数据时间更新模型。每组分开判断，起始时间按每组第一条数据规整，每隔
  *frequency* 时间输出一次拟合模型；如果窗口内没收到数据则不输出。示例：假设收到的数据时间如下：09:30:00.100,
  09:32:00.100, 09:35:00.100, 09:45:00.100, 09:50:00.100，同时 *frequency* =
  5m, 则 model 输出的时间为 09:35:00.000, 09:40:00.000, 09:50:00.000。右边界为开，即
  09:35:00.000 输出的 model 的拟合数据不包括 09:35:00.000。
* 指定为 DURATION 标量，若同时未指定
  *timeColumn*，则按照系统时间更新每组的模型。起始时间按第一条数据进到引擎的时间规整；如果窗口内没收到数据则不输出。

**timeColumn** 可选参数，时间类型向量，用于指定输入表中的时间列。

**predictDummyTable** 可选参数，表示预测的输入数据表结构。默认和 *dummyTable* 一致。

**predictInputColumn** 可选参数，字符串标量，表示预测数据的输入列名。

**predictKeyColumn** 可选参数，字符串标量或向量，表示分组列，默认和 *keyColumn* 一致。

**predictTimeColumn** 可选参数，表示预测数据的时间列，默认和 *timeColumn* 一致。

**predictOutput** 可选参数，表示预测结果输出表。输出列遵循如下顺序：

1. 时间列，类型和 *predictTimeColumn* 保持一致；如果未指定
   *predictTimeColumn*，则输出系统时间（类型为 TIMESTAMP）。
2. 分组列，和 *predictKeyColumn* 指定的列顺序一致。
3. 预测输入列。
4. 预测结果。
5. *extraMetrics* 表示额外指定输出的算子。

注： 如果不设置参数 *predictOutput*，则引擎只用于拟合模型。

**extraMetrics** 可选参数，元代码或元代码元组。可以是 *predictDummyTable* 中的列（*keyColumn*
除外）或因子。

**fitAfterPredict** 可选参数，布尔标量。

* 如果为 true，表示 *predictDummyTable* 和 *dummyTable*
  一样，引擎收到数据后先用之前的模型预测输出，再使用这些数据拟合模型。
* 如果为 false（默认值），表示仅进行模型拟合而不进行预测。在这种情况下，如果需要进行预测，则必须使用
  `appendForPredict` 函数来完成。

## 例子

指定参数，创建一个曲线拟合引擎，最后进行拟合。

```
//指定传入表结构、资产类型、拟合算法
dummyTable = table(1:0, `symbol`sendingtime`askDirtyPrice1`bidDirtyPrice1`midDirtyPirce1`askyield1`bidyield1`midyield1`timetoMaturity`assetType`datasource`clearRate,
                        [SYMBOL, TIMESTAMP,DECIMAL32(3),DECIMAL32(3),DECIMAL32(3),DECIMAL32(3),DECIMAL32(3),DECIMAL32(3),DOUBLE,INT,INT,STRING])
assetType=[0,1,2]
fitMethod=[<piecewiseLinFit(timetoMaturity, midyield1, 10)>,
            <nss(timetoMaturity,bidyield1,"ns")>,
            <piecewiseLinFit(timetoMaturity, askyield1, 5)>]

//指定模型输出表和预测结果输出表
modelOutput=table(1:0, `time`assetType`dataSource`clearRate`model,
                        [TIMESTAMP,INT,INT,SYMBOL,BLOB])
predictOutput=table(1:0, `time`assetType`dataSource`clearRate`x`y,[TIMESTAMP,INT,INT,SYMBOL,DOUBLE,DOUBLE])

//基于上述参数创建曲线拟合引擎
engine = createYieldCurveEngine(name="test", dummyTable=dummyTable,assetType=assetType,fitMethod=fitMethod,
                                keyColumn=`assetType`dataSource`clearRate, modelOutput=modelOutput,
                                frequency=10,predictInputColumn=`timetoMaturity,predictTimeColumn=`sendingtime,
                                predictOutput=predictOutput,fitAfterPredict=true)

//创建数据，进行拟合
data = table(take(`a`b`c, 30) as  symbol, take(now(), 30) as time, decimal32(rand(10.0, 30),3) as p1,  decimal32(rand(10.0, 30),3) as p2,  decimal32(rand(10.0, 30),3) as p3, decimal32(rand(10.0, 30),3) as p4,  decimal32(rand(10.0, 30),3) as p5,  decimal32(rand(10.0, 30),3) as p6, (rand(10.0, 30)+10).sort() as timetoMaturity, take(0 1 2, 30) as assetType, take([1], 30) as datasource, take("1", 30) as clearRate)
engine.append!(data)
```

**相关函数**
[appendForPrediction](../a/appendforprediction.md)
