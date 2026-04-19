# clearComputeNodeDiskCache

## 语法

`clearComputeNodeDiskCache(database, [table], [partition])`

## 详情

应用于计算组中的计算节点上，尝试清空该节点的磁盘缓存。

## 参数

**database** 字符串，表示数据库名称。

**table** 字符串，表示数据表名。可以包含以下通配符：

* "\*" 表示匹配所有（默认值）
* "?" 表示单个字符
* "%" 表示0，1或多个字符。

**partition** 字符串标量或向量，表示分区的逻辑路径。若不指定，则表示所有分区。

## 返回值

无。

## 例子

清除 database\_compute 数据库的磁盘缓存。

```
clearComputeNodeDiskCache("dfs://database_compute")
```

清除 database\_compute 数据库中以 pt 开头的表的磁盘缓存。

```
clearComputeNodeDiskCache("dfs://database_compute","pt%")
```
