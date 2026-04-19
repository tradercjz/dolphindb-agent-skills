<!-- Auto-mirrored from upstream `documentation-main/api/python/AdvancedOperations/SubscriptionOptions/SubscriptionOptions.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 填入分区表数据库路径和表名的 list，以获取对应表结构
sd = ddb.streamDeserializer({
    'msg1': ["dfs://test_StreamDeserializer_pair", "pt1"],
    'msg2': ["dfs://test_StreamDeserializer_pair", "pt2"],
}, session=s)
s.subscribe(host="192.168.1.113", port=8848, handler=streamDeserializer_handler, tableName="outTables", actionName="action", offset=0, resub=False,
            msgAsTable=False, streamDeserializer=sd, userName="admin", password="123456")

from threading import Event
Event().wait()
```

输出结果如下所示：

```
Msg2:  [numpy.datetime64('2012-01-01T01:21:24'), numpy.datetime64('2018-12-01T01:21:23.001'), 'a', 18.43745171907358, 'msg2']
Msg1:  [numpy.datetime64('2012-01-01T01:21:24'), numpy.datetime64('2018-12-01T01:21:23.001'), 'a', 65.69160503265448, 41.17562178615481, 'msg1']
Msg2:  [numpy.datetime64('2012-01-01T01:21:25'), numpy.datetime64('2018-12-01T01:21:23.002'), 'b', 93.68146854126826, 'msg2']
Msg1:  [numpy.datetime64('2012-01-01T01:21:25'), numpy.datetime64('2018-12-01T01:21:23.002'), 'b', 22.181119214976206, 38.162505637388676, 'msg1']
Msg2:  [numpy.datetime64('2012-01-01T01:21:26'), numpy.datetime64('2018-12-01T01:21:23.003'), 'c', 51.19852650281973, 'msg2']
Msg1:  [numpy.datetime64('2012-01-01T01:21:26'), numpy.datetime64('2018-12-01T01:21:23.003'), 'c', 16.937458558939397, 36.79589221812785, 'msg1']
Msg2:  [numpy.datetime64('2012-01-01T01:21:27'), numpy.datetime64('2018-12-01T01:21:23.004'), 'a', 0.812068443512544, 'msg2']
Msg1:  [numpy.datetime64('2012-01-01T01:21:27'), numpy.datetime64('2018-12-01T01:21:23.004'), 'a', 34.11729482654482, 29.094212289899588, 'msg1']
Msg2:  [numpy.datetime64('2012-01-01T01:21:28'), numpy.datetime64('2018-12-01T01:21:23.005'), 'b', 93.43341179518029, 'msg2']
Msg1:  [numpy.datetime64('2012-01-01T01:21:28'), numpy.datetime64('2018-12-01T01:21:23.005'), 'b', 9.413380537647754, 32.449754945002496, 'msg1']
Msg2:  [numpy.datetime64('2012-01-01T01:21:29'), numpy.datetime64('2018-12-01T01:21:23.006'), 'c', 65.18307867064141, 'msg2']
Msg1:  [numpy.datetime64('2012-01-01T01:21:29'), numpy.datetime64('2018-12-01T01:21:23.006'), 'c', 83.58133838768117, 54.27990723075345, 'msg1']
```

### 订阅示例 2 （内存表作为输入表）

下例中，在 DolphinDB 中定义了一个由两个内存表构成的异构流数据表，并在 Python 端使用共享内存表的表名构造反序列化器，最后指定 `batchSize=4` 进行批量订阅。可以看出，在总数据条数为 6\*2=12 的情况下，数据首先按总条数分 3 批传入回调函数，在每批数据中，每条数据可能来自不同的输入表。因此，共调用回调函数 3 次，每次输出4条数据构成的一批数据。

#### 构造异构流表

```
try{dropStreamTable(`outTables)}catch(ex){}
// 构造输出流数据表
share streamTable(100:0, `timestampv`sym`blob`price1,[TIMESTAMP,SYMBOL,BLOB,DOUBLE]) as outTables

