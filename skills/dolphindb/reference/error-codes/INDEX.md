# DolphinDB error-code index

When a DolphinDB runtime error shows `RefId: Sxxxxx`, look up the code below and open the matching file for full 报错信息 / 错误原因 / 解决办法.

Error code format: `S + <category (2 digits)> + <sub-code (3 digits)>`. See `err_codes.md` in this directory for the category legend.

## 00 — 系统 (System)

| Code | Message |
|------|---------|
| [S00001](S00001.md) | The feature of publish is not enabled. RefId: S00001 |
| [S00002](S00002.md) | The openChunks operation failed because the chunk <xxx> is currently locked and in |
| [S00003](S00003.md) | One symbase's size can't exceed 2097152. RefId: S00003 |
| [S00004](S00004.md) | Couldn't create a socket with error code <errno> RefId:S00004 |
| [S00005](S00005.md) | Cannot accept new task <xxx> during a graceful shutdown of the server.RefId: |
| [S00006](S00006.md) | Maximum connections {num} reached. Close unused connections or increase |
| [S00007](S00007.md) | Closing connection with fd=28. Failed to parse the incoming connection with error |
| [S00008](S00008.md) | Couldn't open file [{msg file path}]. {error message}, RefId:S00008 |
| [S00009](S00009.md) | Access denied. You do not have the sufficient permissions to operate on jobs |
| [S00010](S00010.md) | Cannot accept new job submissions. The batch job queue has reached its maximum |
| [S00011](S00011.md) | The message file for job [" + id + "] doesn't exist on disk.RefId: S00011 |
| [S00012](S00012.md) | Failed to add task to remote task queue.RefId: S00012 |
| [S00013](S00013.md) | Failed to create a thread, with exception xx.RefId: S00013 |
| [S00014](S00014.md) | Incompatible server versions. RefId: S00014 |
| [S00015](S00015.md) | "Cannot recognize function: " + xxx. RefId: S00015 |
| [S00016](S00016.md) | "The task queue depth cannot exceed " + xxx. RefId: S00016 |
| [S00017](S00017.md) | The device with ID <xxx> failed to execute write tasks, with error: <xxx>  |
| [S00018](S00018.md) | SSL error: xxx. RefId: S00018 |
| [S00019](S00019.md) | Failed to connect to host <xxx>, with error code: xxx. RefId: S00019 |
| [S00020](S00020.md) | Failed to read message from the socket with IO error type xxx. RefId: 00020 |

## 01 — 存储 (Storage / DFS / TSDB / OLAP)

