# createGPLearnEngine

## 语法

`createGPLearnEngine(trainData, targetData,[groupCol=''],
[populationSize=1000], [generations=20], [tournamentSize=20],
[stoppingCriteria=0.0], [constRange], [windowRange], [initDepth],
[initMethod='half'], [initProgram=''], [functionSet], [maxSamples=1.0],
[fitnessFunc='mse'], [parsimonyCoefficient=0.001], [crossoverMutationProb=0.9],
[subtreeMutationProb=0.01], [hoistMutationProb=0.01], [pointMutationProb=0.01],
[eliteCount =0], [restrictDepth=false], [deviceId=0], [seed], [verbose=true],
[minimize=true], [useAbsFit=true], [dimReduceCol=''])`

注：

社区版 License 暂不支持该引擎，如需使用此功能，请联系技术支持。

## 详情

创建一个 GPLearn 引擎用于训练和预测。

## 参数

* **trainData** 是 FLOAT 或 DOUBLE 类型的表，表示用于训练的数据。
* **targetData** 是 FLOAT 或 DOUBLE 类型的向量，需要预测的数据。targetData 与 trainData
  的数据类型必须一致。
* **groupCol** 字符串标量或向量，表示分组列名，可将数据按照此参数指定的列进行分组后计算。默认为空，表示无分组列。

  注：

  分组列本身不会参与计算。
* **populationSize** 整型标量，表示每代公式的数量， 默认值为 1000。
* **generations** 整型标量，表示进化的代数，默认为 20。
* **tournamentSize** 整型标量，表示生成下一代公式时，参与竞争的公式数量，默认为 20。
* **stoppingCriteria** 浮点型标量，表示终止迭代的适应度阈值。当适应度小于等于此阈值时，会提前结束进化。默认为
  0，表示达到进化的代数之前不会停止。
* **constRange** 可以是 0 或长度为 2 的浮点型向量，表示公式中包含的常量的范围，默认为 [-1.0, 1.0]。
  + 为 0 时，公式中将不会包含常量。
  + 为向量时，向量的两个元素代表闭区间边界。
* **windowRange** 整型向量，表示滑动窗口函数的窗口大小取值范围，滑动窗口的大小是此向量中的随机值，默认为 [2, 3, 4, 5, 6,
  7, 8, 9, 10, 15, 20, 30, 7, 14, 21, 48, 35, 42]。
* **initDepth** 长度为 2 的整型向量，表示初始化公式树的深度范围，默认是 [2, 6]。
* **initMethod** 字符串类型标量，用于指定初始化公式树的方法，默认为 half 。
  + grow 公式树中的每一个节点，都是从函数、常量和变量中随机选取
  + full 只有公式树的叶子节点可以是常量或变量
  + half 公式树的子树，将会有50%/50%的概率通过 grow/full 生成
* **initProgram** 元代码或元代码的元组，默认为空。指定此参数，将会用指定的元代码初始化种群。例如
  `<mavg(price, 10)>` ，其中 mavg 是 GPLearn 已经支持的函数， price 是
  *trainData* 中的列。
* **functionSet**
  初始化公式树和进化时选择的算子，为字符串类型的向量。默认值为空，表示可以使用所有支持的算子。支持的算子列表详见附录。
* **maxSamples** 浮点型标量，表示参与 fitnessFunc 计算的输入数据的比例，取值范围是 [0,1]，默认是 1.0 。
* **fitnessFunc** 用户自定义的 FUNCTIONDEF 类型标量，或字符串标量，代表适应度函数。默认是 'mse'，字符串可选值为：
  + 'mse'，均方误差。
  + 'rmse'，均方根误差。
  + 'pearson'，皮尔逊矩阵相关系数。
  + 'spearmanr'，Spearmanr 排序相关系数。
  + 'mae'，平均绝对误差。
* **parsimonyCoefficient**
  浮点型标量，表示节俭系数。随着进化次数的增加，公式会越来越膨胀，失去可解释性，节俭系数会惩罚过长的公式。默认为 0.0 。
* **crossoverMutationProb** 浮点型标量，表示 crossover 的概率，默认是 0.9 。
* **subtreeMutationProb** 浮点型标量，表示 subtree 变异的概率，默认是 0.01 。
* **hoistMutationProb** 浮点型标量，表示 hoist 变异的概率，默认是 0.01 。
* **pointMutationProb** 浮点型标量，表示 point 变异的概率，默认是 0.01 。

注：

所有变异概率之和必须小于等于 1

* **eliteCount** INT 类型标量，代表精英数量，默认为 0。适应度最优的 eliteCount
  个公式，会作为精英直接传递给下一代。
* **restrictDepth** 布尔类型标量，代表是否严格限制公式的长度，默认为 false。设置为 true 时，公式的深度不会超过
  initDepth 的上限。
* **deviceId** INT类型的标量或向量。当前机器拥有多卡时，可以指定使用的设备 ID，默认为 0 。
* **seed** 整型标量，表示训练时使用的种子。
* **verbose** BOOL 类型标量，设置是否输出训练时的信息，默认是 true。
* **minimize** BOOL 类型标量，设置是否向适应度最小化的方向进化。默认是
  true，则认为适应度越小，公式越优秀；反之则认为适应度越大，公式越优秀。
* **useAbsFit** 在计算适应度时是否取绝对值。可选参数，默认为 true，表示取绝对值。设置为 false 时，当
  *fitnessFunc* 设置为 'pearson'，'spearmanr' 或
  `corr`时，不取绝对值。
* **dimReduceCol** 可选参数，STRING
  类型标量或向量，表示分组列，计算将根据该参数指定的列进行分组聚合。指定此参数后，挖掘出的公式将包含降频算子。注意：若指定此参数，必须确保预测数据
  *targetData* 与训练数据 *trainData* 按 *dimReduceCol*
  分组聚合并按升序排序后的顺序一致。

## 返回值

一个表对象。

## 例子

参考：Shark GPLearn 快速上手

**相关信息**

* [Shark GPLearn 快速上手](../../tutorials/gplearn.html "Shark GPLearn 快速上手")
