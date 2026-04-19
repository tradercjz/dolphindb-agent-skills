# getSubscriptionTopic

## 语法

`getSubscriptionTopic(tableName, [actionName])`

## 详情

查询订阅主题的名称和流数据表的列名。

订阅主题名称是流数据表所在节点的局域网信息（包括内网 IP
地址、端口号和节点别名）、流数据表的名称和订阅任务名称（如果指定了actionName）的组合，它们之间使用"/"分隔。例如，如果服务器的局域网信息为是
"localhost:8848:nodeA"，流数据表的名称是 "trades"，那么主题名称是
"localhost:8848:nodeA/trades"；如果订阅任务名称是 "vwap"，那么主题名称是
"localhost:8848:nodeA/trades/vwap"。

## 参数

**tableName** 是一个字符串，表示共享的流数据表的名称。

**actionName** 是一个字符串，表示订阅任务的名称。它可以包含字母，数字和下划线。

## 返回值

返回具有两个元素的元组：分别是订阅主题的名称和流数据表的列名。

## 例子

在别名为 rh8502 的节点上执行以下脚本，该节点的内网 IP 为192.168.1.135，端口号为8502：

```
t=streamTable(1000000:0,`date`time`sym`qty`price`exch,[DATE,TIME,SYMBOL,INT,DOUBLE,SYMBOL])
share t as trades
trades_1=streamTable(1000000:0,`date`time`sym`qty`price`exch,[DATE,TIME,SYMBOL,INT,DOUBLE,SYMBOL])
subscribeTable(tableName=`trades, actionName=`vwap, offset=-1, handler=append!{trades_1})
getSubscriptionTopic(`trades,`vwap);

// output
("192.168.1.135:8502/rh8502/trades/vwap",["date","time","sym","qty","price","exch"])
```
