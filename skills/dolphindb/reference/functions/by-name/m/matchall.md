# matchAll

## 语法

`matchAll(textCol, terms, [scoreColName])`

## 详情

该函数结合 SQL 语句的 WHERE 子句，针对 PKEY 存储引擎中设置文本索引的列进行文本匹配，返回符合所有指定匹配词的行。

## 参数

**textCol** 待查询的列，即 PKEY 存储引擎中设置了文本索引的列。

**terms** STRING 类型标量，用于指定待查询的词。若需查询多个词，可将它们用空格分隔写入该字符串中。

**scoreColName** 可选参数，STRING
类型标量，表示输出结果中文本匹配得分列的列名。默认值为空，此时不输出得分列。匹配得分代表数据在分区内的匹配程度，不同分区的分数不可比较。

## 返回值

返回一个布尔值，表示该列是否匹配所有指定词。

## 例子

```
// 构造数据
stringColumn = ["There are some apples and oranges.","Mike likes apples.","Alice likes oranges.","Mike gives Alice an apple.","Alice gives Mike an orange.","John likes peaches, so he does not give them to anyone.","Mike, can you give me some apples?","Alice, can you give me some oranges?","Mike traded an orange for an apple with Alice."]
t = table([1,1,1,2,2,2,3,3,3] as id1, [1,2,3,1,2,3,1,2,3] as id2, stringColumn as remark)
if(existsDatabase("dfs://textDB")) dropDatabase("dfs://textDB")
db = database(directory="dfs://textDB", partitionType=VALUE, partitionScheme=[1,2,3], engine="PKEY")
pt = createPartitionedTable(dbHandle=db, table=t, tableName="pt", partitionColumns="id1",primaryKey=`id1`id2,indexes={"remark":"textindex(parser=english, full=false, lowercase=true, stem=true)"})
pt.tableInsert(t)

// 匹配包含 apple 和 orange 的行
select * from pt where matchAll(textCol=remark,terms="apple orange")
```

| id1 | id2 | remark |
| --- | --- | --- |
| 1 | 1 | There are some apples and oranges. |
| 3 | 3 | Mike traded an orange for an apple with Alice. |
