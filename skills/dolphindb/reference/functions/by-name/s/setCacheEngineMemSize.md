# setCacheEngineMemSize

## 语法

`setCacheEngineMemSize(memSize)`

## 详情

在线修改 Cache Engine 的容量。集群环境下，该命令只能由管理员在数据节点/计算节点上执行。执行前需要确保开启了
Cache Engine (配置参数 *chunkCacheEngineMemSize*)。仅 OLAP 引擎支持该命令。

注：

此命令修改的配置值在集群重启后将失效。若需要配置值永久生效，请更改配置文件中的
*chunkCacheEngineMemSize* 。

## 参数

**memSize** 一个数值型标量，且必须大于0且小于 *maxMemSize* \* 0.5。

## 场景

Cache Engine 开启后，写入数据时，系统会先把数据写入缓存，当缓存中的数据量达到 *chunkCacheEngineMemSize*
的30%时，才会写入磁盘。若该配置项设置过小，大批量数据写入时，Cache Engine 可能很快被占满，从而导致写入卡住。此时，通过该命令在线修改 Cache
Engine 的容量，来保证写入继续进行。

## 相关函数

可以使用 getCacheEngineMemSize 获取 Cache Engine 的实时状态，确认 Cache Engine
是否在线修改成功。