n = 6;
table1 = table(100:0, `datetimev`timestampv`sym`price1`price2, [DATETIME, TIMESTAMP, SYMBOL, DOUBLE, DOUBLE])
table2 = table(100:0, `datetimev`timestampv`sym`price1, [DATETIME, TIMESTAMP, SYMBOL, DOUBLE])
tableInsert(table1, 2012.01.01T01:21:23 + 1..n, 2018.12.01T01:21:23.000 + 1..n, take(`a`b`c,n), rand(100,n)+rand(1.0, n), rand(100,n)+rand(1.0, n))
tableInsert(table2, 2012.01.01T01:21:23 + 1..n, 2018.12.01T01:21:23.000 + 1..n, take(`a`b`c,n), rand(100,n)+rand(1.0, n))
share table1 as pt1
share table2 as pt2

d = dict(['msg1', 'msg2'], [pt1, pt2])
replay(inputTables=d, outputTables=`outTables, dateColumn=`timestampv, timeColumn=`timestampv)
```

#### 订阅异构流表

```
import dolphindb as ddb

def streamDeserializer_handler(lsts):
    print(lsts)

s = ddb.session()
s.connect("192.168.1.113", 8848, "admin", "123456")
s.enableStreaming()

sd = ddb.streamDeserializer({
    'msg1': "pt1",
    'msg2': "pt2",
}, session=s)
s.subscribe(host="192.168.1.113", port=8848, handler=streamDeserializer_handler, tableName="outTables", actionName="action", offset=0, resub=False, batchSize=4,
            msgAsTable=False, streamDeserializer=sd, userName="admin", password="123456")

from threading import Event
Event().wait()
```

输出结果如下所示：

```
[[numpy.datetime64('2012-01-01T01:21:24'), numpy.datetime64('2018-12-01T01:21:23.001'), 'a', 87.90784921264276, 'msg2'], [numpy.datetime64('2012-01-01T01:21:24'), numpy.datetime64('2018-12-01T01:21:23.001'), 'a', 14.867915444076061, 92.22166634746827, 'msg1'], [numpy.datetime64('2012-01-01T01:21:25'), numpy.datetime64('2018-12-01T01:21:23.002'), 'b', 80.60459423460998, 'msg2'], [numpy.datetime64('2012-01-01T01:21:25'), numpy.datetime64('2018-12-01T01:21:23.002'), 'b', 10.429520844481885, 29.480175042990595, 'msg1']]
[[numpy.datetime64('2012-01-01T01:21:26'), numpy.datetime64('2018-12-01T01:21:23.003'), 'c', 12.45058359648101, 'msg2'], [numpy.datetime64('2012-01-01T01:21:26'), numpy.datetime64('2018-12-01T01:21:23.003'), 'c', 55.05597074679099, 88.84371786634438, 'msg1'], [numpy.datetime64('2012-01-01T01:21:27'), numpy.datetime64('2018-12-01T01:21:23.004'), 'a', 27.357952459948137, 'msg2'], [numpy.datetime64('2012-01-01T01:21:27'), numpy.datetime64('2018-12-01T01:21:23.004'), 'a', 57.705578718334436, 25.98224212951027, 'msg1']]
[[numpy.datetime64('2012-01-01T01:21:28'), numpy.datetime64('2018-12-01T01:21:23.005'), 'b', 63.73548944480717, 'msg2'], [numpy.datetime64('2012-01-01T01:21:28'), numpy.datetime64('2018-12-01T01:21:23.005'), 'b', 65.34572763741016, 0.6374575316440314, 'msg1'], [numpy.datetime64('2012-01-01T01:21:29'), numpy.datetime64('2018-12-01T01:21:23.006'), 'c', 89.62549424753524, 'msg2'], [numpy.datetime64('2012-01-01T01:21:29'), numpy.datetime64('2018-12-01T01:21:23.006'), 'c', 98.75018240674399, 46.55078419903293, 'msg1']]
```
