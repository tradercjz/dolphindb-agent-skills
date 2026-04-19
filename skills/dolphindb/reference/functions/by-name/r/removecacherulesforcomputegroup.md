# removeCacheRulesForComputeGroup

首发版本：3.00.5

## 语法

`removeCacheRulesForComputeGroup(name, tableNames)`

## 详情

移除计算组的缓存规则，指定需要取消计算组缓存的表。

## 参数

**name** 字符串标量，指定需要移除缓存规则的计算组。

**tableNames**
字符串标量或向量，指定需要取消计算组缓存的表，以库名/表名的形式拼接，例如"dfs://compute\_test/tb1"。暂不支持通配符。

## 返回值

无

## 例子

```
removeCacheRulesForComputeGroup("cgroup1", "dfs://compute_test/tb1")

removeCacheRulesForComputeGroup("cgroup1", ["dfs://compute_test/tb1", "dfs://compute_test/tb2"])
```

**相关函数：**addCacheRulesForComputeGroup、getCacheRulesForComputeGroup
