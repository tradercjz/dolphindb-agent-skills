# cancelRebalanceTask

## 语法

`cancelRebalanceTask(taskId)`

## 详情

取消已经提交但尚未开始执行的再平衡任务。该命令只能由管理员在控制节点上执行。

## 参数

**taskId** 是一个字符串标量或向量，表示再平衡任务的 ID，可以通过 getRecoveryTaskStatus 获得。

## 返回值

无。
