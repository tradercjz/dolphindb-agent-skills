# triggerCheckpointForIMOLTP

## 语法

`triggerCheckpointForIMOLTP([force=false], [sync=false])`

## 详情

用于手动向处于正常运行状态的 OLTP 发出创建检查点（checkpoint）的请求。

## 参数

* **force**：布尔类型的可选参数，默认为 false。用于设定是否强制执行 checkpoint。设定为 true 后，OLTP
  将在接收到该函数发出的指令后强制执行 checkpoint。
* **sync**：布尔类型的可选参数，默认为 false。用于设定是否异步执行强制的 checkpoint。

  + 设置为 false 时，该函数请求一次异步的 checkpoint，并不会等到请求完成再返回执行结果；
  + 设置为 true时，该函数会等到请求受理后再返回执行结果。注意：此时的执行结果并不一定意味着 checkpoint
    文件的创建完成。

注：

该函数的两个可选参数均设定为 true 后，手动创建 checkpoint 文件成功的前提是配置项
*enableIMOLTPEngine* 和 *enableIMOLTPCheckpoint* 均已启用且 OLTP
处于正常运行状态。

## 返回值

无。
