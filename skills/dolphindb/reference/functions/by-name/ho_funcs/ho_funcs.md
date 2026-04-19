# 高阶函数

## 介绍

DolphinDB内置的高阶函数，可以扩展或增强函数或者运算符的功能。高阶函数以一个函数与数据对象作为输入内容，类似于一个函数和数据之间的管道。通常，输入数据首先以一种预设的方式被分解成多个数据块（可能重叠），然后将函数应用于每个数据块，最后将所有的结果组合为一个对象返回。高阶函数的输入数据可以是向量、矩阵或者表，也可以是标量或字典。通过使用高阶函数，某些复杂的分析任务可以用几行代码就可以高效地完成。

## 语法

高阶函数总是与运算符、用户自定义函数或者系统函数共同使用。所有的高阶函数符号以冒号开头，之后紧跟一个大写字母。

`higherOrderFunctionName (<functionName>,
functionParameter1, ...functionParameterN)`

或

`<functionName> :<higher order symbol>
functionParameter`

或

`functionParameter1 <functionName> :<higher order
symbol> functionParameter2`

DolphinDB中，所有高阶函数的第一个参数必须是一个函数名，不可以是函数名数组。如果需要在同一个高阶函数中调用多个函数，可以指定该高阶函数的第一个参数为
*call* 高阶函数，然后在 *call* 的参数中指定多个函数，详情请见 call。

注意：从 2.00.5 版本开始，高阶函数的第一个参数会被强制解析为函数。

## 高阶函数总结

下面的表中，总结了高阶函数的名字和应用场景。

| 符号 | 函数名 | 应用范围 | 典型应用 |
| --- | --- | --- | --- |
| :E | each | 二元运算符，一元运算符，函数调用 | [多因子Alpha策略回测](https://ask.dolphindb.cn/blog/13) |
|  | peach | 并行版本的each |  |
| :R | eachRight | 二元运算符 |  |
| :L | eachLeft | 二元运算符 |  |
| :P | eachPre | 二元运算符 | [国内股票行情数据导入实例](https://ask.dolphindb.cn/blog/42) |
| :O | eachPost | 二元运算符，函数调用 |  |
|  | pivot | 函数调用 | 原始数据或分组聚合结果进行行列转置 |
| :A | accumulate | 二元运算符，函数调用 |  |
| :T | reduce | 二元运算符，函数调用 |  |
| :G | groupby | 函数调用，二元运算符 | [最简最快的WorldQuant 101 Alpha因子实现](https://ask.dolphindb.cn/blog/7) |
| :C | cross | 二元运算符，函数调用 | [多因子Alpha策略最佳因子权重](https://ask.dolphindb.cn/blog/17) |
|  | pcross | 并行版本的cross | [高频数据处理技巧：数据透视的应用](https://ask.dolphindb.cn/blog/21) |
|  | moving | 函数调用（聚合函数），二元运算符 | [寻找相似的历史k线](https://ask.dolphindb.cn/blog/16) |
|  | window | 函数调用 | 应用同 moving。moving 的窗口右边界固定，但 window 函数的左右边界均可自由设定 |
|  | nullCompare | 函数调用，二元运算符 | 保留运算中的空值，使运算结果和 Python 的保持一致。 |
|  | loop | 二元运算符，一元运算符，函数调用，混合返回类型 | [DolphinDB文本数据加载教程](https://ask.dolphindb.cn/blog/76) |
|  | ploop | 并行版本的loop |  |
|  | all | 二元运算符，函数调用 |  |
|  | any | 二元运算符，函数调用 |  |
|  | call | 二元运算符 | 通常与each函数配合使用，实现同时调用一批函数。其入参个数不确定 |
|  | pcall | 并行版本的call |  |
|  | unifiedCall | 函数调用 | 应用同 call，其只接收1个入参 |
| :X | contextby | 函数调用，二元运算符 | 分组内进行指定的计算 |
|  | segmentby | 函数调用，二元运算符 | [技术信号回测](https://ask.dolphindb.cn/blog/12) |
|  | rolling | 函数调用，二元运算符 | 计算APPL相对于市场(SPY)的beta值 |
|  | withNullFill | 二元运算符 | 使用特定值替换Null值参与计算 |
| :H | byRow | 函数调用 | 将函数应用到二维的数据对象（矩阵/表/元组/数组向量/列式元组）的每一行进行计算。 |
| :V | byColumn | 函数调用 | 将函数应用到二维的数据对象（矩阵/表/元组/数组向量/列式元组）的每一列进行计算。 |
|  | talib | 函数调用 | 使 DolphinDB 函数与 Python TA-lib 库中的函数行为保持一致 |
|  | tmoving | 函数调用 | 将一个函数应用到一个时间类型的窗口上，窗口右边界固定 |
|  | twindow | 函数调用 | 应用同 tmoving，但 twindow 函数的左右边界均可自由设定 |

上表中的符号可以迭代使用，按从左到右顺序执行符号对应的分解操作，将分解后的数据块应用于函数或操作符，最后将各子任务的结果组合为一个对象并返回。 比如 X
<operator> :E:L Y，先对 X 和 Y 执行 :E 对应的分解（拆解为 X(i), Y(i)），再执行 :L 对应的分解操作后作用于操作符，
即对每一个 X(i) 执行了 X(i) <operator>:L Y(i)，最后组合各个子任务的结果并输出。具体例子如下：

```
a=1 2 3
b=4 5 6
c=(a,b)
re=c +:E:L c
print(re)
```

输出返回：

```
(1 2 3
- - -
2 3 4
3 4 5
4 5 6
,4  5  6
-- -- --
8  9  10
9  10 11
10 11 12
)
```

## 分解和组装规则

通常来说，一个向量被分解成多个标量，一个元组被拆分出各个元素（各元素的形式不同），一个矩阵被分解成多列（向量），一个表或字典被分解成多行（字典）。

在组装阶段，用户可指定如何将子任务的输出合并为最终结果。默认的 DolphinDB
规则下，根据所有子任务的结果来决定最终输出形式。其中，标量类型合并组成一个向量，向量合并成一个矩阵，字典合并成一张表，多个矩阵合并为一个元组，否则统一合并成一个元组。此外，还提供了三种组装规则：用户可选择总是输出一个元组（Tuple
规则）；默认所有子结果的数据类型和形式都与第一个子结果相同，直接根据第一个子任务的结果来选择最终结果的数据类型和形式；（Consistent
规则），或但凡有一个子任务的结果是向量，则最终结果输出一个元组（kdb+ 规则）。以函数模式 `:E`（详见 each）做简单示例：

```
vec = 1..9
tp = (vec, vec, vec)
typestr copy:EC(tp) // FAST INT MATRIX
typestr copy:ED(tp) //FAST INT MATRIX
typestr copy:EU(tp) //ANY VECTOR
typestr copy:EK(tp) //ANY VECTOR
```

上例中，`:E` 的子任务均返回长度、类型一致的向量。D（DolphinDB）和
C（Consistent）规则将子任务返回的结果组装成矩阵，U（Tuple）规则在任何时候都返回一个元组。而由于子任务中存在向量，K（kdb+）规则下最终结果也是一个元组。

高阶函数按元素遍历向量/元组，按列遍历矩阵，按行遍历表或字典。
