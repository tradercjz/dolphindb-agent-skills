# stopSubEngine

## 语法

`stopSubEngine()`

## 详情

要停止特定子引擎内的事件处理操作，可以在其任何 monitor 实例中调用 `stopSubEngine()`。

在关闭子引擎前：

1. 如果存在通过 spawn 产生的 monitor 实例，将首先调用这些由 spawn 产生的 monitor 实例中已声明的
   `onDestroy` 方法。
2. 调用其内部所有 monitor 实例中已声明的 `onunload` 方法。
