# setMaxTransactionSize

## 语法

`setMaxTransactionSize(engine, maxSizeGB)`

## 详情

在线修改当前数据/计算节点的单次写入事务上限（以 GB 为单位），注意不可超过对应 cache engine 大小。该命令只能由管理员执行。关于 DolphinDB
内存管理相关配置参数及策略，参见功能配置-内存。

**注：**

* 若 OLAP 引擎未开启 Cache Engine，该函数对 OLAP 的事务写入无限制。
* 若当前节点被在线修改了 Cache Engine 容量（setOLAPCacheEngineSize/setTSDBCacheEngineSize），则该函数不可设置超过当前 Cache Engine 容量。
* 此命令修改的配置值在系统重启后将失效。若需要永久限制写入事务的上限，请通过配置文件中的 *maxTransactionRatio* 调整事务大小占
  Cache Engine 的最大比例。

## 参数

**engine** 字符串标量，表示对应的存储引擎，可选值为 “TSDB” 或 “OLAP”。

**maxSizeGB** 数值型标量，表示写入事务的大小上限，单位为 GB。
