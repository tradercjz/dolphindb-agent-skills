# getOrcaStateMachineEventTaskStatus

首发版本：3.00.3

## 语法

`getOrcaStateMachineEventTaskStatus()`

## 详情

StreamMaster 会将接受的请求，作为事件加入状态机队列等待执行。该函数用于获取状态机中任务的状态。

## 返回值

返回一个表，包含以下字段：

* id：事件 id。
* type：事件类型，可能值包括：
  + SUBMIT\_REQUEST：用户的提交流图请求的事件
  + SUBMIT：流图提交事件
  + RESUBMIT\_REQUEST：用户的重新提交流图请求的事件
  + DROP\_REQUEST：用户的删除流图请求的事件
  + DROP\_CALLBACK：系统内部的删除流图回调的事件
  + DROP：流图销毁事件
  + NODE\_DOWN：节点宕机事件
  + NODE\_READY：节点重启事件
  + RECOVER：恢复任务
  + INTERNAL：内部事件
* state：运行状态，包括 pending, running, finished.
* retries：重试次数。当事件没有被正确处理时，状态机会尝试重试。
* scheduledTime：调度时间，表示该事件应该在什么时刻被执行。
* startTime：事件实际开始处理的时间
* endTime：结束时间
* detail：展示事件相关的属性
* errorMessage：事件处理时的异常

## 例子

```
getOrcaStateMachineEventTaskStatus()
```
