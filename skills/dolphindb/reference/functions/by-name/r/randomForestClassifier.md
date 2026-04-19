# randomForestClassifier

## 语法

`randomForestClassifier(ds, yColName, xColNames,
numClasses, [maxFeatures=0], [numTrees=10], [numBins=32], [maxDepth=32],
[minImpurityDecrease=0.0], [numJobs=-1], [randomSeed])`

## 详情

计算指定数据源中 *yColName* 和 *xColNames* 随机森林分类。

生成的模型可以作为 `predict` 函数的输入

## 参数

**ds** 是数据源，通常用sqlDS函数生成。

**yColName** 是字符串，表示数据源中作为因变量（所属分类）的列名。

**xColNames** 是字符串标量或向量，表示数据源中作为自变量的列名。

**numClasses** 是正整数，表示分类数目。y 列的取值必须是[0, numClasses)之间的整数。

**maxFeatures** 是一个整数或浮点数，表示一次分裂节点选取的特征个数或比例。默认值是0。

* 如果 *maxFeatures* 为正整数，则在一次分裂时选取
  *maxFeatures* 个特征。
* 如果 *maxFeatures* =0，则在一次分裂时选取 sqrt(特征列数量)
  个特征。
* 如果 *maxFeatures* 是一个0和1之间的浮点数，则在一次分裂时选取
  int(特征列数量\**maxFeatures*) 个特征。

**numTrees** 是正整数，表示森林中树的个数。默认值为10。

**numBins** 是正整数，表示离散化连续特征时的桶数。默认值为32。增加 *numBins*
会使算法考虑更多的分裂结点的决策值，产生更好的分裂结果，但也会提高计算量和通讯量。

**maxDepth** 是正整数，表示树的最大深度。默认值为32。

**minImpurityDecrease** 是浮点数，如果分裂产生的基尼指数纯度减少值大于或等于这个值，结点会继续分裂。

**numJobs** 是一个整数，表示训练时使用的任务数。它是可选参数，默认值为-1，表示训练时使用所有的线程。如果
*numJobs* 小于-1，假如设置的 localExecutor 参数为 n，产生的任务数为
(n+2+numJobs)。实际执行过程中，最多会产生 min(numTrees, n+1)个任务。如果 *ds*
中有数据源位于远程节点，该参数不起作用，只产生一个任务。

**randomSeed** 是随机数生成器使用的种子。

## 返回值

返回结果是字典，包含以下 key：numClasses, minImpurityDecrease, maxDepth, numBins, numTress,
maxFeatures, model, modelName, xColNames。其中 model 是一个元组，保存了训练生成的树；modelName 为
“Random Forest Classifier”。

## 例子

用模拟数据训练一个随机森林回归模型

```
t = table(100:0, `cls`x0`x1, [INT,DOUBLE,DOUBLE])
cls = take(0, 50)
x0 = norm(-1.0, 1.0, 50)
x1 = norm(-1.0, 1.0, 50)
insert into t values (cls, x0, x1)
cls = take(1, 50)
x0 = norm(1.0, 1.0, 50)
x1 = norm(1.0, 1.0, 50)
insert into t values (cls, x0, x1)

model = randomForestClassifier(sqlDS(<select * from t>), `cls, `x0`x1, 2);
```

把模型用于预测

```
predict(model, t)
```

加载一个保存的模型

```
loadModel("C:/DolphinDB/data/classifierModel.bin")
```

相关函数：adaBoostRegressor, adaBoostClassifier, randomForestRegressor
