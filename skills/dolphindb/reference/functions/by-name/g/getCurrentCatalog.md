# getCurrentCatalog

## 语法

`getCurrentCatalog()`

## 详情

查看当前 session 位于哪个 catalog 中。返回一个字符串。

## 参数

无

## 返回值

一个字符串。

## 例子

```
select * from cat1.db1.table1 // 成功
select * from db1.table1 // 报错

use CATALOG cat1;

select * from db1.table1 // 成功
getCurrentCatalog() // Output:"cat1"
```
