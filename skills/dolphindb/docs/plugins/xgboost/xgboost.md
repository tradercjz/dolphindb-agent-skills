<!-- Auto-mirrored from upstream `documentation-main/plugins/xgboost/xgboost.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# xgboost

XGBoost（eXtreme Gradient Boosting）是一个用于建立梯度提升树（Gradient Boosting Decision
Trees，GBDT）模型的开源机器学习库。xgboost 插件基于 [XGBoost 开源库](https://github.com/dmlc/xgboost)开发，可以调用 XGBoost 库函数，对 DolphinDB
的表执行训练、预测、模型保存和加载。

目前仅支持 1.2 和 3.1 两个版本的 XGBoost。但由于默认参数设置存在差异，两个版本的计算结果也会有一定差别。

更多功能推荐使用 py 插件调用 xgboost 实现。

## 在插件市场安装插件

### 版本要求

DolphinDB Server 2.00.10 及更高版本。插件对应的 XGBoost 版本与 DolphinDB Server 版本的关系对照如下：

* XGBoost 1.2：Windows x86-64 JIT
* XGBoost 3.1：Linux x86-64，Linux x86-64 ABI=1

### 安装步骤

1. 在 DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   注意：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可自行编译或在 [DolphinDB
   用户社区](https://ask.dolphindb.cn/)进行反馈。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 `installPlugin`
   命令完成插件安装。

   ```
   installPlugin("xgboost")
   ```
3. 使用 `loadPlugin`
   命令加载插件。

   ```
   loadPlugin("xgboost")
   ```

## 用户接口

### train

**语法**

```
xgboost::train(Y, X, [params], [numBoostRound=10], [model])
```

**详情**

对给定的表调用 XGBoost 库函数进行训练。返回值是训练得到的模型，可以用于继续训练或预测。

**参数**

**Y** 一个向量，表示因变量。

**X** 一个矩阵或一个表，表示自变量。

**params** 一个字典，表示 XGBoost 训练所用的参数，详情参考官方文档。

**numBoostRound** 一个正整数，表示 boosting 的迭代次数。

**model** 一个 XGBoost 模型，允许继续训练。可以通过该函数训练得到模型，或加载已有模型。

### predict（XGBoost 1.2 版本）

**语法**

```
xgboost::predict(model, X, [outputMargin=false], [ntreeLimit=0], [predLeaf=false], [predContribs=false], [training=false])
```

**详情**

对给定的表调用 XGBoost 库函数进行预测。

**参数**

**model** 用于预测的 XGBoost 模型。可以通过 `xgboost::train` 或
`xgboost::loadModel` 函数得到模型。

**X** 一个矩阵或一个表，表示用于预测的数据。

**outputMargin** 一个布尔值，表示是否输出原始的未经转换的边际值（raw untransformed margin value）。

**ntreeLimit** 一个非负整数，表示预测时使用的树的数量限制（默认值 0 表示使用所有树）。

**predLeaf** 一个布尔值。如果为 true，将返回一个形状为 (*样本数*，*树的个数*)
的矩阵，每一条记录表示每一个样本在每一棵树中的预测的叶节点的序号。

**predContribs** 一个布尔值。如果为 true，将返回一个形状为 (*样本数*，*特征数 + 1*)
的矩阵，每一条记录表示特征对预测的贡献（SHAP values）。所有特征贡献的总和等于未经转换的边际值（raw untransformed margin
value）。

**training** 一个布尔值。表示预测值是否用于训练。

关于以上参数的具体用途说明，参见官方文档。

### predict（XGBoost 3.1 版本）

**语法**

```
xgboost::predict(model, X, [type=0], [iterationRange], [strictShape=false], [training=false])
```

**详情**

对给定的表调用 XGBoost 库函数进行预测。

**参数**

**model** 用于预测的 XGBoost 模型。可以通过 `xgboost::train` 或
`xgboost::loadModel` 函数得到模型。

**X** 一个矩阵或一个表，表示用于预测的数据。

**type** 一个整型，可以为 0-6。具体含义为：

* 0：normal prediction
* 1：output margin
* 2：predict contribution
* 3：predict approximated contribution，
* 4：predict feature interaction
* 5：predict approximated feature interaction
* 6：predict leaf "training"

**iterationRange** 一个整型数据对，第一个数字为开始的迭代次数，第二个数字为结束的迭代次数。若未指定该参数，则会从模型元数据中读取
best\_iteration 作为迭代次数。在 Python 接口中，该参数默认设置为 0:0。

**strictShape** 一个布尔值，指示是否要以严格规则输出结果。

**training** 一个布尔值。表示预测值是否用于训练。

关于以上参数的具体用途说明，参见官方文档。

### saveModel

**语法**

```
xgboost::saveModel(model, filePath)
```

**详情**

将训练得到的 XGBoost 模型保存到磁盘。

**参数**

**model** 用于保存的 XGBoost 模型。

**filePath** 一个字符串，表示保存的路径。

### loadModel

**语法**

```
xgboost::loadModel(filePath)
```

**详情**

从磁盘上加载 XGBoost 模型。

**参数**

**filePath** 一个字符串，表示模型所在的路径。

## 示例

```
loadPlugin("xgboost")

// 创建训练表
t = table(1..5 as c1, 1..5 * 2 as c2, 1..5 * 3 as c3)
label = 1 2 9 28 65

// 设置模型参数
params = {objective: "reg:linear", max_depth: 5, eta: 0.1, min_child_weight: 1, subsample: 0.5, colsample_bytree: 1, num_parallel_tree: 1}

// 训练模型
model = xgboost::train(label, t, params, 100)

// 用模型预测
xgboost::predict(model, t)

// 保存模型
xgboost::saveModel(model, "001.model")

// 加载模型
model = xgboost::loadModel("001.model")

// 在已有模型的基础上继续训练
model = xgboost::train(label, t, params, 100, model)
```
