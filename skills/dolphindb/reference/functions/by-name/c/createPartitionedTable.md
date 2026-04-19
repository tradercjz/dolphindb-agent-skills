# createPartitionedTable

## 语法

`createPartitionedTable(dbHandle, table, tableName,
partitionColumns, [compressMethods], [sortColumns|primaryKey],
[keepDuplicates=ALL], [sortKeyMappingFunction], [softDelete=false], [indexes],
[latestKeyCache=false], [compressHashSortKey=true],
[encryptMode='plaintext'])`

## 详情

根据 *table* 的结构创建一个空的分区表。

* 对于分布式数据库和本地磁盘数据库，*table* 参数只能是一个表。
* 对于内存数据库，*table* 参数可以是一个表或包含多个表的元组。如果 *table*
  是一个元组，每个 *table* 表示一个分区。

如果参数 *table* 是一个表，则根据该表的结构创建一个分区表。通过
`append!`或
`tableInsert`给新创建的分区表插入数据。它不能用于创建顺序分区的分区表。

如果参数 *table* 是一系列表，则创建一个分区的内存表。参数 *table*
中表的数量与数据库中分区的数量相同。

注：

* 创建分区表时只会使用参数 *table* 的结构，并不会把 *table* 中的数据插入到新的分区表中。
* OLAP 引擎允许集群每个节点创建的不同的分布式分区表句柄（包含临时句柄）上限为 8192；TSDB
  引擎没有上限。临时句柄的说明请参考注释。
* 调用函数 createPartitionedTable
  创建分布式分区表时，若用户没有创建一个句柄变量来接收函数的返回值，则每个数据库会创建一个临时句柄。若在同一数据库下多次创表，则该数据库的临时句柄会被覆盖。

## 参数

注：

参数 *sortColumns*, *keepDuplicates* 及
*sortKeyMappingFunction* 仅在 `database` 的 *engine* 参数指定为
TSDB 时才有效。

**dbHandle**
database
函数返回的数据库句柄。它可以是本地磁盘数据库，也可以是分布式数据库。*dbHandle* 为空字符串或没有指定时，表示内存数据库的句柄。

**table** 一个表或包含多个表的元组。系统将会根据该表的结构创建新的分区表。

**tableName** 一个字符串，表示分区表的名称。表名只能由中文或英文字母、数字或下划线（\_）组成，且必须以中文或英文字母开头。

**partitionColumns** 一个字符串或字符串向量，表示分区列或者应用于分区列的函数调用（例如："partitionFunc(id)"）。对于组合分区，*partitionColumns*
是一个字符串向量。对非顺序分区，此参数为必选参数。若指定该参数为函数调用，则必须有且仅有一个参数是分区列，且其它参数是常量标量。此时，系统在创建分布式表时，会根据函数调用返回的数据进行分区。然而，在 SQL
查询中，对于基于分区列（例如partitionFunc(id) 中的 id 列）的查询优化行为受到一些限制：

* 当 WHERE 条件中对分区列进行非等值比较（例如 >，<）时，不会进行分区剪枝。
* 无法根据分区列或分区路径进行其它查询优化。

