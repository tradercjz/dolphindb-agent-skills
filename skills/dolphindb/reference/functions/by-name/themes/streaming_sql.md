# 流式 SQL

流式 SQL 支持基于共享内存表进行实时 SQL 查询和持续结果更新。用户可以声明表为流式 SQL 输入表，注册流式 SQL
查询，订阅实时结果，并管理查询的生命周期。该功能适合对实时行情、监控指标等数据进行低延迟分析。相关函数如下所示：

| 函数名 | 函数介绍 |
| --- | --- |
| declareStreamingSQLTable | 声明指定表为流式 SQL 输入表，只有被声明的表才能注册流式 SQL 查询。声明不会影响该表在普通 SQL 中的使用。 |
| getStreamingSQLStatus | 查询流式 SQL 查询状态，支持查询单条或所有查询。管理员可查看所有用户查询。 |
| listStreamingSQLTables | 列举当前用户声明的所有流式 SQL 表，管理员可查看所有用户声明。返回表包含表名、共享状态及声明用户列表。 |
| registerStreamingSQL | 注册流式 SQL 查询，返回查询 ID，并自动生成结果变更日志流表。支持 SELECT、WHERE、JOIN（仅支持等值连接，且仅支持 ej、lj、rj、fj 类型）、ORDER BY 等关键字。 |
| revokeStreamingSQL | 注销已注册的流式 SQL 查询。 |
| revokeStreamingSQLTable | 注销之前声明的流式 SQL 表。注销前须先取消该表上的所有流式 SQL 查询订阅。只能注销当前用户声明的表。注销仅移除流式 SQL 功能，不删除表或数据。 |
| subscribeStreamingSQL | 订阅指定流式 SQL 查询结果，订阅端执行查询并维护实时更新的共享结果表。 |
| unsubscribeStreamingSQL | 取消订阅指定流式 SQL 查询结果，订阅端停止更新结果表。 |
