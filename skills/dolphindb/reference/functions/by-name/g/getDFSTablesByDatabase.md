# getDFSTablesByDatabase

## 语法

`getDFSTablesByDatabase(directory)`

## 详情

返回分布式数据库中的表。

2.00.9 版本起，

* 管理员可以返回当前节点上任一分布式表；
* 其他用户执行时仅返回：

  （1）拥有 DB\_OWNER, DB\_MANAGE, DB\_READ, DB\_WRITE, DB\_INSERT,
  DB\_UPDATE, DB\_DELETE 权限的数据库所对应的分布式表；

  （2）拥有 TABLE\_READ, TABLE\_WRITE,
  TABLE\_INSERT, TABLE\_UPDATE, TABLE\_DELETE 权限的分布式表。

## 参数

**directory** 是分布式数据库所在的目录。

## 返回值

字符串向量。

## 例子

```
getDFSTablesByDatabase("dfs://db")
// output: ["dfs://db/dt", "dfs://db/dt1"]
```