**compressMethods** 一个字典，指定某些列使用 lz4, delta, zstd 或 chimp
压缩算法存储。key 为字段名，value 为压缩算法（"lz4", "delta", "zstd" 或 "chimp"）。若未指定，默认采用 lz4 压缩算法。有关
Delta 压缩算法，亦称为 delta-of-delta encoding，参考：[Delta Compression Techniques](http://engineering.nyu.edu/~suel/papers/delta-chap.pdf)。

* 对于 DECIMAL, SHORT, INT, LONG 与时间或日期类型数据，建议采用 Delta 算法压缩。
* 将字符串存储为 SYMBOL 类型数据，实现对字符串类型的压缩。
* 对于小数部分长度在三位以内的 DOUBLE 类型的数据，可以考虑使用 chimp 算法压缩。

**sortColumns** 字符串标量或向量，用于指定每一分区内的排序列，每次写入磁盘的数据在每一分区内将按 *sortColumns*
进行排序。系统默认 *sortColumns* （指定多列时） 除最后一列外的列字段作为排序的索引列，称作 sort key。每一分区内，同一个 sort
key 组合值对应的数据将按最后一列的值顺序连续存放在一起。查询时，若查询条件包含索引列，可以快速定位数据所在的数据块位置，提高查询性能。

* 仅当 dbHandle 指示的数据库采用 "TSDB" 引擎（engine="TSDB"）时，本参数才生效。
* *sortColumns* 只能是 INTEGER, TEMPORAL, LITERAL 类别（除 BLOB） 或 DECIMAL 类型。
  + 若 *sortColumns* 指定为多列，则 *sortColumns*
    的最后一列必须为时间类型或整型，其余列为索引列，且索引列不能为为 TIME, TIMESTAMP, NANOTIME,
    NANOTIMESTAMP 类型。
  + 若 *sortColumns* 仅指定一列，则该列作为 sort key，其类型可以是除 TIME, TIMESTAMP,
    NANOTIME, NANOTIMESTAMP 之外的任意类型。若 *sortColumns* 为时间类型 （非分区列），且同时指定了
    *sortKeyMappingFunction*，则查询的过滤条件中 *sortColumns*
    只能与相同时间类型的值进行比较。
* 频繁查询的字段适合设置为 *sortColumns*（建议不超过 4 列），且建议优先把查询频率高的字段作为 *sortColumns*
  中位置靠前的列。
* 为保证性能最优，建议每个分区内索引列的组合数（sort key）不超过 2000 个。
* *sortColumns* 是每个分区内部 level file 内数据的排序依据，与其是否为分区字段无关。

**primaryKey**字符串标量或向量，用于指定主键列。在数据写入操作中，如果主键相同，新的数据覆盖现有数据。

* 仅当*dbHandlei* 指示的数据库采用 "PKEY" 引擎（engine="PKEY"）时，本参数才生效。
* 主键列必须包含所有的分区列。
* 主键列支持的类型包括：BOOL, CHAR, SHORT, INT, LONG, INT128, STRING, TIME, SECOND,
  MINUTE, DATE, MONTH, DATEHOUR, DATETIME, SYMBOL, TIMESTAMP, NANOTIME,
  NANOTIMESTAMP, UUID, COMPLEX, POINT, IPADDR, DECIMAL32, DECIMAL64,
  DECIMAL128。

**keepDuplicates** 指定在每个分区内如何处理所有 *sortColumns*
之值皆相同的数据。提供以下选项：

* ALL：保留所有数据，为默认值。
* LAST：仅保留最新数据
* FIRST：仅保留第一条数据

在 TSDB 引擎单个分区 sort key 组合数过多，但每个 sort key 组合值对应的记录数较少的场景下，建议配置
*sortKeyMappingFunction* 参数以对 sort key 组合数进行降维。降维后单个 TSDB level File
内的数据块可以存储更多的数据，查询时既减少了读数据块的次数（降低了 I/O 开销），又提升了数据的压缩率。

**sortKeyMappingFunction** 由一元函数对象组成的向量，其长度与 sort key 一致。若只指定一个映射函数 mapfunc，必须写为
*sortKeyMappingFunction*=[mapfunc]。用于指定应用在索引列中各列的映射函数，以减少 sort key
的组合数，该过程称为 sort key 降维。

索引列中的各列被对应的映射函数降维后，原本的多个 sort key 组合值会被重新映射到一个新的 sort key
组合值上。而每个新 sort key 组合值对应的数据仍将根据 *sortColumns*
的最后一列进行排序。降维在写入磁盘时进行，因此指定该参数一定程度上将影响写入性能。

注：

* *sortKeyMappingFunction*
  指定的函数对象与索引列中的各列一一对应，若其中某列无需降维，则函数对象置为空。
* 当 *sortKeyMappingFunction* 中的函数对象为
  `hashBucket`，且需要对采用 Hash 分区的分区字段进行降维时，应确保 Hash 分区的数量和
  `hashBucket` 中的 *buckets*
  之间不存在整除关系（*buckets*=1 除外），否则会导致同一分区内的所有 Hash 值得到的 key 都相同。

**softDelete** 用于启用或禁用软删除功能。默认为
false，即禁用。该参数适于在行数多但删除量小的场景下使用。使用该参数需要同时满足以下条件：

* 由TSDB 存储引擎创建的数据库内的表
* *keepDuplicates* 已设置为 LAST

**indexes** 为一个字典，用于为表中的列指定索引。仅当 *dbHandle* 指示的数据库采用
“TSDB” （engine=”TSDB” 且 keepDuplicates=ALL）或 “PKEY” 引擎（engine=”PKEY”）时，本参数才生效。

* 设置布隆过滤器，适用于 PKEY 数据库。

  为 PKEY 数据库表中的列指定索引。字典的键是 STRING
  类型标量，表示列名；值是 STRING 类型标量，表示为该列指定的索引类型。目前支持设置 “bloomfilter”
  索引类型：适用于对大基数列进行点查，且基数越大，索引效果越好，如身份证 ID、订单号、从业务上游同步的外键等数据列。目前支持的类型包括 BOOL,
  CHAR, SHORT, INT, LONG, TEMPORAL, BLOB, STRING, BINARY, COMPLEX, DECIMAL32,
  DECIMAL64, DECIMAL128。

  注：

  引擎会将所有主键列合并为组合主键，并为组合主键设置 bloomfilter 类型索引。
* 设置文本索引，适用于 PKEY 数据库。

  为某一列设置文本索引，以便在查询时对该列进行高效的文本查询。每个表支持为 STRING 或 BLOB
  类型的非主键列设置文本索引。字典的 key 为 STRING 类型，表示列名，且该列类型必须是 STRING 或 BLOB；字典的 value 为
  STRING 类型，其形式为
  `textindex(parser=english,full=false,lowercase=true,stem=true)`，其中：

  + parser：指定分词器。没有默认值，必须显式指定。可选值为 none, english, chinese, mixed：

    - none：不分词。
    - english：英文分词器，按照空格和标点进行分词，适合于英文为主要内容的场景。
    - chinese：中文分词器。按照中文词库、空格和标点进行分词。适合于中文较多，仅有少量英文或对英文要求不高的场景。
    - mixed：混合分词器。英文按单词分词，中文按 Bigram 分词（以两个连续字符为单位进行分词，且会重叠。如
      '武汉市长江大桥' 会被分词为 '武汉' '汉市' '市长' '长江' '江大'
      '大桥'）。适合于中英文交替，且对英文要求较高的场景。
  + full：设置中文分词时的分词模式。该属性仅在 parser=chinese 时有效。默认值为 false。

    - false：默认模式。词语之间不会重叠和包含。比如 '武汉市长江大桥' 会分成 '武汉市' 和 '长江大桥'。
    - true：全分词模式。该模式会尽可能多的分析句子中包含的词语。比如 '武汉市长江大桥' 会分成 '武汉', '武汉市',
      '市长', '长江', '长江大桥', '大桥'。
  + lowercase：是否忽略大小写。该属性在 *parser* 为 english, chinese, mixed
    时有效。默认值为true。

    - true：适用于需要忽略英文大小写的场景。
    - false：适用于需要大小写敏感的场景。
  + stem：是否将英文单词作为词干匹配。该属性仅在 parser=english 且 lowercase=true 时生效。默认值为
    false。

    - true：将英文单词作为词干。此时可能会匹配到相应的派生词，例如查询单词'dark'，可能会搜到含 'darkness'
      的结果。
    - false：只能精确查询结果。
* 设置向量索引，适用于 TSDB 和 PKEY 数据库。

  为某一列设置向量索引，以便在查询时对该列进行高效的欧氏距离计算。目前，每个表仅支持为单个列设置向量索引。字典的键为 STRING
  类型，表示列名，且该列的类型必须为 FLOAT[] 或 DOUBLE[]；字典的 value 为 STRING 类型，其形式为
  `"vectorindex(type=flat, dim=128)"`，其中：

  type 可选值为 flat, pq, ivf, ivfpq, hnsw：

  + flat 适用于数据规模在数百至数万级别的向量数据，或需要最高精度的场景。
  + pq 适用于数据规模在数十万至数千万级别的向量数据，且对搜索精度要求不高的场景。常见应用场景如大型数据库、视频库等。
  + ivf 适用于数据规模在数万至数百万级别的向量数据，常见应用场景如图片检索、文本检索等。
  + ivfpq
    适用于数据规模在数百万至数千万级别的向量数据，需要在检索速度和精度之间找到最佳平衡的场景。常见应用场景如大型推荐系统、社交网络中的用户匹配。
  + hnsw 适用于数据规模在数亿至数十亿级别的向量数据，并对检索速度，精度和动态更新有高要求的场景，常见应用场景如实时推荐系统、在线搜索、RAG
    等。

  dim 为正整数，表示向量的维度。若 *type* 指定为 pq 或 ivfpq，则要求
  *dim* 为 4 的倍数。 后续插入的向量维度必须为 *dim*，否则会插入失败。

  如果已为某一列设置了向量索引，在查询语句中，若同时满足以下条件，则会应用向量索引提升查询性能：

  + 不包含 join 语句
  + 包含 order by 子句且其中只包含对该列应用 rowEuclidean 函数并按升序排序
  + 包含 limit 子句
  + 若引擎为 TSDB，where 子句中不包含 sort key

  注：

  当引擎为 PKEY，在满足上述查询条件时，查询会先根据 order by 子句和 limit
  子句对索引列进行过滤，再将所得结果根据 where 条件进行过滤，由此得到的结果可能会比 limit 的结果少。

**latestKeyCache** 可选参数，布尔标量，用于设置 IOTDB 是否开启最新值缓存功能。默认值为 false，即关闭。注意：该参数为 true
时，参数 *sortColumns* 至少需要包含两列。一般为 ID 列、各种 tag 列和时间列。

**compressHashSortKey** 可选参数，布尔标量，用于设置是否开启 sortColumns 列压缩功能。当引擎为 IOTDB 时，默认值为
true。当 *sortKeyMappingFunction* 设置为 `hashBucket`
函数时，该功能默认开启。

注意：建立点位管理表时，

* 须保证当前数据库使用 IOTDB 引擎。
* 暂不支持通过 `createPartitionedTable` 函数创建 IOTANY 列，只能通过 create 语句创建。
* 暂不支持 softDelete 等利用 cid 特性的功能。故建立时须设置 softDelete=false。
* 不支持 sortColumns 中包含 DECIMAL 类型。

**encryptMode** 可选参数，字符串标量，指定表的加密方式，默认为不加密（明文模式）。仅 Linux
系统支持该参数。目前支持以下可选值（大小写不区分）：plaintext, aes\_128\_ctr, aes\_128\_cbc, aes\_128\_ecb,
aes\_192\_ctr, aes\_192\_cbc, aes\_192\_ecb, aes\_256\_ctr, aes\_256\_cbc, aes\_256\_ecb,
sm4\_128\_cbc, sm4\_128\_ecb。

## 返回值

返回一个表。

## 例子

例1. 在分布式数据库中创建一个分区表

例1.1 创建一张 OLAP 引擎下的分区表。

```
n=1000000;
t=table(2020.01.01T00:00:00 + 0..(n-1) as timestamp, rand(`IBM`MS`APPL`AMZN,n) as symbol, rand(10.0, n) as value)
db = database("dfs://rangedb_tradedata", RANGE, `A`F`M`S`ZZZZ)
Trades = db.createPartitionedTable(table=t, tableName="Trades", partitionColumns="symbol", compressMethods={timestamp:"delta"});
```

`createPartitionedTable` 只是建立一张空的表格 Trades，该表复制了表 t
的字段。接着用 `append!` 函数将数据追加到 Trades 表里。

```
Trades.append!(t);
```

查询分区表：

```
Trades=loadTable(db,`Trades);
select min(value) from Trades;

0
```

在分布式数据库中，初次创建表后，可以跳过 loadTable 把表载入内存的步骤，因为分布式文件系统会动态刷新表的内容。系统重启后，需要再次执行
`loadTable` 函数加载表。

例1.2 创建一张 TSDB 引擎下的分区表。

```
n = 10000
SecurityID = rand(`st0001`st0002`st0003`st0004`st0005, n)
sym = rand(`A`B, n)
TradeDate = 2022.01.01 + rand(100,n)
TotalVolumeTrade = rand(1000..3000, n)
TotalValueTrade = rand(100.0, n)
schemaTable_snap = table(SecurityID, TradeDate, TotalVolumeTrade, TotalValueTrade).sortBy!(`SecurityID`TradeDate)

