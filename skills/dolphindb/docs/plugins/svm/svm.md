<!-- Auto-mirrored from upstream `documentation-main/plugins/svm/svm.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# SVM

支持向量机（Support Vector Machine, SVM）是一种监督学习算法，常用于分类和回归问题。DolphinDB 提供了 SVM 插件，使用户可以在 DolphinDB 中对 DolphinDB 对象执行 SVM 模型的训练和预测。插件基于 libsvm 进行实现，对常见的支持向量机算法进行了封装。

## 安装插件

### 版本要求

DolphinDB Server: 2.00.10 及更高版本，支持 Linux x86-64, Windows x86-64。

### 安装步骤

1. 在 DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   **注意**：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可[自行编译](https://gitee.com/dolphindb/DolphinDBPlugin)（请自行选择对应分支下的插件）或在 [DolphinDB 用户社区](https://ask.dolphindb.cn/)进行反馈。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   ```
   installPlugin("SVM")
   ```
3. 使用 `loadPlugin` 命令加载插件。

   ```
   loadPlugin("SVM")
   ```

## 接口说明

### fit

**语法**

```
svm::fit(Y, X, [params=None])
```

**详情**

根据给定的训练数据训练 SVM 模型。

返回一个 SVM 对象。

**参数**

**Y** 目标值向量，元素类型统一为 INT 类型或 DOUBLE 类型。

**X** 输入的训练数据 (可以为矩阵、表、向量)，元素类型为 DOUBLE。

* 当 X 为矩阵的时候，每一列代表一个样本，列中的元素代表属性值。
* 当 X 为表的时候，表中每列数据都必须是 DOUBLE 类型，每一行表示一个样本。
* 当 X 为向量的时候，`fit` 方法会根据 y 向量的长度将 X 均匀分成相应长度的样本。

**params** 一个字典，类型为 (STRING, ANY)，表示 SVM 训练参数。它包括如下键值:

* "type": 表示 SVM 类型。其值可以为 "NuSVC"、"NuSVR"、"OneClass"、"SVC"、"SVR"。
* "kernel": 表示核函数类型。其值可以为 "linear"、"poly"、"rbf"、"sigmoid"、"precomputed"。
* "degree": 表示核函数级数。其值为一个 INT 值。
* "gamma": 表示核函数的 gamma 参数。其值可以为 "scale" 或者 DOUBLE 值。
* "coef0": 表示核函数的 coef0 参数。其值为一个 DOUBLE 值，默认为 0。
* "C": 表示 C-SVC, epsilon-SVR, and nu-SVR 的 cost 参数。其值为一个 DOUBLE 值，默认为 1。
* "epsilon": 表示 epsilon-SVR 中的 epsilon 参数。其值为一个 DOUBLE 值，默认为 0.1。
* "shrinking": 表示是否使用 shrinking heuristics。其值为一个布尔值。默认为 true。
* "cache\_size": 表示核函数缓存的大小。其值为一个 DOUBLE 值，单位为 MB，默认为 100。
* "verbose": 表示是否进行详细输出。其值为一个布尔值，默认为 true。
* "nu": 表示边界误差的分数的上限）和支持向量的分数的下限。范围属于 (0,1]，其默认值为 0.5。

### predict

**语法**

```
svm::predict(model, X)
```

**详情**

根据 SVM 模型和测试数据进行分类或者回归。

返回一个向量，向量中的值为预测的样本标签值或回归值。

**参数**

**model** 一个 SVM 对象。

**X** 输入的测试数据，元素类型为 DOUBLE。其类型可以为矩阵、表、向量。

### score

**语法**

```
svm::score(model, Y, X)
```

**详情**

根据给定的测试数据和标签值计算已有 SVM 的模型的准确性，并返回统计指标。其中 SVM 模型由一个 SVM 对象给出。

如果是分类模型，返回预测的准确率。如果是回归模型，返回 MSE 和 R2。

**参数**

**model** 一个 SVM 对象。

**Y** 真实目标值向量。

**X** 输入的测试数据矩阵。其类型可以为矩阵、表、向量。

### saveModel

**语法**

```
svm::saveModel(model, filePath)
```

**详情**

将已经训练好的 SVM 模型保存。

返回一个布尔值，表示模型是否保存成功。

**参数**

**model** 一个 SVM 对象。

**filePath** STRING 类型标量，表示文件路径。

### loadModel

**语法**

```
svm::loadModel(filePath)
```

**详情**

将文件形式的 SVM 模型导入到内存中。

返回一个 SVM 对象。

**参数**

**filePath** STRING 类型标量，表示文件路径。

## 使用示例

### 例1 SVM 分类模型

训练模型：

```
path="/path/to/PluginSVM.txt";
modelPath="/path/to/mymodel"
loadPlugin(path)
X = matrix(-1.0 -1.0,-2.0 -1.0, 1.0 1.0, 2.0 1.0)
Y = 1.0 1.0 2.0 2.0
clf = fit(Y, X)
```

用模型进行预测：

```
predict(clf, X)
// output: [1,1,2,2]
```

评估模型：

```
score(clf, Y, X);
//output : 1
```

将模型保存：

```
saveModel(clf, modelPath)
```

### 例2 SVM 回归模型

训练模型：

```
path="/path/to/PluginSVM.txt";
modelPath="/path/to/mymodel";
loadPlugin(path);
X = table(1 3 5 7 11 16 23 as X)
Y = 0.1 4.2 5.6 8.8 22.1 35.6 77.2
regr = fit(Y, X, {type: "SVR"})
```

评估模型：

```
score(regr, Y, X);
/*
MSE->797.772
R2->0.582937
*/
```
