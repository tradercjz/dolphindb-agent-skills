# resetDfsRecoveryConcurrency

## 语法

`resetDfsRecoveryConcurrency(newConcurrecyNum)`

## 详情

在线修改当前节点分区恢复任务的最大并发数。此函数只能由管理员在控制节点调用。

注意：此函数修改的配置值将在系统重启后失效。若需使配置值永久生效，请编辑配置文件中的
dfsRecoveryConcurrency参数。默认情况下，该参数值为集群中控制节点、数据节点和计算节点的节点数之和的两倍。

## 参数

**newConcurrecyNum** 正整数，代表分区恢复任务的并发数上限。

## 例子

```
resetDfsRecoveryConcurrency(2)
```

相关函数：getDfsRecoveryConcurrency
