# gpPredict

## 语法

`gpPredict(engine, input, [programNum = 1], [groupCol],
[deviceId=0])`

注：

社区版 License 暂不支持该函数，如需使用此功能，请联系技术支持。

## 详情

采用上次训练得到的适应度函数较小的前 programNum 个公式用于预测。如果指定 groupCol，计算时还会依据 groupCol 分组。

## 参数

**engine** 通过函数 createGPLearnEngine 创建引擎的返回对象。

**input** 浮点型的表，表示需要预测的数据。

**programNum** 整型标量，表示参与预测的公式数量，默认为 1。

**groupCol** 字符型标量，表示进行分组的列名，默认为空。此列不会参与计算。

**deviceId** INT类型的标量或向量。当前机器拥有多卡时，可以指定使用的设备 ID，默认为 0 。

## 返回值

返回一个表，共 programNum 列，列名为 gpFit 训练得到的公式。

## 例子

参考：Shark GPLearn 快速上手。

**相关信息**

* [Shark GPLearn 快速上手](../../tutorials/gplearn.html "Shark GPLearn 快速上手")