| Code | Message |
|------|---------|
| [S01000](S01000.md) | TSDBEngine BlockedCacheTable::append: Failed to append to the TSDB cache engine due |
| [S01001](S01001.md) | The column used for value-partitioning cannot contain NULL values. RefId: S01001 |
| [S01002](S01002.md) | Usage: addRangePartitions(dbHandle, newRanges, [level=0], [locations]). The new |
| [S01003](S01003.md) | deleteSubChunks failed on {path} because the chunk {chunkId} is not in COMPLETE |
| [S01004](S01004.md) | <WARNING> openChunks attempted to colocate chunk <xxx> with sibling chunks but |
| [S01005](S01005.md) | The script must be executed on an initialized controller. RefId: S01005 |
| [S01006](S01006.md) | The chunk <xxx> is reported as stale on the controller. Check the controller logs |
| [S01007](S01007.md) | {taskDesc}: Retry {retries}/{maxRetries} : Failed to recover chunk {chunkId}. Check |
| [S01008](S01008.md) | The source and target replicas of chunk <chunkId> for recovery are not available |
| [S01009](S01009.md) | <WARN> Liveness checking: data node {nodeDesc} has gone offline. RefId:S01009 |
| [S01010](S01010.md) | ChunkCache::flushTableToDisk: Failed to flush TSDB Cache Engine to disk due to Out of |
| [S01011](S01011.md) | The Raft WAL file for the raft group {RaftGroupAlias} is incomplete. The system will |
| [S01012](S01012.md) | No available replica for the chunk xxx is found on the controller. RefId:S01012 |
| [S01013](S01013.md) | Failed to drop partition {partition} because the replicas are currently unavailable |
| [S01014](S01014.md) | A column with name <xxx> already exists in table. RefId:S01014 |
| [S01015](S01015.md) | The number of columns of the current table must match that of the target table |
| [S01016](S01016.md) | Some of the data being written is not defined in the partitioning scheme of the |
| [S01017](S01017.md) | Failed to garbage collect outdated level file <filePath> with error: |
| [S01018](S01018.md) | A STRING or SYMBOL column used for value-partitioning cannot contain invisible |
| [S01019](S01019.md) | <restore> Failed to add new value partitions to database {dbUrl}. Please manually |
| [S01020](S01020.md) | The specified partitions must already exist in the database. RefId:S01020 |
| [S01021](S01021.md) | When chunkGranularity is set to DATABASE, only SQL backup (specified by sqlObj) is |
| [S01022](S01022.md) | Cannot back up the partitions to the specified backupDir as back up files created |
| [S01023](S01023.md) | The chunk <xxx> is being replicated in the slave cluster for cluster replication |
| [S01024](S01024.md) | <funcName> must be executed on the controller of the master cluster |
| [S01025](S01025.md) | The task with ID <taskId> on node <nodeAlias> is finished or invalid |
| [S01026](S01026.md) | CacheDumpTaskDispatcher::{function} {action}. Out of memory error occurred while |
| [S01027](S01027.md) | <WARNING> TSDBEngine::MergeRunner xxx. Out of memory error occurred while merging |
| [S01028](S01028.md) | Out of memory error occurred during asynchronous sorting in TSDB cache engine. Will |
| [S01029](S01029.md) | TSDB Engine failed to read xxx. RefId:S01029 |
| [S01030](S01030.md) | coldVolumes directories must follow these formats: local directory with |
| [S01031](S01031.md) | [TieredStorageMgmt] : To configure coldVolumes with S3 volumes, the awss3 plugin must |
| [S01032](S01032.md) | To configure coldVolumes with S3 volumes, s3AccessKeyId, s3SecretAccessKey and |
| [S01033](S01033.md) | Failed to write to TSDB editlog in replaceTableRecord with I/O error: |
| [S01034](S01034.md) | MergeRunner::checkAndDoMerge: Chunk [xxx] does not exist in TSDB |
| [S01035](S01035.md) | [asyncReplication] Failed to write task <tid>, with error: xxx |
| [S01036](S01036.md) | [asyncReplication] Failed to remove task data file <filePath>, with error: |
| [S01037](S01037.md) | [asyncReplication] Failed to open file <filePath>, with error: xxx |
| [S01038](S01038.md) | [asyncReplication] Failed to execute task with taskId <taskId> on the slave |
| [S01039](S01039.md) | [asyncReplication] Skipped task with taskId <taskId>. The task is invalid or has |
| [S01040](S01040.md) | [asyncReplication] Skipped task <tid>. Task data does not exist on site |
| [S01041](S01041.md) | [asyncReplication] Failed to deserialize task <tid>, with error: xxx |
| [S01042](S01042.md) | [asyncReplication] Failed to deserialize the metadata of task <tid>, with error: |
| [S01043](S01043.md) | [asyncReplication] Failed to execute tasks of group <xxx> in execution queue |
| [S01044](S01044.md) | [asyncReplication] Data of task <xxx> has not been persisted on the master |
| [S01045](S01045.md) | Failed to start chunk recovery, chunk <chunkId> is in <xxx> state. Will retry |
| [S01046](S01046.md) | MergeRunner::checkAndDoMerge: Skipped chunk <cid>: chunk in recovery |
| [S01047](S01047.md) | Compaction blocked: Existing task in level <xxx>, chunk <cid>, table |
| [S01048](S01048.md) | Cannot find table <xxx> in metadata.RefId: S01048 |
| [S01049](S01049.md) | TSDBEngine ChunkCache::append: Failed to obtain metadata of chunk <cid> |
| [S01050](S01050.md) | [chunkRecovery]: CRC32 check failed for file <filePath>. The saved checksum |
| [S01051](S01051.md) | [chunkRecovery]: The chunk <xxx> after recovery on the source node remains in |
| [S01052](S01052.md) | OOM occurs when appending data to the OLAP cache engine. Will retry later |
| [S01053](S01053.md) | [TabletCache::loadColumn] The number of rows <xxx> to be loaded from chunk |
| [S01054](S01054.md) | The column at <columnIndex> to be loaded does not exist. The number of available |
| [S01055](S01055.md) | Failed to <xxx>, with error code <xxx>, errno <xxx>. RefId:S01055 |
| [S01056](S01056.md) | None of the specified partitions exist. RefId:S01056 |
| [S01057](S01057.md) | Failed to compact level files, with error code <ret> |
| [S01058](S01058.md) | The data type of the specified partition does not match the partitioning scheme of |
| [S01059](S01059.md) | Function getTSDBCompactionTaskStatus is only enabled in DATANODE or SINGLE mode |
| [S01060](S01060.md) | Chunk <chunkId> is in coldVolumes and can't be compacted |
| [S01061](S01061.md) | Failed to generate checkpoint file <filePath>, with error: xxx |
| [S01062](S01062.md) | Failed to create hard link for column <xxx>, with error: xxx |
| [S01063](S01063.md) | Failed to create rollback log file [xxx] : + xxx + RefId: S01063 |
| [S01064](S01064.md) | Column modifications are only supported for OLAP-based DFS tables. RefId: S01064 |
| [S01065](S01065.md) | The column [" + columnName + "] to be modified cannot be partitioning column. RefId: |
| [S01067](S01067.md) | The function specified in partitionColumns must return a vector/scalar when the input |
| [S01068](S01068.md) | "Failed to lock file <" + fileName + "> with error : " + xxx + " RefId: S01068 |
| [S01069](S01069.md) | The s3AccessKeyId, s3SecretAccessKey and s3Region must be configured in config file |
| [S01070](S01070.md) | The transaction <tid> has expired, and the resolution process has been initiated |
| [S01071](S01071.md) | The transaction <tid> has expired. It will be rolled back without resolution |
| [S01072](S01072.md) | Failed to garbage collect old versioned data because the cached table information on |
| [S01074](S01074.md) | [Recovery: chunk <>, recovery id <>] Failed with exception: xxx. RefId: |
| [S01076](S01076.md) | The new leader <alias> has been waiting for transactions to complete for <xxx> |
| [S01077](S01077.md) | Failed to save table on data node, with error: xxx. RefId: S01077 |

