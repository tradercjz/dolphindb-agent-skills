# ridgeCV

## 语法

`ridgeCV(ds, yColName, xColNames, [alphas=[0.01,0.1,1.0]], [intercept=true],
[normalize=false], [maxIter=1000], [tolerance=0.0001], [solver='svd'],
[swColName])`

## 详情

使用五折交叉验证法进行岭回归（ridge）估计，输出最优参数对应的岭回归模型。

![](../../images/ridge.png)

## 参数

**alphas** 是浮点型标量或向量，表示乘以L1范数惩罚项的系数。默认值是 [0.01, 0.1, 1.0]。

注：

除 *alphas* 参数外，其它参数都和 ridge 的参数相同，参数描述可参考 ridge。这里仅说明 *alphas* 参数。

## 返回值

结果为一个字典，包含以下 key：

* modelName：模型名称，ridgeCV 方法对应的模型名为 "ridgeCV"。
* coefficients：模型的回归系数。
* intercept：截距。
* xColNames：数据源中自变量的列名。
* predict：用于预测的函数。
* alpha：交叉验证选择的惩罚量。

## 例子

```
y = [225.720746,-76.195841,63.089878,139.44561,-65.548346,2.037451,22.403987,-0.678415,37.884102,37.308288]
x0 = [2.240893,-0.854096,0.400157,1.454274,-0.977278,-0.205158,0.121675,-0.151357,0.333674,0.410599]
x1 = [0.978738,0.313068,1.764052,0.144044,1.867558,1.494079,0.761038,0.950088,0.443863,-0.103219]
t = table(y, x0, x1);

ridgeCV(t, `y, `x0`x1);
```

返回如下：

```
coefficients->[94.3410,14.2523]
predict->coordinateDescentPredict
modelName->ridgeCV
xColNames->[x0,x1]
intercept->0.1063
alpha->0.0100
```
