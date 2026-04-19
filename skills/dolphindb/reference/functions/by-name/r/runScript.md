# runScript

## 语法

`runScript(script)`

## 详情

本地执行一段脚本。该命令必须要用户登录后才能执行。

## 参数

**script** 是字符串，表示需要执行的脚本。

## 例子

```
t = table(1..100 as id,201..300 as val1)
script1 = 'dn = "dfs://test";if(existsDatabase(dn)){dropDatabase(dn)};db = database(dn,VALUE,1..10);pt = db.createPartitionedTable(t,`pt,`id).append!(t)'
script2 = 'select * from loadTable("dfs://test",`pt)'
runScript(script1)
runScript(script2)
```
