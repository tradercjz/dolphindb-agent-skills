# matchFuzzy

首发版本：3.00.4

## 语法

```
matchFuzzy(textCol, term, minimumSimilarity, prefixLength, [scoreColName])
```

## 详情

该函数用于 SQL 语句的 WHERE 子句，针对 PKEY
存储引擎中设置文本索引的列进行文本模糊匹配，以便在用户输入存在拼写错误或不完全匹配的情况下，依然能够返回相关度较高的查询结果。

注：

* 当 *minimumSimilarity* 设置为 1 时，意味着单词完全匹配，相当于
  `matchAny` 函数。
* 仅支持对单个单词的查询，若 *term* 中包含多个单词，则查询结果为空。
* 当 *prefixLength* 大于 *term* 的长度时，将自动调整为 *term* 的长度。

## 参数

**textCol**待查询的列，即 PKEY 存储引擎中设置了文本索引的列。

**term** STRING 类型标量，用于指定待查询的词。仅支持单个单词查询。

**minimumSimilarity**DOUBLE 类型标量，表示匹配结果需要的最小近似度，取值范围为 [0,1]。

**prefixLength** 非负整数，表示匹配结果需与 *term* 具有相同的前缀的长度。

**scoreColName**: 可选参数，STRING
类型标量，表示输出结果中文本匹配得分列的列名。默认值为空，此时不输出得分列。匹配得分代表数据在分区内的匹配程度，不同分区的分数不可比较。

## 例子

```
// 构造数据
stringColumn = ["There are some apples and oranges.","Mike likes apples.","Alice likes oranges.","Mike gives Alice an apple.","Alice gives Mike an orange.","John likes peaches, so he does not give them to anyone.","Mike, can you give me some apples?","Alice, can you give me some oranges?","Alice made apple pie."]
t = table([1,1,1,2,2,2,3,3,3] as id1, [1,2,3,1,2,3,1,2,3] as id2, stringColumn as remark)
if(existsDatabase("dfs://textDB")) dropDatabase("dfs://textDB")
db = database(directory="dfs://textDB", partitionType=VALUE, partitionScheme=[1,2,3], engine="PKEY")
pt = createPartitionedTable(dbHandle=db, table=t, tableName="pt", partitionColumns="id1",primaryKey=`id1`id2,indexes={"remark":"textindex(parser=english, full=false, lowercase=true, stem=true)"})
pt.tableInsert(t)

// 模糊匹配 make，前缀必须为m
select * from pt where matchFuzzy(textCol=remark,term="make",minimumSimilarity=0.6,prefixLength=1)
```

| id1 | id2 | remark |
| --- | --- | --- |
| 1 | 2 | Mike likes apples. |
| 2 | 1 | Mike gives Alice an apple. |
| 2 | 2 | Alice gives Mike an orange. |
| 3 | 1 | Mike, can you give me some apples? |
| 3 | 3 | Alice made apple pie. |

```
// 模糊匹配 make，前缀必须为 ma，将得分列输出为 score
select * from pt where matchFuzzy(textCol=remark,term="make",minimumSimilarity=0.6,prefixLength=2,scoreColName="score")
```

| id1 | id2 | remark | score |
| --- | --- | --- | --- |
| 3 | 3 | Alice made apple pie. | 0.7027325630187988 |
