<!-- Auto-mirrored from upstream `documentation-main/progr/statements/transaction.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# transaction

## 语法

```
transaction{

<statement block>;

}
```

## 详情

transaction 将对单个内存表（mvccTable、共享内存表和
OLTP 表）操作的多个 SQL 语句封装为一个事务，以保证语句块的原子性、一致性和隔离性，即若 transaction
执行过程中某条语句报错，则回滚所有语句。

注：

* 目前 transaction 仅支持封装除 create、alter 以外的 SQL 语句。
* `statement block` 下方支持添加 `commit` 或
  `rollback`。`commit`
  （可以省略）表示提交本次事务的所有更改，`rollback` 表示撤销本次事务的所有更改。

## 例子

例1：封装针对共享内存表的 SQL 语句。

```
sym = `C`MS`MS`MS`IBM`IBM`C`C`C$SYMBOL
price= 49.6 29.46 29.52 30.02 174.97 175.23 50.76 50.32 51.29
qty = 2200 1900 2100 3200 6800 5400 1300 2500 8800
timestamp = [09:34:07,09:36:42,09:36:51,09:36:59,09:32:47,09:35:26,09:34:16,09:34:26,09:38:12]
t = table(timestamp, sym, qty, price);

share t as pub

def update_date(){

  update pub set qty=qty-50 where sym=`C

  update pub set price=price-0.5 where sym=`MS

  select ts from pub // ts 列并不存在
}
transaction {
  update_date() // 报错：select ts from pub => Unrecognized column name [ts]
}

// 由于 select ts from pub 语句执行失败，所有语句回滚，内存表中的 qty 和 price 未被更改
eqObj(pub[`qty], qty)
// 输出：true，表示 qty 未被更改

eqObj(pub[`price], price)
// 输出：true，表示 price 未被更改
```

例2：封装针对 OLTP 表的 SQL 语句。

创建 OLTP 数据库和表。

注：

需要在配置文件里添加 `enableIMOLTPEngine=true` 开启 OLTP 引擎。

```
dbName = "oltp://test_imoltp"
tableName = "test_table"

if (existsDatabase(dbName)) {
    dropDatabase(dbName)
}

db = database(dbName, VALUE, 1..100, , "IMOLTP")

pt = db.createIMOLTPTable(
    table(1:0, ["id", "val1", "val2", "sym"], [LONG, INT, LONG, STRING]),
    tableName,
    primaryKey=`id
)
```

将三条 insert into 语句封装为一个事务。

```
transaction {
    insert into pt values(0, 0, 0, `aaa)
    insert into pt values(1, 1, 1, `bbb)
    insert into pt values(2, 2, 2, `ccc)
}
select id from pt order by id
```

语句正常执行，select 语句查询结果如下：

| id |
| --- |
| 0 |
| 1 |
| 2 |

添加 `rollback` 回滚事务。

```
transaction {
    insert into pt values(3, 3, 3, `ddd)
    insert into pt values(4, 4, 4, `eee)
    delete from pt where id = 1
    update pt set id = 10 where id = 0

    assert (exec id from pt order by id) == [2,3,4,10] // 此时事务生效，pt 表被更改
    rollback // 回滚事务，撤销所有更改
}
select id from pt order by id
```

最终事务中的所有更改被撤销，select 语句查询结果不变：

| id |
| --- |
| 0 |
| 1 |
| 2 |
