# setGpFitnessFunc

## 语法

`setGpFitnessFunc(engine, func, [funcArgs])`

注：

社区版 License 暂不支持该函数，如需使用此功能，请联系技术支持。

## 详情

重置 GPLearn 引擎的适应度函数。

## 参数

**engine**  通过函数 `createGPLearnEngine` 创建引擎的返回对象。

**func** 替换后的适应度函数，可以是

* 字符串类型标量，必须为 'mse', 'rmse', 'pearson', 'spearmanr', 'mae' 之一。
* 用户自定义函数，至少包含两个入参，第一个参数代表因子计算结果，第二个参数代表预测值，如有其他参数，则通过 *funcArgs*传递；函数的返回值必须是一个浮点型标量。自定义函数目前不支持复杂赋值、if、for 等语句，只支持 return 语句。return
  值为支持的适应度函数和训练函数的组合，其中适应度函数需要手动写公式实现。例如：

  ```
  def f(x, y){
    return mean((x+y)*(x+y)-y*y)
  }
  ```

自定义的适应度函数，还可与辅助函数进行组合，从而实现在计算适应度前，对数据进行预处理。辅助函数如下所示

| **函数名** | **备注** |
| --- | --- |
| clip(X,Y,Z) |  |
| zscore(x) |  |
| mad(X, [useMedian=false]) |  |
| med(x) |  |
| mean(x) |  |
| corr(X,Y) |  |
| groupby(func, funcArgs, groupingCol) |  |
| std(X) |  |
| stdp(X) |  |
| skew(X) |  |
| kurtosis(X) |  |
| contextby(func, funcArgs, groupingCol, [sortingCol]) | 仅支持 *func* 为辅助函数 `rank` 或 `zscore`。 |
| rank(X, [ascending=true], [groupNum], [ignoreNA=true], [tiesMethod='min'], [percent=false], [precision]) | 暂不支持设置参数 *groupNum*, *ignoreNA*, *precision*. |

**funcArgs** 元组，其每个元素依次代表用户自定义的 *func* 中除因子计算结果和预测值外的其他参数。

## 例子

```
def myFitness(x, y, groupCOlA, groupColB) {
  return mean(abs(groupby(mean, y, groupColB) - groupby(mean, x, groupColA)))
}
setGpFitnessFunc(engine=myEngine, func=myFitness, funcArgs=[groupColA, groupColB])
```
