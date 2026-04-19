# appendOrcaStreamTable

首发版本：3.00.3

## 语法

`appendOrcaStreamTable(name, data)`

## 详情

向 orca 流表插入数据。注意：该函数不支持普通流表。

## 参数

**name** 表示流表的名称。字符串标量，可以传入完整的流表全限定名（如
"trading.orca\_table.trades"）；也可以仅提供流表名（如 "trades"），系统会根据当前的 catalog
设置自动补全为对应的全限定名。

**data** 数据表对象

## 例子

向 orca 流表中插入表 snapshot。

```
if (!existsCatalog("test")) {
	createCatalog("test")
}
go;
use catalog test

t = table(1..100 as id, 1..100 as value, take(09:29:00.000..13:00:00.000, 100) as timestamp)
g = createStreamGraph("factor")
baseStream = g.source("snapshot",  schema(t).colDefs.name, schema(t).colDefs.typeString)
  .reactiveStateEngine([<cumsum(value)>, <timestamp>])
  .setEngineName("rse")
  .buffer("end")

g.submit()

appendOrcaStreamTable("snapshot", t)
// 与 appendOrcaStreamTable("test.orca_table.snapshot", t) 等价
```

可通过 SQL 语句 `select * from <catalog>.orca_table.<name>` 查看插入结果，其中
<catalog> 部分可以省略，系统会根据当前的 catalog 自动补全：

```
select * from orca_table.end
```

| cumsum\_value | timestamp |
| --- | --- |
| 1 | 09:29:00.000 |
| 3 | 09:29:00.001 |
| 6 | 09:29:00.002 |
| 10 | 09:29:00.003 |
| 15 | 09:29:00.004 |
| 21 | 09:29:00.005 |
| 28 | 09:29:00.006 |
| 36 | 09:29:00.007 |
| 45 | 09:29:00.008 |
| 55 | 09:29:00.009 |
| … | … |
