<!-- Auto-mirrored from upstream `documentation-main/plugins/lgbm.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# lgbm

lgbm 插件用于调用 LightGBM 库，能够高效地对 DolphinDB 进行分类和回归。具体功能包括：

* 快速训练：利用 LightGBM 算法对数据进行训练，生成模型。
* 预测：使用训练好的模型对新数据进行预测。
* 模型的保存与加载：可以将训练好的模型保存为文件，方便后续加载以进行预测，无需重新训练。

该插件基于 LightGBM 4.5.0 版本的 SDK 开发。

更多功能推荐使用 py 插件调用 LightGBM 实现。

## 安装插件

### 版本要求

DolphinDB Server: 2.00.13 及更高版本，插件只支持 Linux 和 Linux\_ABI。

### 安装步骤

1. 使用 `listRemotePlugins` 命令完成插件安装。

   注意：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可自行编译或在 [DolphinDB
   用户社区](https://ask.dolphindb.cn/)进行反馈。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   ```
   installPlugin("lgbm")
   ```
3. 使用 `loadPlugin` 命令加载插件。

   ```
   loadPlugin("lgbm")
   ```

## 接口说明

### train

**语法**

```
lgbm::train(X,Y,[numIterations=100],[params])
```

**参数**

**X** 是一个表，其中每一列都需要是数值类型，表示输入特征集。如果 *X* 中某行存在空值，则该行数据将不被用于训练。

**Y** 是一个数值类型向量，表示标签列。如果 *Y* 中出现空值，则 *X* 中对应行的数据将不被用于训练。

**numIterations** 可选参数，非负整值，表示执行一次回归训练所用的迭代次数，默认为 100。

**params** 可选参数，一个字典，用于配置相关参数。可配置的选项具体参考官方文档。常用参数：

* objective：字符串标量，目标函数名称，默认为 'regression'。
* boosting：字符串标量，目前仅支持 'gbdt'。
* learning\_rate：浮点数，表示学习率，默认为 0.1。
* min\_data\_in\_leaf：非负整数，表示叶子节点最少数据点个数，默认为 20。

**详情**

在给定数据集上对 lgbm 模型进行回归训练。

返回值：返回一个训练好的 lgbm 模型。

### predict

**语法**

```
lgbm::predict(model, X)
```

**参数**

**model** 一个训练好的 lgbm 模型。

**X** 是一个表，表示输入的特征集。如果 X 中出现空值，该数据行对应的预测的结果不具备可参考性。

**详情**

对给定特征集进行回归预测。

返回值：一个向量。

### saveModel

**语法**

```
lgbm::saveModel(model, filePath)
```

**参数**

**model** 要保存的 lgbm 模型。

**filePath** 字符串标量，表示模型文件的保存路径，格式如 "XXX/model.txt"。

**详情**

将模型保存为文件。

返回值：无。

### loadModel

**语法**

```
lgbm::loadModel(filePath)
```

**参数**

**filePath** 字符串标量，模型文件的路径，格式如 "XXX/model.txt"。

**详情**

从文件中加载模型。

返回值：lgbm 模型。

### getParam

**语法**

```
lgbm::getParam(model)
```

**参数**

**model**
`loadModel` 接口返回的 lgbm 模型。

**详情**

返回模型信息。

返回值：一个字典，包含如下键值："objective", "num\_class", "feature\_names", "max\_feature\_idx",
"tree\_sizes"。

## 使用示例

```
loadPlugin("lgbm")

// 创建训练集
x1=rand(10,100)
x2=rand(10,100)
Y=2*x1+3*x2
X=table(x1,x2)

// 设置模型参数
num_iteration=500
params = {task:"train",min_data_in_leaf:"5"}

// 模型训练
model=lgbm::train(X,Y,num_iteration,params);

// 创建测试集
x1=rand(10,10)
x2=rand(10,10)
X=table(x1,x2)
Y=2*x1+3*x2

// 模型预测
pred=lgbm::predict(model,X);

// 计算拟合率
fitGoodness = 1 - (pred - Y).sum2() / (Y - Y.avg()).sum2()

// 模型保存
path="/path/to/model.txt";
lgbm::saveModel(model, path)

//模型加载
model1=lgbm::loadModel(path);

// 使用从文件加载的模型进行预测
pred=lgbm::predict(model1, X);

// 计算拟合率
fitGoodness = 1 - (pred - Y).sum2() / (Y - Y.avg()).sum2()
```
