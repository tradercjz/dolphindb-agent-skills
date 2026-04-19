# SQL

## 关键字

- `alter`
- `any/all`
- `between`
- `case`
- `cgroup by`
- `coalesce`
- `context by`
- `create`
- `delete`
- `distinct`
- `drop`
- `exec`
- `exists`
- `group by`
- `having`
- `[HINT\_EXPLAIN`
- `in`
- `insert into`
- `interval`
- `is null`
- `like/LIKE`
- `limit`
- `map`
- `notBetween/NOTBETWEEN`
- `notIn/NOTIN`
- `notLike/NOTLIKE`
- [`nullIf`](../by-name/n/nullIf.md) — 若 *X* 和 *Y* 都是标量，比较 *X* 和 *Y* 的类型和值是否相同，若相同返回 NULL 值，否则返回 X。
- `order by`
- `over`
- `partition`
- `pivot by`
- `sample`
- `select`
- `SQL Trace`
- `top`
- `union/union all`
- [`unpivot`](../by-name/u/unpivot.md) — 把多列的数据转换成一列。
- `update`
- `where`
- `with`

## 表连接

- `aj`
- `cj`
- `ej`
- `fj`
- `inner join`
- `lj`
- `lsj`
- `pj`
- `pwj`
- `right join`
- `sej`
- `wj`

## 状态查看

- [`getCompletedQueries`](../by-name/g/getCompletedQueries.md) — 查询本地节点上最近完成的 *top* 条查询分布式数据库的 SQL 语句的描述信息。
- [`getQueryStatus`](../by-name/g/getQueryStatus.md) — 获取由当前节点发起且正在执行的查询任务状态。该函数只能在任务发起节点上调用。
- [`getRunningQueries`](../by-name/g/getRunningQueries.md) — 获取本地节点上正在执行的查询任务的描述信息。
- `getTraces`
- `setTraceMode`
- `viewTraceInfo`
