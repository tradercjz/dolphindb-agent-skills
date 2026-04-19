<!-- Auto-mirrored from upstream `documentation-main/stream/py_sub.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# Python 订阅

以下介绍通过 Python API 订阅流处理结果的交互方式。完整 Python API 可以参考：Python API。

下面为以逐笔成交数据为例介绍订阅流数据结果订阅及写入数据库的流程。

1. DolphinDB 发布端创建一个共享的流数据表 *tglobal*。

   ```
   name = `ChannelNo`ApplSeqNum`MDStreamID`BidApplSeqNum`OfferApplSeqNum`SecurityID`SecurityIDSource`TradePrice`TradeQty`ExecType`TradeTime`LocalTime`SeqNo`DataStatus`TradeMoney`TradeBSFlag`BizIndex`OrderKind`Market
   type = [INT,LONG,SYMBOL,LONG,LONG,SYMBOL,SYMBOL,DOUBLE,INT,SYMBOL,TIMESTAMP,TIME,LONG,INT,DOUBLE,SYMBOL,LONG,SYMBOL,SYMBOL]
   share streamTable(100:0, name, type) as tglobal
   ```
2. Python 订阅端建立 DolphinDB 连接，并开启数据订阅的端口，用于订阅服务器端发送的数据。

   ```
   import numpy as np
   import pandas as pd
   import dolphindb as ddb
   import time
   s = ddb.session()
   s.connect(host="localhost", port=8892, userid="admin", password="123456")
   s.enableStreaming(10020)
   ```
3. Python 订阅端创建表 *tglobal* 的本地订阅，host 和 port 需设置为是发布端节点的 IP 地址和端口号；
   *handler* 设置为自定义的回调函数，用于处理每次流入的数据，*batchSize* 和 *throttle*
   应根据需求合理设置，具体参数含义见：流数据订阅 。

   ```
   listTrade = []
   def handler(lst):
       listTrade.append(lst)
   s.subscribe(host="localhost", port=8892, handler=handler, tableName="tglobal", actionName="action", offset=-1, resub=False, filter=None, msgAsTable=False, batchSize=100000, throttle=60)
   ```
4. 向 DolphinDB 发布端流数据表 *tglobal* 写入模拟数据。

   ```
   for(i in 1..100){
       insertData = [rand(100,1),long(i),string(i),long(i),long(i),string(i),string(i),rand(1.0,1),rand(100,1),string(i),timestamp('2021.01.04T09:30:02.000'),time('09:30:02.000'),long(i),rand(100,1),rand(1.0,1),string(i),long(i),string(i),string(i)]
       insert into tglobal values(insertData)
   }
   ```
5. Python 订阅端查看订阅到的数据。

   ```
   print(listTrade[0][0])

   // output
   [12, 1, '1', 1, 1, '1', '1', 0.053802191046997905, 26, '1', numpy.datetime64('2021-01-04T09:30:02.000'), numpy.datetime64('1970-01-01T09:30:02.000'), 1, 34, 0.4466768535785377, '1', 1, '1', '1']
   ```
6. 当流数据订阅结束时，可以取消订阅并取消对流数据表的定义，取消流数据表定义需在对该表的订阅全部取消后进行。

   ```
   //取消订阅
   unsubscribeTable(tableName="tglobal", actionName="action")
   //取消定义流数据表
   undef(`tglobal, SHARED)
   ```

**相关信息**

* [undef](../funcs/u/undef.html "undef")
* [database](../funcs/d/database.html "database")
* [streamTable](../funcs/s/streamTable.html "streamTable")
* [subscribeTable](../funcs/s/subscribeTable.html "subscribeTable")
* [unsubscribeTable](../funcs/u/unsubscribeTable.html "unsubscribeTable")