## 02 — SQL

| Code | Message |
|------|---------|
| [S02000](S02000.md) | Columns specified in valueColNames of function unpivot must be of the same data type |
| [S02001](S02001.md) | Duplicate column name: [xxx]. RefId:S02001 |
| [S02002](S02002.md) | Failed to parse the metacode of SQL statement into distributed queries |
| [S02003](S02003.md) | InputTables must be non-partitioned table(s), data source(s), or a dictionary |
| [S02004](S02004.md) | No partition returned by the sql object. RefId:S02004 |
| [S02005](S02005.md) | Unrecognized column name. RefId:S02005 |
| [S02006](S02006.md) | When joining multiple tables, only the first table to be joined can be a partitioned |
| [S02007](S02007.md) | Direct access using column names is not supported to retrieve data from an MVCC |
| [S02008](S02008.md) | Direct access using column names is not supported to retrieve data from a DFS table |
| [S02009](S02009.md) | Direct access using column names is not supported to retrieve data from a stream |
| [S02010](S02010.md) | All columns must be of the same length. RefId:S02010 |
| [S02011](S02011.md) | SQL context is not initialized yet. RefId:S02011 |
| [S02012](S02012.md) | Not support to create temporary table whose name has already been used |
| [S02013](S02013.md) | The left part of a join must be a table. RefId:S02013 |
| [S02014](S02014.md) | The right part of a join must be a table. RefId:S02014 |
| [S02015](S02015.md) | The table object must be a DFS table. RefId: S02015 |
| [S02016](S02016.md) | Invalid columns [xxx]. RefId:S02016 |
| [S02017](S02017.md) | Invalid grouping column. RefId:S02017 |
| [S02018](S02018.md) | The grouping column [xxx] cannot be an array vector. RefId:S02018 |
| [S02019](S02019.md) | The column to be sorted cannot be an array vector. RefId:S02019 |
| [S02020](S02020.md) | The grouping column [xxx] must be a vector. RefId:S02020 |
| [S02021](S02021.md) | The HAVING clause after GROUP BY must be followed by a boolean expression |
| [S02022](S02022.md) | The column [xxx] must use aggregate function. RefId:S02022 |
| [S02023](S02023.md) | The array vector specified in SELECT must be generated by function toArray |
| [S02024](S02024.md) | Array vector does not support SYMBOL or STRING type. RefId:S02024 |
| [S02025](S02025.md) | `The where clause <xxx> of a distributed query should not use any aggregate |
| [S02026](S02026.md) | Function [xxx] cannot be used with CONTEXT BY. RefId:S02026 |
| [S02027](S02027.md) | The length of the vector returned by the UDF specified in SELECT must be the same as |
| [S02028](S02028.md) | Only one parameter can be passed to row reduction operation [xxx] when it is used |
| [S02029](S02029.md) | Row reduction operation [xxx] cannot be used with PIVOT BY. RefId:S02029 |
| [S02030](S02030.md) | Function toArray cannot be used with PIVOT BY. RefId:S02030 |
| [S02031](S02031.md) | Only one parameter can be passed to null-filling operation [xxx] when it is used with |
| [S02032](S02032.md) | Cannot nest aggregate function. RefId:S02032 |
| [S02033](S02033.md) | The FROM clause must be followed by a table. RefId:S02033 |
| [S02034](S02034.md) | The where condition must be an expression or a function call, but now it is <xxx> |
| [S02035](S02035.md) | The where condition must be a logical expression. RefId:S02035 |
| [S02036](S02036.md) | The size of the result returned by the where condition <xxx> does not match the |
| [S02037](S02037.md) | The '[not] in' predicate cannot be followed by columns from the partitioned table |
| [S02038](S02038.md) | Order-sensitive or user-defined functions are not allowed in the order by clause […] |
| [S02039](S02039.md) | The number of partitions […] relevant to the query is too large. Please add more |
| [S02040](S02040.md) | The temporal partitioning column <xxx> must be compared with a temporal object in |
| [S02041](S02041.md) | The nested joins in a query must return a table. RefId:S02041 |
| [S02042](S02042.md) | Distributed queries do not support the ‘exists’ keyword. RefId:S02042 |
| [S02043](S02043.md) | The 'asis' keyword is not supported without a PIVOT BY clause. Please include a valid |
| [S02044](S02044.md) | Unexpected function arguments in analytic function. RefId: S02044 |
| [S02045](S02045.md) | The PARTITION/ORDER BY column 'xxx' must be included in the GROUP BY clause. RefId: |
| [S02046](S02046.md) | Analytic functions are not allowed in WHERE clause, GROUP BY clause, or to be nested |
| [S02047](S02047.md) | Analytic functions cannot be used with CONTEXT BY or PIVOT BY. RefId: S02047 |
| [S02048](S02048.md) | Order-sensitive functions are not allowed in ORDER BY clause within an OVER clause |
| [S02049](S02049.md) | Analytic function does not support function '%s'. RefId: S02049 |
| [S02050](S02050.md) | The “select“ clause does not support the following functions: aggregate |
| [S02051](S02051.md) | Row reduction operation <xxx> cannot be used with PIVOT BY clause within an EXEC |
| [S02052](S02052.md) | The last column for "pivot by" clause must be a partitioning column. RefId: |
| [S02053](S02053.md) | `The select clause with DISTINCT keyword must contain all ORDER BY |
| [S02054](S02054.md) | Can't modify read only table. RefId: S02054 |
| [S02055](S02055.md) | The DISTINCT keyword cannot be used with group by, context by, or pivot by. RefId: |
| [S02056](S02056.md) | For a distributed query, the TOP or LIMIT clause cannot specify an offset when used |
| [S02057](S02057.md) | The 'kendall' function is not allowed in a distributed query. RefId: S02057 |
| [S02059](S02059.md) | Cannot recognize table name or alias '<…>'. RefId: S02059 |

