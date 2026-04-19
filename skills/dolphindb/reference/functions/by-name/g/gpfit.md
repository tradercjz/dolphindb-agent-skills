# gpFit

## 语法

`gpFit(engine, [programNum=1], [programCorr=false])`

注：

社区版 License 暂不支持该函数，如需使用此功能，请联系技术支持。

## 详情

查看训练生成的公式。

## 参数

**engine** 通过函数 createGPLearnEngine 创建引擎的返回对象。

**programNum** 整型标量，表示训练完返回的公式数量。

**programCorr** 布尔标量，指示是否返回公式之间的相关性。

## 返回值

返回一个表：

* 第一列为 program 列，STRING 类型，用于存储得到的公式；
* 第二列为 fitness 列，DOUBLE 类型，存储公式的适应度；
* 当 programCorr 为 true 时，第三列为 programCorr 列，是DOUBLE 类型的数组向量，存储公式之间的相关性。

## 例子

参考：Shark GPLearn 快速上手。

**相关信息**

* [Shark GPLearn 快速上手](../../tutorials/gplearn.html "Shark GPLearn 快速上手")
