# logisticRegression

## 语法

`logisticRegression(ds, yColName, xColNames, [intercept=true], [initTheta],
[tolerance=1e-3], [maxIter=500], [regularizationCoeff=1.0],
[numClasses=2])`

## 详情

对数据源中的自变量（*xColNames*）和因变量（*yColName*）进行逻辑回归分析。生成的模型可以作为
`predict` 函数的输入，用于预测新数据的分类结果。

## 参数

**ds** 数据源类型，通常由 sqlDS 生成。

**yColName** 字符串，指定 *ds* 中的列名，表示因变量（所属分类）列。

**xColNames** 字符串标量或向量，指定 *ds* 中的列名，表示自变量列。

**intercept** 可选参数。布尔类型，表示是否包含截距项。默认值为 true，系统会自动添加一列值为 1 的变量用于生成截距。

**initTheta** 可选参数。DOUBLE 类型向量，指定迭代的初始参数。默认是长度为
`xColNames.size()+intercept` 的零向量。

**tolerance** 可选参数。大于 0 的数值标量，指定迭代终止的边界差值 。如果在两次相邻迭代中，参数的对数似然函数的梯度的绝对值最大分量的差小于
*tolerance*，则迭代终止。默认值是0.001。

**maxIter** 可选参数。正整数，指定迭代的最大次数。当迭代次数达到 *maxIter* 时，迭代终止。默认值是500.

**regularizationCoeff** 可选参数。大于 0 的数值标量，指定正则项系数。默认值是1.0。

**numClasses** 可选参数。大于等于 2 的整数，表示因变量的类别数量。默认值是 2。

## 返回值

一个字典，包含以下键值：

* modelName：字符串，表示模型的名称，即“Logistic Regression“。
* tolerance：浮点数，表示迭代终止的边界差值。
* xColNames：字符串标量或向量，表示自变量列名。
* intercept：布尔值，表示是否包含回归中的截距项。
* numClasses：正整数，表示因变量的类别数量。
* coefficients：浮点类型的矩阵或向量，表示每一个因变量种类模型参数的估计值。

  + 二元分类（*numClasses* = 2）时，返回向量，表示正类（即 label = 1）的参数的估计值。
  + 多元分类（*numClasses* > 2）时，返回矩阵，第 i 行表示第 i 类（即 label =
    i）参数的估计值。
* iterations：整型标量或向量，表示每一个因变量种类迭代的次数。

  + 二元分类（*numClasses* = 2）时，返回一个正整数，表示正类（即 label = 1）的参数的迭代次数。
  + 多元分类（*numClasses* > 2）时，返回一个向量，第 i 个数表示第 i 类（即 label =
    i）参数的迭代次数。
* logLikelihood：浮点类型的标量或向量，表示每一个因变量种类迭代中最终的对数似然值。

  + 二元分类（*numClasses* = 2）时，返回一个浮点数，表示正类（即 label = 1）的参数的对数似然值。
  + 多元分类（*numClasses* > 2）时，返回一个向量，第 i 个数表示第 i 类（即 label =
    i）参数的对数似然值。
* predict：模型的预测函数。

## 例子

以下例子把两个不同中心的正态分布标记为两类，然后计算逻辑回归模型。

```
t = table(100:0, `y`x0`x1, [INT,DOUBLE,DOUBLE])
y = take(0, 50)
x0 = norm(-1.0, 1.0, 50)
x1 = norm(-1.0, 1.0, 50)
insert into t values (y, x0, x1)
y = take(1, 50)
x0 = norm(1.0, 1.0, 50)
x1 = norm(1.0, 1.0, 50)
insert into t values (y, x0, x1)

model = logisticRegression(sqlDS(<select * from t>), yColName=`y, xColNames=`x0`x1);

// output
modelName->Logistic Regression
tolerance->0.001
xColNames->["x0","x1"]
intercept->1
numClasses->2
coefficients->[1.772463953718721,1.848711011775654,0.24896957744541]
iterations->[5]
logLikelihood->[15.982057280977643]
predict->logisticRegressionPredict
```

把模型用于预测：

```
predict(model, t);
```

保存模型到磁盘：

```
saveModel(model, "C:/DolphinDB/data/logisticModel.txt");
```

加载一个保存的模型：

```
loadModel("C:/DolphinDB/data/logisticModel.txt");
```
