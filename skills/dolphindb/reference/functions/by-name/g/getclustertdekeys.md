# getClusterTDEKeys

首发版本：3.00.3

## 语法

`getClusterTDEKeys()`

## 详情

获取集群中开启静态加密表的加密信息。仅 Linux 系统支持该功能。

注意：该函数由管理员返回集群中所有的加密表信息。否则，仅返回该用户有访问权限的加密表信息。访问权限包含 DB\_MANAGE, DBOBJ\_CREATE,
DB\_OWNER, TABLE\_READ, TABLE\_WRITE, TABLE\_INSERT, TABLE\_UPDATE, TABLE\_DELETE,
DB\_READ, DB\_WRITE, DB\_INSERT, DB\_UPDATE, DB\_DELETE。

## 参数

无

## 返回值

返回一个表，包含以下列：

* tableName：加密表表名。
* mode：建表时指定的加密方式，全大写。
* version：主密钥版本。

## 例子

```
getClusterTDEKeys()
```

| **tableName** | **mode** | **version** |
| --- | --- | --- |
| dfs://db/table1 | `AES_128_CTR` | 3,698,850,997 |
| dfs://db/table2 | `AES_128_CTR` | 5,768,669,747 |