dbPath = "dfs://TSDB_STOCK"
if(existsDatabase(dbPath)){dropDatabase(dbPath)}
db_snap = database(dbPath, VALUE, 2022.01.01..2022.01.05, engine='TSDB')
snap=createPartitionedTable(dbHandle=db_snap, table=schemaTable_snap, tableName="snap",
    partitionColumns=`TradeDate, sortColumns=`SecurityID`TradeDate, keepDuplicates=ALL,
    sortKeyMappingFunction=[hashBucket{,5}])
snap.append!(schemaTable_snap)
flushTSDBCache()
snap = loadTable(dbPath, `snap)
select * from snap
```

例2. 在内存数据库中创建一个分区表

例2.1 创建分区常规内存表

```
n = 200000
colNames = `time`sym`qty`price
colTypes = [TIME,SYMBOL,INT,DOUBLE]
t = table(n:0, colNames, colTypes)
db = database(, RANGE, `A`D`F)
pt = db.createPartitionedTable(table=t, tableName=`pt, partitionColumns=`sym)

insert into pt values(09:30:00.001,`AAPL,100,56.5)
insert into pt values(09:30:01.001,`DELL,100,15.5)
```

例2.2 创建分区键值内存表

```
n = 200000
colNames = `time`sym`qty`price
colTypes = [TIME,SYMBOL,INT,DOUBLE]
t = keyedTable(`time`sym, n:0, colNames, colTypes)
db = database(, RANGE, `A`D`F)
pt = db.createPartitionedTable(table=t, tableName=`pt, partitionColumns=`sym)