## 03 — 流数据 (Streaming)

| Code | Message |
|------|---------|
| [S03000](S03000.md) | To undefine the shared stream table 'xxx', first cancel all subscriptions to it |
| [S03001](S03001.md) | The engine 'xxx' already exists. Choose another name or release the existing engine |
| [S03002](S03002.md) | Subscription to table <xxx> already exists on this node. Change an actionName or |
| [S03003](S03003.md) | All subscriptions to the stream table <xxx> must be canceled before it can be |
| [S03005](S03005.md) | The reactive state engine doesn't support the aggregate function <%funcName> in |
| [S03006](S03006.md) | To enable table persistence, specify persistenceDir in server configuration and |
| [S03007](S03007.md) | Cannot subscribe to the table <xxx>. Share this table before subscribing. RefId: |
| [S03008](S03008.md) | Subscription is not enabled on this node. Specify mode as single, datanode, or |
| [S03009](S03009.md) | No access to shared table <xxx>. Contact an administrator. RefId: S03009 |
| [S03012](S03012.md) | Data insertion failed: Number of columns in the data to insert doesn't match the |
| [S03013](S03013.md) | Failed to deserialize the heterogeneous stream table, with unknown msgType |
| [S03014](S03014.md) | The time-series engine only accepts aggregate functions as metrics. RefId: S03014 |
| [S03015](S03015.md) | When the fill parameter is a vector, its size must be consistent with the number of |
| [S03016](S03016.md) | The orderbook snapshot engine requires a special license. Update your license or |
| [S03017](S03017.md) | Failed to append data to column 'XXXXX' with error: Incompatible type. Expected: |
| [S03018](S03018.md) | warmupStreamEngine currently only supports the reactive state engine and time series |
| [S03019](S03019.md) | The volume of data exceeds the compression limit. Try inserting data in smaller |
| [S03020](S03020.md) | The leader has not been elected. Try again later. RefId: S03020 |
| [S03021](S03021.md) | Failed to create the HA stream table <xxx>. The feature of HA streaming has not |
| [S03022](S03022.md) | Failed to create the HA stream table <xxx>. Please configure parameter |
| [S03023](S03023.md) | Failed to get the information of persisted stream tables 'XXX'. Please configure |
| [S03024](S03024.md) | Cannot force delete the HA stream table <xxx>.RefId: S03024 |
| [S03025](S03025.md) | Only admin can force delete a stream table from the disk.RefId: S03025 |
| [S03027](S03027.md) | The subscribeTable function can only be executed on a data node or a compute |
| [S03028](S03028.md) | Failed to filter the table. Please set a filtering column first.RefId: S03028 |
| [S03036](S03036.md) | The CEP engine ‘xxx' failed to call function 'xxx’, with error: xxx. RefId: |
| [S03037](S03037.md) | The CEP sub engine ‘xxx' failed to call the onload function, with error: xxx. RefId: |
| [S03038](S03038.md) | Invalid engine. RefId: S03038 |
| [S03039](S03039.md) | Failed to serialize events due to incompatible event fields. Expected: <xxx> |
| [S03040](S03040.md) | Failed to deserialize events due to incompatible event schema. Expected: <xxx> |
| [S03041](S03041.md) | This function can only be called in the monitor within a CEP engine. RefId: |
| [S03042](S03042.md) | The number of result columns must match the number of metrics. RefId: S03042 |
| [S03043](S03043.md) | No access to table [xxxx]. RefId: S03043 |

