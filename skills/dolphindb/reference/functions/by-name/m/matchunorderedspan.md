# matchUnorderedSpan

## 语法

`matchUnorderedSpan(textCol, span, slop, [scoreColName])`

## 详情

该函数用于 SQL 语句的 WHERE 子句，针对 PKEY 存储引擎中设置文本索引的列进行文本匹配，返回包含指定短语的行。不同于 matchSpan
的是，该函数在匹配时将忽略短语中单词的顺序。

## 参数

**textCol** 待查询的列，即 PKEY 存储引擎中设置了文本索引的列。

**span** STRING 类型标量，用于指定待查询的短语。

**slop** 非负整数，表示用户输入的词距。匹配时，若短语前、后或短语中有不多于 *slop* 个其他词语，仍视作匹配成功。

**scoreColName** 可选参数，STRING
类型标量，表示输出结果中文本匹配得分列的列名。默认值为空，此时不输出得分列。匹配得分代表数据在分区内的匹配程度，不同分区的分数不可比较。

## 返回值

返回一个布尔值。

## 例子

```
// 构造数据
stringColumn = ["There are some apples and oranges.","Mike likes apples.","Alice likes oranges.","Mike gives Alice an apple.","Alice gives Mike an orange.","John likes peaches, so he does not give them to anyone.","Mike, can you give me some apples?","Alice, can you give me some oranges?","Mike traded an orange for an apple with Alice."]
t = table([1,1,1,2,2,2,3,3,3] as id1, [1,2,3,1,2,3,1,2,3] as id2, stringColumn as remark)
if(existsDatabase("dfs://textDB")) dropDatabase("dfs://textDB")
db = database(directory="dfs://textDB", partitionType=VALUE, partitionScheme=[1,2,3], engine="PKEY")
pt = createPartitionedTable(dbHandle=db, table=t, tableName="pt", partitionColumns="id1",primaryKey=`id1`id2,indexes={"remark":"textindex(parser=english, full=false, lowercase=true, stem=true)"})
pt.tableInsert(t)

// 匹配包含短语 mike apple 的行，忽略 mike 和 apple 的顺序，且允许短语前后或内部有小于等于2个其他词汇
select * from pt where matchUnorderedSpan(remark, "apple mike", 2)
```

| id1 | id2 | remark |
| --- | --- | --- |
| 1 | 2 | Mike likes apples. |
| 2 | 1 | Mike gives Alice an apple. |
| 3 | 3 | Mike traded an orange for an apple with Alice. |
