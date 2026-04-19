# cancelRecoveryTask

## 语法

`cancelRecoveryTask(taskId)`

## 详情

取消已经提交但尚未开始执行的副本恢复任务。该命令只能由管理员在控制节点上执行。

## 参数

**taskId** 是一个字符串标量或向量，表示副本恢复任务的 ID，可以通过 getRecoveryTaskStatus 获得。

## 返回值

无。