## 04 — 管理 (Admin / Permission / Cluster)

| Code | Message |
|------|---------|
| [S04001](S04001.md) | The database [" + s + "] does not exist. RefId: S04001 |
| [S04002](S04002.md) | The function view [xxx] does not exist. RefId: S04002 |
| [S04003](S04003.md) | The parameter objs must be a string that begins with 'dfs://' and ends with '\*'. For |
| [S04004](S04004.md) | Non-admin users cannot {action} the {prev} privilege. Contact the administrator |
| [S04005](S04005.md) | To manage permissions for databases you didn't create, you must have the DB\_MANAGE |
| [S04006](S04006.md) | The job parallelism must be between 1 and 64.RefId: S04006 |
| [S04007](S04007.md) | Failed to set the maximum number of file handles that can be opened with error: " + |
| [S04008](S04008.md) | The job priority must be between 0 and 8.RefId: S04008 |

## 05 — 通用 (General)

| Code | Message |
|------|---------|
| [S05000](S05000.md) | The input matrix is singular and cannot be inverted. RefId:S05000 |
| [S05001](S05001.md) | A set does not support random access |
| [S05003](S05003.md) | DECIMAL math overflow RefId:S05003 |
| [S05004](S05004.md) | The column [ZZZ] expects type of XXX, but the actual type is YYY. RefId:S05004 |
| [S05005](S05005.md) | Not allowed to create a void vector. RefId:S05005 |
| [S05006](S05006.md) | The number of columns to be updated must match the number of columns specified in |
| [S05007](S05007.md) | All elements of the input tuple must have the same length. RefId:S05007 |
| [S05008](S05008.md) | Must specify scale for Decimal data type, e.g., DECIMAL32(2). RefId: S05008 |
| [S05009](S05009.md) | The scale of Decimal should be an integer. RefId: S05009 |
| [S05010](S05010.md) | Scale out of bounds (valid range: [0, 9], but get: <xxx>). RefId: S05010 |
| [S05011](S05011.md) | The number of contiguous vector elements has reached its maximum. RefId: S05011 |
| [S05012](S05012.md) | A keyed/indexed table can't contain duplicated keys. RefId: S05012 |
| [S05013](S05013.md) | All elements of a tuple column of a table must have the same type. RefId: S05013 |
| [S05014](S05014.md) | The column <xxx> does not exist. To add a new column, the size of the new column |
| [S05015](S05015.md) | Can't drop a key column. RefId: S05015 |
| [S05016](S05016.md) | An in-memory table can't exceed 2 billion rows. RefId: S05016 |
| [S05017](S05017.md) | A table cannot contain columns with duplicate name: <xxx>.RefId: S05017 |

