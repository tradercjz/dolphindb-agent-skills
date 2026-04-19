# matchedRowCount

首发版本：3.00.5

## 语法

`matchedRowCount()`

## 详情

返回当前 session 中最后一次执行的 INSERT INTO、DELETE、UPDATE 语句所影响的行数。

如果当前 session 中尚未执行过这些语句，则 `matchedRowCount` 返回 0。

`matchedRowCount` 计数规则由语句决定：

* UPDATE：匹配到的行数，而非实际修改的行数。
* DELETE：匹配到的行数，与实际修改的行数一致。
* INSERT INTO：成功插入的行数，不统计更新的行。

## 参数

无

## 返回值

整型标量，表示受影响的行数。

## 例子

```
t=table(`XOM`GS`FB as ticker, 100 80 120 as volume);
INSERT INTO t values(`AMZN`GS, 300 100);
matchedRowCount()
// output: 2

UPDATE t set volume=100 where ticker=`GS
matchedRowCount()
// output: 2

sym=`A`B`C`D`E
id=5 5 3 2 1
val=52 64 25 48 71
t=keyedTable(`sym,sym,id,val)

INSERT INTO t values(`A`K, 6 3, 20 62)
matchedRowCount()
// output: 1

t = table(1..100 as id, rand(100, 100) as value)
DELETE from t where id < 50

matchedRowCount()
// output: 49

dbName="dfs://matchedRowCount"
if(existsDatabase(dbName)){
	dropDatabase(dbName)
}
db = database(dbName, VALUE, 1..10)
t = table(1..10 as id, 1..10 as value)
pt = db.createPartitionedTable(t, `pt, `id)

INSERT INTO t VALUES(11 12 13, 20 30 40)

matchedRowCount()
// output: 3
```
