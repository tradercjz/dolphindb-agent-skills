# haStreamTable

## 语法

`haStreamTable(raftGroup, table, tableName, cacheSize, [keyColumn],
[retentionMinutes=1440], [preCache])`

## 详情

创建高可用流数据表。该函数只能在启用流数据高可用后使用。要启用流数据高可用，用户需要在集群配置文件 cluster.cfg
中指定配置参数 *streamingHAMode* 和 *streamingRaftGroups*。系统启动时，配置参数
*streamingRaftGroup* 指定的数据节点/计算节点组成 Raft 组，一个数据节点/计算节点作为
Leader，其他数据节点/计算节点作为 Follower。Raft 组的每个数据节点/计算节点上都有流数据表的副本。

客户端只需订阅 Raft 组中任意一个数据节点/计算节点上的高可用流数据表，并启用订阅的自动重连功能，即把
*reconnect* 参数设置为 true。Leader 上的高可用流数据表会向客户端发布数据。如果 Raft 组中的 Leader
宕机，系统会选举出新的 Leader 继续发布数据，客户端会自动切换订阅到新的 Leader 上的高可用流数据表。

一个 Raft 组可以包含多个高可用流数据表。

## 参数

**raftGroup** 是一个大于1的整数，用于指定 Raft 组的 ID。

**table** 是一个表对象。它必须是一个由 `table` 函数创建的空表。

**tableName** 是一个字符串，用于指定高可用流数据表的名称。

**cacheSize** 是一个正整数，用于指定高可用流数据表在内存中最多保留多少行。如果 *cacheSize*
是小于1000的正整数，它会被自动调整为1000。

**keyColumn** 可选参数，字符串标量或向量，用于指定主键。设置该参数后，将创建高可用的键值流数据表，其主键不允许包含重复值。

**retentionMinutes** 可选参数，整数，用于指定保留大小超过 1GB 的 log
文件的时间（从文件的最后修改时间开始计算），单位是分钟。默认值是1440，即一天。

**preCache** 可选参数，正整数，用于指定服务重启后从磁盘加载高可用流表到内存的记录条数。默认值同 *cacheSize* 的配置值。

## 返回值

一张表。

## 例子

假设配置参数 *streamingRaftGroup*=11:NODE1:NODE2:NODE3，在 Raft
组的任意一个节点如 NODE1 上执行以下脚本创建高可用流数据表 trades：

```
colNames = `timestamp`sym`qty`price
colTypes = [TIMESTAMP,SYMBOL,INT,DOUBLE]
t=table(1:0,colNames,colTypes)
haStreamTable(11,t,`trades,100000);
```

在集群的另外一个节点 NODE4 上执行以下脚本订阅表 trades，把订阅的数据保存至分布式数据库中。

```
if(existsDatabase("dfs://stock")){
   dropDatabase("dfs://stock")
}
db=database(directory="dfs://stock",partitionType=VALUE,partitionScheme=2018.08.01..2019.12.30)
t=table(1:0,`timestamp`sym`qty`price,[TIMESTAMP,SYMBOL,INT,DOUBLE])
trades_slave=db.createPartitionedTable(table=t,tableName=`trades_slave,partitionColumns=`timestamp);
subscribeTable(server=NODE2,tableName=`trades,actionName=`sub_trades,offset=-1,handler=append!{trades_slave},msgAsTable=true,batchSize=1000,throttle=1,hash=-1,reconnect=true);

// 这里subscribeTable函数的第一个参数可以是NODE1,NODE2,NODE3中的任意一个，reconnect参数必须为true。
```

在 NODE4 上执行以下脚本取消订阅：

```
unsubscribeTable(server=NODE2,tableName=`trades,actionName=`sub_trades);
// 这里unsubscribeTable函数的第一个参数可以是 NODE1, NODE2, NODE3 中的任意一个。
```

相关函数：keyedStreamTable, dropStreamTable, getStreamingLeader, getStreamingRaftGroups