## 06 — 解释器 (Interpreter / Parser)

| Code | Message |
|------|---------|
| [S06000](S06000.md) | '=' or ':' is expected after the column name. RefId: S06000 |
| [S06001](S06001.md) | If one argument is passed as keyword argument, all subsequent arguments must also be |
| [S06002](S06002.md) | 'share' statement can't be declared within a function definition. RefId: S06002 |
| [S06003](S06003.md) | Not allowed to define a named function [XXX] within another function. RefId: |
| [S06004](S06004.md) | The function or procedure 'XXX' is not defined. RefId: S06004 |
| [S06005](S06005.md) | Not allowed to overwrite existing built-in functions/procedures. RefId: S06005 |
| [S06006](S06006.md) | The object 'XXX' is neither an XDB connection nor a function definition. RefId: |
| [S06007](S06007.md) | Function <xxx> is declared but not defined yet. RefId: S06007 |
| [S06008](S06008.md) | The definition of <xxx> is inconsistent with the declared signature. RefId: |
| [S06009](S06009.md) | To form a pair, both operands must have the same data category. RefId: S06009 |
| [S06010](S06010.md) | Keyword IS must be followed by [NOT] NULL. RefId: S06010 |
| [S06011](S06011.md) | Please use '==' rather than '=' as equal operator in non-sql expression. RefId: |
| [S06012](S06012.md) | A parameter with default value must be read only. RefId: S06012 |
| [S06013](S06013.md) | As long as one parameter sets a default value, all following parameters must set |

## 07 — 其他 (Other - 07)