insert into pt values(09:30:00.001,`AAPL,100,56.5)
insert into pt values(09:30:01.001,`DELL,100,15.5)
```

例2.3 创建分区流数据表

注意，创建分区流数据表时 `createPartitionedTable`
的第二个参数必须是元组，并且其长度必须与分区数量相等，每个表对应一个分区。下例中，trades\_stream1 和 trades\_stream2 组成一个分区流数据表
trades。写入数据时，只能分别往 trades\_stream1 和 trades\_stream2 写入，不能直接写入到 trades。查询 trades
可以获取到两个表的数据。

```
n=200000
colNames = `time`sym`qty`price
colTypes = [TIME,SYMBOL,INT,DOUBLE]
trades_stream1 = streamTable(n:0, colNames, colTypes)
trades_stream2 = streamTable(n:0, colNames, colTypes)
db=database(, RANGE, `A`D`F)
trades = createPartitionedTable(db,table=[trades_stream1, trades_stream2], tableName="", partitionColumns=`sym)

insert into trades_stream1 values(09:30:00.001,`AAPL,100,56.5)
insert into trades_stream2 values(09:30:01.001,`DELL,100,15.5)

select * from trades;
```

| time | sym | qty | price |
| --- | --- | --- | --- |
| 09:30:00.001 | AAPL | 100 | 56.5 |
| 09:30:01.001 | DELL | 100 | 15.5 |

例2.4 创建分区 MVCC 内存表

创建分区 MVCC 内存表的方式与创建分区流数据表的方式相同。

```
n=200000
colNames = `time`sym`qty`price
colTypes = [TIME,SYMBOL,INT,DOUBLE]
trades_mvcc1 = mvccTable(n:0, colNames, colTypes)
trades_mvcc2 = mvccTable(n:0, colNames, colTypes)
db=database(, RANGE, `A`D`F)
trades = createPartitionedTable(db,table=[trades_mvcc1, trades_mvcc2], tableName="", partitionColumns=`sym)

