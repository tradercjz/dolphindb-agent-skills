# CEP 相关函数

复杂事件处理引擎用于从大规模实时数据流中提取信息、识别模式并进行实时分析和决策。本文提供 CEP
引擎相关函数的概览，包括核心函数、事件注册、流表操作及策略管理，方便快速查阅和使用。

| **分类** | **函数名** | **函数简介** |
| --- | --- | --- |
| 引擎 | createCEPEngine | 创建 CEP 引擎。 |
| stopSubEngine | 停止子引擎。 |
| dropStreamEngine | 释放指定的 CEP 引擎。 |
| 事件 | appendEvent | 向 CEP 引擎写入事件。 |
| appendEventWithResponse | 发送事件并阻塞等待特定响应事件返回。 |
| sendEvent | 将事件插入到当前子引擎的事件处理队列的尾部。 |
| routeEvent | 将事件插入到当前子引擎的事件处理队列的队首。 |
| emitEvent | 将事件插入到 CEP 引擎的事件输出队列的队尾。引擎会异步地将事件发送到输出队列。 |
| monitor | spawnMonitor | 创建一个 monitor 实例。 |
| getCEPEngineMonitor | 获取指定 CEP 引擎中指定或所有一级（非 spawn）monitor 实例。 |
| getCEPEngineSubMonitor | 获取指定 monitor 在指定 CEP 引擎中生成的 subMonitor。 |
| destroyMonitor | 终止 monitor 实例。 |
| listenser | addEventListener | 指定事件匹配规则和回调函数，返回一个 EventListener 实例。 |
| getEventListener | 查询当前 monitor 中已注册的事件监听器实例。 |
| terminate | 终止该 EventListener 实例，不再触发回调。 |
| 事件流序列化 | streamEventSerializer | 将事件序列化为 BLOB 格式，写入到异构流表。 |
| 监控运维 | getStreamEngineStat().CEPEngine | 查看当前所有 CEP 引擎的状态。 |
| getCEPEngineStat | 查看指定 CEP 引擎当前的运行状态，包括 CEP 引擎及其子引擎的状态。 |
| 数据视图 | createDataViewEngine | 创建一个 DataView 引擎。 |
| getDataViewEngine | 获取在 CEP 引擎内部创建的指定 DataView 引擎的数据。 |
| getStreamEngine | 获取在 CEP 引擎外部创建的指定 DataView 引擎的数据。 |
| updateDataViewItems | 更新 DataView 引擎中指定键值对应的指定字段的值。 |
| deleteDataViewItems | 删除 DataView 引擎中指定键值的数据。 |
| dropDataViewEngine | 删除当前 CEP 引擎中指定的 DataView 引擎。 |