| Code | Message |
|------|---------|
| [S07000](S07000.md) | [IMOLTP] Failed to start service: Invalid redo file path [...]: A directory with the |
| [S07001](S07001.md) | IMOLTP is currently initializing. Please try again later. RefId: S07001 |
| [S07002](S07002.md) | Cannot insert record with duplicate key 'x' because the table enforces uniqueness on |
| [S07003](S07003.md) | Cannot perform DDL operations on OLTP databases/tables in a 'transaction' statement |
| [S07004](S07004.md) | Data type x is not supported as index key. Supported data types include CHAR, BOOL |
| [S07005](S07005.md) | Strings in key column must not exceed 4096 bytes. RefId: S07005 |
| [S07006](S07006.md) | Cannot use aggregate functions to update the IMOLTP table. RefId: S07006 |

## 09 — 其他 (Other - 09)

| Code | Message |
|------|---------|
| [S09000](S09000.md) | JIT does not support functions with a variable number of parameters.RefId: S09000 |
| [S09001](S09001.md) | JIT: Function passed as the argument to the JIT function can only take integral or |
| [S09002](S09002.md) | JIT: Built-in functions cannot be passed as arguments to the JIT function.RefId: |
| [S09003](S09003.md) | JIT: To form a pair, both operands must have the same data type. RefId: S09003 |
| [S09004](S09004.md) | JIT: The start and end values of 'seq' must have the same temporal data type.RefId: |
| [S09005](S09005.md) | JIT: The assigned variable must have the same type as the indexed value.RefId: |
| [S09006](S09006.md) | JIT: Scalar assignment from vector requires scalar indexing.RefId: S09006 |
| [S09007](S09007.md) | JIT: Right operand of 'cast' must be a constant.RefId: S09007 |
| [S09008](S09008.md) | JIT:Inferring return type failed. All return values must have the same data |
| [S09009](S09009.md) | JIT:Inferring return type failed. The return value cannot be NULL.RefId: S09009 |

## 10 — 其他 (Other - 10)

| Code | Message |
|------|---------|
| [S10000](S10000.md) | Shark requires premium license. Contact technical support for trial license |
| [S10001](S10001.md) | Insufficient GPU memory. Reduce the training data size or initial tree depth.RefId: |
| [S10002](S10002.md) | Failed to detect GPU on the current device.RefId: S10002 |
| [S10003](S10003.md) | Usage: talib(func, args...). func must be a moving function.RefId: S10003 |
| [S10004](S10004.md) | GPLearn currently does not support function <xxx>.RefId: S10004 |
| [S10005](S10005.md) | The number of fitness function parameters must be greater than or equal to 2.RefId: |
| [S10006](S10006.md) | Unsupported keyColumn type: xxxx(类型名称).RefId: S10006 |
| [S10007](S10007.md) | Device Engine does not support function <xxx>.RefId: S10007 |
| [S10008](S10008.md) | keyColumn must be a string or a string vector indicating the name of the key |
| [S10009](S10009.md) | Usage: createDeviceEngine(name, metrics, dummyTable, outputTable, keyColumn |

## 12 — 其他 (Other - 12)

| Code | Message |
|------|---------|
| [S12000](S12000.md) | Failed to rename checkpoint file.RefId: S12000 |
| [S12001](S12001.md) | Cannot restore metalog because the checkpoint file is incomplete. Please contact |
| [S12002](S12002.md) | Flushing is paused because the stashed buffer is too large. Please wait for the |
| [S12003](S12003.md) | Failed to serialize level file {BlockType}: filepath\_=xxx. RefId: S12003 |
| [S12004](S12004.md) | The meta.log file was not found. Please contact technical support to check the online |
| [S12005](S12005.md) | The database is not found during redo log replay. Please contact technical |
| [S12006](S12006.md) | Chunk not found. chunkId=xxx. Please try again, and if the issue persists, contact |
| [S12007](S12007.md) | The specified index type is not supported. Supported types are “bloomfilter” and |
| [S12008](S12008.md) | {indexType} cannot be specified on columns of xxx type. RefId: S12008 |
| [S12009](S12009.md) | An error occurred during level file compaction. Please contact technical |
