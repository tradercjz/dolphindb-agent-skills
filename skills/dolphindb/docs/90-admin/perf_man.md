<!-- Auto-mirrored from upstream `documentation-main/sys_man/perf_man.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 运维监控

DolphinDB 提供以下三种运维监控方式，以下依照推荐度排序：

1. 通过第三方系统的 API，如 Prometheus 和 Grafana 的组合。有关详细的使用步骤，参考：集群运维监控。
2. 使用内置函数。可以使用以下函数来进行性能监控。以下函数都返回多个性能监控的度量值：

   * getPerf：返回本地节点的性能监控度量值。可以在集群中的每个节点执行。
   * getClusterPerf：返回集群中所有节点的性能监控度量值。只能在控制器上执行。
   * getJobStat ：监控正在执行或者在作业队列中的作业和任务数量。
3. Web 界面。以下是部分显示在 Web 界面的性能监控度量值：

   * memUsed： 节点使用的内存
   * memAlloc： 节点中DolphinDB当前内存池的容量
   * medLast10QueryTime： 前10个完成的查询执行所耗费时间的中间值
   * maxLast10QueryTime： 前10个完成的查询执行所耗费时间的最大值
   * medLast100QueryTime： 前100个完成的查询执行所耗费时间的中间值
   * maxLast100QueryTime： 前100个完成的查询执行所耗费时间的最大值
   * maxRunningQueryTime： 当前正在执行的查询的耗费时间的最大值。

注：

* 如果节点是单独启动的，性能监控的默认设置是 false。如果需要启动性能监控，我们可以在配置文件
  dolphindb.cfg 中设置 perfMonitoring=true。
* 如果集群在 Web
  界面启动，性能监控的默认设置是true。如果需要停止控制器启动的所有节点上的性能监控，我们可以在控制器节点的配置文件 dolphindb.cfg 中设置
  perfMonitoring=false。

工作日志文件包含了每个节点执行查询的描述性信息。工作日志文件的默认文件夹是 log 文件夹，默认名称是
nodeAlias\_job.log。可以在配置文件中修改 *jobLog* 参数来修改路径和名称。
