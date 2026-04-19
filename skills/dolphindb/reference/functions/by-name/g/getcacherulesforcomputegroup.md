# getCacheRulesForComputeGroup

首发版本：3.00.5

## 语法

`getCacheRulesForComputeGroup([name])`

## 详情

返回全部或指定计算组中的缓存规则。

## 参数

**name** 可选参数，字符串标量，指定计算组的名称；不指定则返回全部计算组中的缓存规则。

## 返回值

一张表，包含以下字段：

* **computeGroup**：计算组的名称。
* **tableName**：需要在计算组缓存路径中进行缓存的表。

## 例子

```
getCacheRulesForComputeGroup("cgroup1")
```

| computeGroup | tableName |
| --- | --- |
| cgroup1 | dfs://compute\_test/tb1 |

**相关函数：**removeCacheRulesForComputeGroup、addCacheRulesForComputeGroup