insert into trades_mvcc1 values(09:30:00.001,`AAPL,100,56.5)
insert into trades_mvcc2 values(09:30:01.001,`DELL,100,15.5)

select * from trades;
```

| time | sym | qty | price |
| --- | --- | --- | --- |
| 09:30:00.001 | AAPL | 100 | 56.5 |
| 09:30:01.001 | DELL | 100 | 15.5 |

例3. 创建 TSDB 分区表时设置向量索引，提高查询性能。

```
db = database(directory="dfs://indexesTest", partitionType=VALUE, partitionScheme=1..10, engine="TSDB")
schematb = table(1:0,`col0`col1`col2`col3,[INT,INT,TIMESTAMP,FLOAT[]])
pt = createPartitionedTable(dbHandle=db, table=schematb, tableName=`pt, partitionColumns=`col0, sortColumns=`col1`col2, indexes={"col3":"vectorindex(type=flat, dim=5)"})

tmp = cj(table(1..10 as col0),cj(table(1..10 as col1),table(now()+1..10 as col2))) join table(arrayVector(1..1000*5,1..5000) as col3)

pt.tableInsert(tmp)

select * from pt where col2<now() order by rowEuclidean(col3,[1339,252,105,105,829]) limit 10
```

| col0 | col1 | col2 | col3 |
| --- | --- | --- | --- |
| 2 | 1 | 2024.06.27 16:56:38.950 | [526, 527, 528, 529, 530] |
| 2 | 1 | 2024.06.27 16:56:38.949 | [521, 522, 523, 524, 525] |
| 2 | 1 | 2024.06.27 16:56:38.951 | [531, 532, 533, 534, 535] |
| 2 | 1 | 2024.06.27 16:56:38.948 | [516, 517, 518, 519, 520] |
| 2 | 1 | 2024.06.27 16:56:38.952 | [536, 537, 538, 539, 540] |
| 2 | 1 | 2024.06.27 16:56:38.947 | [511, 512, 513, 514, 515] |
| 2 | 1 | 2024.06.27 16:56:38.953 | [541, 542, 543, 544, 545] |
| 2 | 1 | 2024.06.27 16:56:38.946 | [506, 507, 508, 509, 510] |
| 2 | 1 | 2024.06.27 16:56:38.954 | [546, 547, 548, 549, 550] |
| 2 | 1 | 2024.06.27 16:56:38.945 | [501, 502, 503, 504, 505] |

例4. 创建主键引擎的分区表

```
db = database(directory="dfs://PKDB", partitionType=VALUE, partitionScheme=1..10, engine="PKEY")
schematb = table(1:0,`id1`id2`val1`val2`date1`time1,[INT,INT,INT,DECIMAL32(2),DATE,TIME])
pkt = createPartitionedTable(dbHandle=db, table=schematb, tableName="pkt", partitionColumns="id1", primaryKey=`id1`id2, indexes={"val1": "bloomfilter", "val2": "bloomfilter"})
```

例5. 创建点位管理表

本例中，我们通过复合分区方案按 id 和 ts 分区，创建了一个名为 pt 的点位管理表。该表使用 ticket 和 id2 作为唯一识别一个点位的两列；启用最新值缓存和
hashSortKey
压缩。

```
db1 = database(, partitionType=HASH, partitionScheme=[INT, 10])
db2 = database(, partitionType=VALUE, partitionScheme=2017.08.07..2017.08.11)
db = database(dbName, COMPO, [db1, db2], engine='IOTDB')
schematb = table(1:0,`id`ticket`id2`ts,[INT,SYMBOL,LONG,TIMESTAMP])
pt = createPartitionedTable(dbHandle=db, table=schematb, tableName="pt", partitionColumns=`id`ts, primaryKey=`ticket`id2`ts, sortKeyMappingFunction = [hashBucket{, 50}, hashBucket{, 50}], latestKeyCache = true )
```
