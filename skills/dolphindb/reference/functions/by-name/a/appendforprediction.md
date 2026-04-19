# appendForPrediction

## 语法

`appendForPrediction(engine, data)`

## 详情

与函数 `createYieldCurveEngine` 结合使用，用于对输入引擎的数据进行预测。

**返回值：**一个整型标量，表示预测数据的数量。

## 参数

**engine** 一个字符串，表述预测的债券曲线拟合引擎名；也可以是引擎句柄。

**data** 表，表示进行预测的数据。注意：须与对应债券曲线拟合引擎中参数 *predictDummyTable* 的结构保持一致。

## 例子

首先创建一个曲线拟合引擎。

```
//指定传入表结构、资产类型、拟合算法
dummyTable = table(1:0, `symbol`sendingtime`askDirtyPrice1`bidDirtyPrice1`midDirtyPirce1`askyield1`bidyield1`midyield1`timetoMaturity`assetType`datasource`clearRate,
                        [SYMBOL, TIMESTAMP,DECIMAL32(3),DECIMAL32(3),DECIMAL32(3),DECIMAL32(3),DECIMAL32(3),DECIMAL32(3),DOUBLE,INT,INT,STRING])
assetType=[0,1,2]
fitMethod=[<piecewiseLinFit(timetoMaturity, midyield1, 10)>,
            <nss(timetoMaturity,bidyield1,"ns")>,
            <piecewiseLinFit(timetoMaturity, askyield1, 5)>]
//指定模型输出表
modelOutput=table(1:0, `time`assetType`dataSource`clearRate`model,
                        [TIMESTAMP,INT,INT,SYMBOL,BLOB])

//基于上述参数创建曲线拟合引擎
engine = createYieldCurveEngine(name="test", dummyTable=dummyTable,assetType=assetType,fitMethod=fitMethod,
                                keyColumn=`assetType`dataSource`clearRate, modelOutput=modelOutput,
                                frequency=10, fitAfterPredict=false)
```

然后进行预测。

```
data = table(take(`a`b`c, 30) as  symbol, take(now(), 30) as time, decimal32(rand(10.0, 30),3) as p1,  decimal32(rand(10.0, 30),3) as p2,  decimal32(rand(10.0, 30),3) as p3, decimal32(rand(10.0, 30),3) as p4,  decimal32(rand(10.0, 30),3) as p5,  decimal32(rand(10.0, 30),3) as p6, (rand(10.0, 30)+10).sort() as timetoMaturity, take(0 1 2, 30) as assetType, take([1], 30) as datasource, take("1", 30) as clearRate)
appendForPrediction(engine, data)
//Output: 30
```

**相关函数** [createYieldCurveEngine](../c/createyieldcurveengine.md)
