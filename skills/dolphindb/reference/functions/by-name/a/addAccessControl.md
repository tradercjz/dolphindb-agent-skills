# addAccessControl

## 语法

`addAccessControl(table)`

## 详情

限制其他用户访问当前用户创建的共享表或者流数据引擎。添加访问限制后，其他用户只有被管理员赋予访问权限后，才可访问当前用户创建的共享表或者流数据引擎。

注：

1. 只能由管理员或者创建共享表/流数据引擎的用户执行该函数。
2. 如果管理员已经为其他用户 grant/deny/revoke 共享表/流数据引擎的权限，其他未经授权的用户无法再访问共享表/流数据引擎，无需调用
   `addAccessControl` 添加访问限制。

## 参数

**table** 共享表或者流数据引擎对象。

## 例子

创建一组用户，进行权限管理。

```
login(`admin, `123456)
createUser(`u1, "111111");
createUser(`u2, "222222");
createUser(`u3, "333333");
```

例1：限制其他用户访问流数据引擎

1. 用户 u1 创建流数据引擎
   agg1。

   ```
   login(`u1, "111111")
   share streamTable(1000:0, `time`sym`volume, [TIMESTAMP, SYMBOL, INT]) as trades
   output1 = table(10000:0, `time`sym`sumVolume, [TIMESTAMP, SYMBOL, INT])
   agg1 = createTimeSeriesEngine(name="agg1", windowSize=60000, step=60000, metrics=<[sum(volume)]>, dummyTable=trades, outputTable=output1, timeColumn=`time, useSystemTime=false, keyColumn=`sym, garbageSize=50, useWindowStartTime=false)
   subscribeTable(tableName="trades", actionName="agg1", offset=0, handler=append!{agg1}, msgAsTable=true);
   ```
2. 给引擎 agg1
   添加访问限制。

   ```
   addAccessControl(agg1)
   ```
3. 用户 u2 注入数据到引擎 agg1 或删除引擎 agg1
   时报错。

   ```
   // 以用户 u2 的身份登录服务器
   login(`u2, "222222")

   // 注入数据
   insert into trades values(2018.10.08T01:01:01.785,`A,10) // OK!
   insert into agg1 values(2018.10.08T01:01:01.785,`A,10) // ERROR: No access to table [agg1]

   // 注销引擎
   dropStreamEngine("agg1") // No access to drop stream engine agg1
   ```
4. 给用户 u2 赋予引擎 agg1
   的写入权限。

   ```
   login(`admin, `123456)
   grant("u2", TABLE_WRITE, "agg1")
   ```

   如果在集群中，权限对象必须为
   "nodeAlias:tableName"，例如引擎 agg1 在节点 dnode1
   中。

   ```
   grant("u2", TABLE_WRITE, "dnode1:agg1")
   ```
5. 此时用户 u2 可以成功注入数据到引擎
   agg1。

   ```
   insert into agg1 values(2018.10.08T01:01:01.785,`A,10)
   ```

例2：限制其他用户访问流数据引擎

```
login(`u1, "111111")
t = table(take(`a`b`c`, 10) as sym, 1..10 as val)
share t as st;
addAccessControl(`st)

login(`u3, "333333")
select * from st # ERROR: No access to shared table [st]
insert into st values(`a, 4) // ERROR: No access to shared table [st]
```

**相关函数**：grant、deny、revoke
