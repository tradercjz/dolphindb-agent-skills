<!-- Auto-mirrored from upstream `documentation-main/progr/data_forms.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 数据形式

DolphinDB 支持以下数据形式：

| 名称 | ID | 例子 |
| --- | --- | --- |
| 标量 | 0 | 5, 1.3, 2012.11.15, `hello |
| 向量 | 1 | * 常规向量：5 4 8 或 [5, 4, 8] * 元组：(1 2 3, ["I","M","G"], 2.5) * 数组向量：arrayVector * 大数组：bigArray * 列式元组：columnar   tuple |
| 数据对 | 2 | 3:5; 'a':'c'; "Tom":"John"。参考：  * pair |
| 矩阵 | 3 | 1..6$2:3 or reshape(1..6, 2:3)。参考：  * 普通矩阵：matrix * 索引矩阵：setIndexedMatrix! * 索引序列：indexedSeries, setIndexedSeries! |
| 集合 | 4 | set |
| 字典 | 5 | * 有序/无序字典：dict * 有序/无序同步字典：syncDict |
| 表 | 6 | * 内存表：   + 常规表：table   + 索引表：indexedTable   + 键值表：keyedTable   + 流数据表：streamTable,haStreamTable, keyedStreamTable   + 缓存表：cachedTable   + 分区表：createPartitionedTable   + 跨进程共享内存表：createIPCInMemoryTable * 分布式表：   + 分区表：createPartitionedTable   + 维度表：createTable * 多版本并发控制表：mvccTable |
| 张量 | 10 | 通过 tensor 函数，创建张量。例如：  1 维张量：`tensor(1..100)`  2 维张量：`tensor(1..10$5:2)`  3 维张量：`tensor((rand(1.0, 6)$3:2, rand(1.0, 6)$3:2))`  …  n 维张量，其中 n 不能大于10。  注意：   * 目前张量仅支持如下类型：BOOL, CHAR, SHORT, INT, LONG, FLOAT, DOUBLE。 |

可以通过 form 函数来取得一个变量或者常量的数据形式。

```
form false;
// output: 0

form `TEST;
// output: 0

form `t1`t2`t3;
// output: 1

form 1 2 3;
// output: 1

x= 1 2 3
if(form(x) == VECTOR){y=1};
y;
// output: 1

form 1..6$2:3;
// output: 3

form(tensor(1..10$5:2))
// output: 10
```
