# isControllerInitialized

## 语法

`isControllerInitialized()`

## 详情

查看控制节点是否启动完成。若启动完成返回 true，否则返回 false。普通集群环境下，仅在控制节点调用；高可用集群环境下，仅在
leader 节点调用。

## 返回值

布尔标量。

## 例子

```
isControllerInitialized()
// output: true
```

相关函数：isDataNodeInitialized
