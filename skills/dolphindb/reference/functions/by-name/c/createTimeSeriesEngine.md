# createTimeSeriesEngine

## 语法

`createTimeSeriesEngine(name, windowSize, step, metrics,
dummyTable, outputTable, [timeColumn], [useSystemTime=false], [keyColumn],
[garbageSize], [updateTime], [useWindowStartTime], [roundTime=true],
[snapshotDir], [snapshotIntervalInMsgCount], [fill='none'], [forceTriggerTime],
[raftGroup], [keyPurgeFreqInSec=-1], [closed='left'],
[outputElapsedMicroseconds=false], [subWindow], [parallelism=1],
[acceptedDelay=0], [outputHandler], [msgAsTable=false])`

别名：`createTimeSeriesAggregator`

## 详情

创建流数据时间序列引擎，以实现基于时间的滑动窗口或滚动窗口进行实时计算。

时序引擎的聚合计算的算子分为增量计算和全量计算两种。增量计算算子不会保留历史数据，每次有数据进来就会进行增量计算；而全量计算算子（例如自定义的聚合函数，或未经优化的内置聚合函数，亦或是嵌套了状态函数的函数）会保留窗口内完整的数据，待触发输出时进行全量计算。

时序引擎对以下聚合计算算子进行了优化，实现了增量计算，显著提升了性能：corr, covar, first, last, max,
med, min, percentile, quantile, std, var, sum, sum2, sum3, sum4, wavg, wsum, count,
firstNot, ifirstNot, lastNot, ilastNot, imax, imin, nunique, prod, sem, mode,
searchK, beta, avg, covarp, mcovarp, tmcovarp, cumcovarp, mcovarpTopN, tmcovarpTopN,
cumcovarpTopN。

更多流数据引擎的应用场景说明可以参考 流计算引擎。

### 窗口

* 窗口边界规整：对起始窗口左边界进行规整。（详情请参考 *step* 和
  *roundTime* 的参数说明以及 `规整规则表`）
* 窗口确定：

  + *windowSize* 确定窗口长度。
  + *closed* 确定窗口左闭右开或左开右闭。
  + *step* 确定滑动的步长。

  其中，*windowSize* 与 *step* 的单位取决于
  *useSystemTime* 参数。若 *useSystemTime* = true，
  *windowSize* 与 *step* 的单位是毫秒。若 *useSystemTime* =
  false，*windowSize* 与 *step* 的单位同 *timeColumn*
  列的精度一致。
* 窗口截取：*useSystemTime*
  参数决定了如何截取窗口，可以基于数据的时间列，亦可以基于数据注入系统的时间进行截取。

### 计算

* 乱序数据处理规则：
  + 若指定了 *timeColumn*，则 *timeColumn* 的时间必须为非递减序列；若同时指定了
    *keyColumn*，则按照分组分别进行滑动窗口计算，*timeColumn*
    在每组内的时间必须为非递减序列。否则，时间乱序的数据在计算中会被直接丢弃。
  + 若希望接收指定范围内的乱序数据，可以设置 *acceptedDelay*，详见 *acceptedDelay*
    参数说明。
* 触发规则：若指定了
  *timeColumn*，当前窗口的计算将由该窗口结束后收到的第一条数据触发；若设置 *useSystemTime* =
  true，窗口结束后会自动触发计算。
* 强制触发规则：对长时间未触发计算的窗口数据，可以通过设置 *updateTime* 或
  *forceTriggerTime* 强制触发计算。具体规则请参考参数说明。
* 窗口填充规则：未指定 *fill* 或指定 *fill* = "none"
  时，只会输出计算结果不为空的窗口；若指定了 *fill*，则会输出所有窗口，且根据 *fill*
  规则对结果为空的窗口进行填充。

### 其它功能

* 支持数据/状态清理：清理引擎中堆积的数据和不再需要的状态信息。（详情请参考
  *garbageSize* 和 *keyPurgeFreqInSec* 的参数说明）
* 快照机制：启用快照机制之后，系统若出现异常，可及时将流数据引擎恢复到最新的快照状态。（详情请参考
  *snapshotDir* 和 *snapshotIntervalInMsgCount* 的参数说明）

## 参数

**name** 字符串标量，表示时间序列引擎的名称，作为其在一个数据节点/计算节点上的唯一标识。可包含字母，数字和下划线，但必须以字母开头。

**windowSize** 正整数标量或向量，表示滑动窗口的长度。

**step** 正整数标量，表示滑动窗口移动的步长。 *windowSize* 必须是 *step*
的整数倍，否则会抛出异常。*windowSize* 和 *step* 的单位与 *useSystemTime* 有关：

* 若 *useSystemTime* 为 true，则 *windowSize* 和
  *step* 的单位为毫秒。
* 若 *useSystemTime* 为 false，则 *windowSize* 和
  *step* 的单位与 *timeColumn* 的时间精度一致。

**metrics** 以元代码的格式表示计算指标，支持输入元组。有关元代码的更多信息可参考 元编程。

* 计算指标可以是一个或多个系统内置或用户自定义的聚合函数（使用 defg 关键字定义），如
  <[sum(volume), avg(price)]>；可以对聚合结果使用表达式，如
  <[avg(price1)-avg(price2)]>；也可对列与列的计算结果进行聚合计算，如
  <[std(price1-price2)]>。
* *metrics* 内支持调用具有多个返回值的函数，例如 <func(price) as
  `col1`col2>（可不指定列名）。
* 支持指定为一个常量标量或向量，例如 <1>，<[1, 2, 3]> 。当指定为常量向量时，对应的输出列必须设置为数组向量类型。
* 若 *windowSize* 为向量， *windowSize* 每个值可对应
  *metrics* 中多个计算指标。例如，*windowSize* 为[10,20]时，metrics可为
  (<[min(volume), max(volume)]>, <sum(volume)>)。
  *metrics* 也可以嵌套输入元组向量。例如：[[<[min(volume), max(volume)]>,
  <sum(volume)>], [<avg(volume)>]]

  注：

  + *metrics* 中使用的列名大小写不敏感，不需要与输入表的列名大小写保持一致。
  + *metrics* 中不可使用嵌套聚合函数。

**dummyTable** 一个表对象，和输入的流数据表的 schema 一致，可以含有数据，亦可为空表。

**outputTable** 计算结果的输出表，可以是内存表或者分布式表。在使用 `createTimeSeriesEngine`
函数之前，需要将输出表预先设立为一个空表，并指定各列列名以及数据类型。时间序列引擎会将计算结果插入该表。

* 输出表的列顺序如下：

  1. 时间列。其中：

     + 若 *useSystemTime* = true，为 TIMESTAMP 类型；反之，该列数据类型与
       *timeColumn* 列一致。
     + 若 *useWindowStartTime* =
       true，显示时间为数据窗口起始时间；反之，显示时间为数据窗口终止时间。
  2. 分组列。如果 *keyColumn* 不为空，则其后几列和 *keyColumn*
     设置的列及其顺序保持一致。
  3. 耗时列。如果指定 *outputElapsedMicroseconds* = true，则指定一个 LONG
     类型的列用于存储耗时（单位：微秒）。
  4. 计算结果列。可为多列。

  注：

  自 2.00.10 版本开始，引擎支持通过自定义聚合函数，将多个计算结果以 array
  vector 的形式输出，此时必须在 *outputTable* 中指定对应列类型为 array
  vector，详见例2。

**timeColumn** 可选参数，字符串标量或向量。当 *useSystemTime* = false
时，必须指定该参数。 该参数用于指定订阅的流数据表中时间列的名称。

注：

字符串向量必须是 date 和 time
组成的向量，date 类型为 DATE，time 类型为 TIME, SECOND 或 NANOTIME。此时，输出表第一列的时间类型必须与 concatDateTime(date, time)
的类型一致。

**useSystemTime** 可选参数，布尔值，表示是否使用数据注入引擎时的系统时间作为时间列进行计算。

* 当 *useSystemTime* =
  true时，时间序列引擎会按照数据注入时间序列引擎的时刻（毫秒精度的本地系统时间，与数据中的时间列无关），每隔固定时间截取固定长度窗口的流数据进行计算。只要一个数据窗口中含有数据，数据窗口结束后就会自动进行计算。结果中的第一列为计算发生的时间戳，与数据中的时间无关。
* 当 *useSystemTime* = false（缺省值）时，时间序列引擎根据流数据中的 *timeColumn*
  列来截取数据窗口。一个数据窗口结束后的第一条新数据才会触发该数据窗口的计算。请注意，触发计算的数据并不会参与该次计算。

  例如，一个数据窗口从 10:10:10 到 10:10:19。若 *useSystemTime*
  = true，则只要该窗口中至少有一条数据，该窗口的计算会在窗口结束后的 10:10:20 触发。若 *useSystemTime*
  = false，且 10:10:19 后的第一条数据为 10:10:25，则该窗口的计算会在 10:10:25 触发。

**keyColumn**
可选参数，字符串标量或向量，表示分组列名。若设置，则分组进行聚合计算，例如以每支股票为一组进行聚合计算。

分组字段支持数组向量类型（见例
5）。当分组字段包含数组向量时，引擎会先将数组向量展开为一维向量（flatten），再基于展开后的记录进行分组。此时需满足以下条件：

* 所有数组向量在每一行中的元素长度必须一致；
* *metrics*
  中的表达式的计算结果长度，必须与数组向量展开后的总长度一致（例如：`sum(iif(flatten(orderTypeList)!=2,0，flatten(orderQtyList)/180))`。

**garbageSize** 可选参数，正整数，默认值是
50,000（单位为行）。随着订阅的流数据不断积累，注入时间序列引擎，存放在内存中的数据会越来越多，这时需要清理不再需要的历史数据。当内存中历史数据行数超过
*garbageSize* 值时，系统会清理本次计算不需要的历史数据。如果指定了
*keyColumn*，内存清理是各组内独立进行的。当一个组在内存中的历史数据记录数超出 *garbageSize*
时，会清理该组中本次计算中不需要的历史数据。

注：

对于增量计算算子，系统会自动清理不再需要的历史数据。而对于全量计算算子，需要指定该参数来触发清理历史数据。

**updateTime** 可选参数，非负整数，单位与 timeColumn 的时间精度一致。用于指定比
*step* 更短的计算时间间隔。*step* 必须是 *updateTime* 的整数倍。要设置
*updateTime*， *useSystemTime* 必须设为 false。

如果没有指定 *updateTime*，一个数据窗口结束前，不会发生对该数据窗口数据的计算。若一个窗口长时间未触发计算，可以指定
updateTime，分多次触发当前窗口数据的计算。计算触发的规则为：

* updateTime 指定为正整数值时：

  + 从当前窗口的左边界开始，每隔 *updateTime*
    时间，若有新的数据到来，则对当前窗口内该数据之前的所有数据进行计算。
  + 如果系统经过 2 \* *updateTime* （至少2秒）后仍有未被处理的数据，则触发对当前窗口内所有数据的计算。
  + 若分组计算，则每组内进行上述操作。
* updateTime 指定为 0 时：在新的数据到来后，立即对当前窗口的最新数据计算并输出。

指定 *updateTime*
后，建议使用键值内存表作为输出表。因为每次计算均会增加一条记录，输出表若使用普通内存表或流数据表，则会产生大量带有相同时间戳的结果。因为键值流数据表不可更新记录，输出表亦不推荐使用键值流数据表。

**useWindowStartTime** 可选参数，布尔值，表示输出表中的时间是否为数据窗口起始时间。默认值为
false，表示输出表中的时间为数据窗口起始时间 + *windowSize* 。若 *windowSize* 是向量，
*useWindowStartTime* 必须为 false。

**roundTime** 可选参数，布尔值，表示若数据时间精度为毫秒或者秒且 *step* >
一分钟，如何对窗口边界值进行规整处理。默认值为 true，表示按照既定的多分钟规则进行规整。若为 false，则按一分钟规则进行窗口规整。

若要开启快照机制（snapshot），必须指定 *snapshotDir* 与 *snapshotIntervalInMsgCount*。

**snapshotDir** 可选参数，字符串，表示保存引擎快照的文件目录。

* 指定的目录必须存在，否则系统会提示异常。
* 创建流数据引擎时，如果指定了 *snapshotDir*，会检查该目录下是否存在快照。如果存在，会加载该快照，恢复引擎的状态。
* 多个引擎可以指定同一个目录存储快照，用引擎的名称来区分快照文件。
* 一个引擎的快照可能会使用三个文件名：

  + 临时存储快照信息：文件名为 <engineName>.tmp；
  + 快照生成并刷到磁盘：文件保存为 <engineName>.snapshot；
  + 存在同名快照：旧快照自动重命名为 <engineName>.old。

**snapshotIntervalInMsgCount** 可选参数，为整数类型，表示每隔多少条数据保存一次流数据引擎快照。

**fill** 可选参数，一个标量或向量，指定某个分组的某个窗口无数据时的处理方法。可取以下值：

* 'none': 不输出结果。
* 'null': 输出结果为 NULL。
* 'ffill': 输出上一个有数据的窗口的结果。
* '具体数值'：该值的数据类型需要和对应的 *metrics* 计算结果的类型保持一致。

*fill* 可以输入向量，长度与 *metrics* 元素个数保持一致，表示为每个 *metrics* 指定不同的 *fill*
方式。若为向量，向量中各项只能是 'null', 'ffill' 或一个数值，不能是 'none'。

**forceTriggerTime** 可选参数，是非负整数，单位与 *timeColumn*
的时间精度一致。用于强制触发各个分组未计算的窗口进行计算。要设置 *forceTriggerTime*， *useSystemTime* 必须设置为
false，且不能指定 *updateTime*。强制触发计算及输出规则如下：

1. 未被触发计算的窗口结束后（窗口结束时刻为 t），若收到了其他分组的数据（时间戳为 t1），且满足 t1-t
   ≥ *forceTriggerTime*，则该窗口将被触发计算。
2. 如果某个分组在最后一个窗口被强制触发计算后，没有再收到新的数据，但其他分组仍然收到了新的数据，那么通过 *fill*
   来填充该分组的所有缺失窗口，可以确保在最新时间截面上仍然输出该分组的窗口。如果不指定
   *fill*，则最后一个窗口被触发计算后，该分组不会产生新的窗口。

设置 *forceTriggerTime* 或 *updateTime* 时需注意以下几点：

* 设置 *updateTime*，计算发生后仍有属于当前窗口的数据到达时，当前窗口计算结果会再次更新；
* 设置 *forceTriggerTime*，则触发计算之后收到的数据会被丢弃，建议不要设置太小的
  *forceTriggerTime*。
* 如果 *timeColumn* 指定的时间为 TIME
  类型，数据跨天后无法仅凭时间判断数据的先后顺序，因此会出现跨天无法强制触发的情况。*timeColumn*
  的时间需要加上日期。

**raftGroup** 可选参数，表示流数据高可用订阅端 raft 组的 ID (大于1的整数，由流数据高可用相关的配置项
*streamingRaftGroups* 指定)。设置该参数表示开启计算引擎高可用。在 leader 节点创建流数据引擎后，会同步在
follower 节点创建该引擎。每次保存的 snapshot 也会同步到 follower。当 raft 组的 leader 节点宕机时，会自动切换新 leader
节点重新订阅流数据表。请注意，若要指定 *raftGroup*，必须同时指定 *snapshotDir*。

注意，自 3.00.5
版本起，流计算引擎暂不支持高可用功能，*raftGroup* 参数将不生效。

**keyPurgeFreqInSec** 正整数，单位为秒。用于控制定期清理“窗口数据已为空”的分组对应的
key，从而避免 key 持续增长带来的内存占用。指定该参数后，如果当前数据注入时间与上一次清理时间的间隔 ≥
*keyPurgeFreqInSec*，则会删除当前窗口数据为空的分组及其对应的 key。

注：

* 若需指定该参数，必须指定 *forceTriggerTime*，且不能指定 *fill*。
* 可以通过调用 getStreamEngineStat 函数查看 TimeSeriesEngine 引擎状态的
  numGroups 列，来对比响应式状态引擎清理前后分组数的变化。

**closed** 字符串，用于确定滑动窗口边界的开闭情况。可选值为 'left' 或 'right'，默认值为
'left'。

* closed = 'left'： 窗口左闭右开。
* closed = 'right'： 窗口左开右闭。

**outputElapsedMicroseconds**
布尔值，表示是否输出每个窗口从触发计算到计算完成输出结果的耗时（若指定了 *keyColumn* 则包含数据分组的耗时），默认为 false。指定参数
*outputElapsedMicroseconds* 后，在定义 *outputTable* 时需要在时间列和分组列后增加一个 LONG
类型的列，详见 *outputTable* 参数说明。

**subWindow** 整型或者 DURATION
数据对。在滑动窗口内指定子窗口，仅计算子窗口内的数据。子窗口边界的开闭情况由参数 *closed*
决定。子窗口结束后收到第一条数据触发对子窗口内数据的计算（参考例4）。当 *subWindow* 为整型数据对时，其单位与 *timeColumn*
的时间精度一致。若指定 *subWindow*，则：

* *windowSize* 和 *step* 必须相等。
* 不可设置 *updateTime*>0和 *useSystemTime*=true。

**parallelism** 为不超过 63 的正整数，可选参数，表示并行计算的工作线程数，默认值为
1。在计算量较大时，合理地调整该参数能够有效利用计算资源，降低计算耗时。建议小于机器核数，推荐值为 4 到 8 。

**acceptedDelay** 正整数，可选参数。指定每个窗口接收数据的最大延迟，默认值为 0。若设置该参数，则不能设置
*forceTriggerTime* 或 *updateTime*。

* 当 useSystemTime= true 时，*acceptedDelay* 必须小于等于
  *windowSize*。在窗口结束后的 *acceptedDelay*
  时间内接收到的数据，仍然属于此窗口并参与计算，而不会参与下一个窗口的计算。
* 当 useSystemTime= false 时，该参数用于处理乱序数据。假设当前窗口结束的时间戳为 t ，若收到一条时间戳大于等于
  t+*acceptedDelay*的数据，则触发在此之前收到的所有属于当前窗口的数据进行计算输出，并关闭该窗口。

**outputHandler**
一元函数。设置此参数时，引擎计算结束后，不再将计算结果写到输出表，而是会调用此函数处理计算结果。

**msgAsTable** 布尔标量，表示在设置了参数 outputHandler
时，将引擎的计算结果以表的结构调用函数。默认值为 false，此时将计算结果的每一列作为元素组成元组。

### 规整规则

为了便于观察和对比计算结果，系统会对第一个数据窗口的起始时间进行规整，根据 *step*
参数、数据的时间精度，以及 *roundTime* 参数来确定整数类型的规整尺度
alignmentSize。当时间序列引擎使用分组计算时，所有分组的窗口均进行统一的规整。相同时刻的数据窗口在各组均有相同的边界。

* 当数据时间类型为MONTH时，会以第一条数据对应年份的1月作为窗口的上边界。
* 当数据的时间类型为DATE时，不对第一个数据窗口的边界值进行规整。
* 若数据的时间精度为分钟，如 MINUTE(HH:mm) 类型，alignmentSize 取值如下：

  *若 roundTime = false*：

  | step | alignmentSize |
  | --- | --- |
  | 0~2 | 2 |
  | 3 | 3 |
  | 4~5 | 5 |
  | 6~10 | 10 |
  | 11~15 | 15 |
  | 16~20 | 20 |
  | 21~30 | 30 |
  | >30 | 60 (1小时) |

  *若 roundTime = true*:

  当 step <= 30 时，alignmentSize 取值同上表。当 step > 30
  时，alignmentSize 取值见下表：

  | step | alignmentSize |
  | --- | --- |
  | 31~60 | 60 (1小时) |
  | 61~120 | 120 (2小时) |
  | 121~180 | 180 (3小时) |
  | 181~300 | 300 (5小时) |
  | 301~600 | 600 (10小时) |
  | 601~900 | 900 (15小时) |
  | 901~1200 | 1200 (20小时) |
  | 1201~1800 | 1800 (30小时) |
  | >1800 | 3600 (60小时) |
* 若数据的时间精度为秒，如 DATETIME(yyyy-MM-dd HH:mm:ss) 与
  SECOND(HH:mm:ss) 类型，alignmentSize 的 取值如下：

  *若
  roundTime = false*：

  | step | alignmentSize |
  | --- | --- |
  | 0~2 | 2 |
  | 3 | 3 |
  | 4~5 | 5 |
  | 6~10 | 10 |
  | 11~15 | 15 |
  | 16~20 | 20 |
  | 21~30 | 30 |
  | >30 | 60 (1分钟) |

  *若 roundTime = true*：

  当 step <= 30
  时，alignmentSize 取值同上表。当 step > 30 时，alignmentSize 取值见下表：

  | step | alignmentSize |
  | --- | --- |
  | 31~60 | 60 (1分钟) |
  | 61~120 | 120 (2分钟) |
  | 121~180 | 180 (3分钟) |
  | 181~300 | 300 (5分钟) |
  | 301~600 | 600 (10分钟) |
  | 601~900 | 900 (15分钟) |
  | 901~1200 | 1200 (20分钟) |
  | 1201~1800 | 1800 (30分钟) |
  | >1800 | 3600 (1小时) |
* 若数据的时间精度为毫秒，如 TIMESTAMP(yyyy-MM-dd HH:mm:ss.mmm) 与
  TIME(HH:mm:ss.mmm) 类型，alignmentSize 的取值如下：

  *若 roundTime = false*:

  | step | alignmentSize |
  | --- | --- |
  | 0~2 | 2 |
  | 3~5 | 5 |
  | 6~10 | 10 |
  | 11~20 | 20 |
  | 21~25 | 25 |
  | 26~50 | 50 |
  | 51~100 | 100 |
  | 101~200 | 200 |
  | 201~250 | 250 |
  | 251~500 | 500 |
  | 501~1000 | 1000（1秒） |
  | 1001~2000 | 2000（2秒） |
  | 2001~3000 | 3000（3秒） |
  | 3001~5000 | 5000（5秒） |
  | 5001~10000 | 10000（10秒） |
  | 10001~15000 | 15000（15秒） |
  | 15001~20000 | 20000（20秒） |
  | 20001~30000 | 30000（30秒） |
  | >30000 | 60000（1分钟） |

  *若 roundTime = true*:

  若 *step* <= 30000，alignmentSize 取值同上表；若
  *step* > 30000，alignmentSize 取值见下表：

  | step | alignmentSize |
  | --- | --- |
  | 30001~60000 | 60000（1分钟） |
  | 60001~120000 | 120000（2分钟） |
  | 120001~300000 | 300000（5分钟） |
  | 300001~600000 | 600000（10分钟） |
  | 600001~900000 | 900000（15分钟） |
  | 900001~1200000 | 1200000（20分钟） |
  | 1200001~1800000 | 1800000（30分钟） |
  | >1800000 | 3600000（1小时） |
* 若数据的时间精度为纳秒，如 NANOTIMESTAMP(yyyy-MM-dd
  HH:mm:ss.nnnnnnnnn) 与 NANOTIME(HH:mm:ss.nnnnnnnnn) 类型，alignmentSize
  的取值如下：

  *若 roundTime = false*:

  | step | alignmentSize |
  | --- | --- |
  | 0~2ns | 2ns |
  | 3ns~5ns | 5ns |
  | 6ns~10ns | 10ns |
  | 11ns~20ns | 20ns |
  | 21ns~25ns | 25ns |
  | 26ns~50ns | 50ns |
  | 51ns~100ns | 100ns |
  | 101ns~200ns | 200ns |
  | 201ns~250ns | 250ns |
  | 251ns~500ns | 500ns |
  | >500ns | 1000ns |

  *若 roundTime = true*:

  | step | alignmentSize |
  | --- | --- |
  | 1000ns~1ms | 1ms |
  | 1ms~10ms | 10ms |
  | 10ms~100ms | 100ms |
  | 100ms~1s | 1s |
  | 1s~2s | 2s |
  | 2s~3s | 3s |
  | 3s~5s | 5s |
  | 5s~10s | 10s |
  | 10s~15s | 15s |
  | 15s~20s | 20s |
  | 20s~30s | 30s |
  | >30s | 1min |

假设第一条数据的时间为 x,
那么根据其类型，第一个数据窗口的左边界的计算规则为：`timeType_cast(x/alignmentSize*alignmentSize+step-windowSize)`。其中，timeType\_cast
表示依据时间精度，需要强制转换的时间类型；'/' 表示整除。例如，第一条数据的时间为 2018.10.08T01:01:01.365，windowSize 为
120000，step 为 60000，那么 alignmentSize 为 60000，第一个数据窗口的左边界为
`timestamp(2018.10.08T01:01:01.365/60000*60000+60000-120000)`，即
2018.10.08T01:00:00.000。

## 返回值

一个表对象，通过向该表对象写入，将数据注入时间序列引擎进行计算。

## 例子

注：

以下例子使用了相同的变量和表名便于比较。每个例子执行结束后，请使用以下命令清除环境中的临时数据：

* getStreamingStat：用于查看当前的流数据表订阅者。例如：

  ```
  getStreamingStat().pubTables
  ```
* unsubscribeTable：用于取消订阅流数据表。例如，在例子 1 代码运行后取消对
  trades
  的订阅：

  ```
  unsubscribeTable(tableName="trades", actionName="engine1")
  ```
* dropStreamTable：用于删除流数据表。例如，删除例子 1 中的流数据表
  trades：

  ```
  dropStreamTable(tableName="trades")
  ```
* dropStreamEngine：用于流数据引擎。例如，删除例子 1 中的流数据引擎
  engine1：

  ```
  dropStreamEngine("engine1")
  ```

例1. 时间序列引擎 engine1 订阅流数据表 trades，实时计算表 trades
中过去1分钟内每只股票交易量之和。

```
share streamTable(1000:0, ["time","sym","volume"], [TIMESTAMP, SYMBOL, INT]) as trades
share table(10000:0, ["time","sym","sumVolume"], [TIMESTAMP, SYMBOL, INT]) as output1
engine1 = createTimeSeriesEngine(name="engine1", windowSize=60000, step=60000, metrics=<[sum(volume)]>, dummyTable=trades, outputTable=output1, timeColumn="time", useSystemTime=false, keyColumn="sym", garbageSize=50, useWindowStartTime=false)
subscribeTable(tableName="trades", actionName="engine1", offset=0, handler=append!{engine1}, msgAsTable=true);

insert into trades values(2018.10.08T01:01:01.785,`A,10)
insert into trades values(2018.10.08T01:01:02.125,`B,26)
insert into trades values(2018.10.08T01:01:10.263,`B,14)
insert into trades values(2018.10.08T01:01:12.457,`A,28)
insert into trades values(2018.10.08T01:02:10.789,`A,15)
insert into trades values(2018.10.08T01:02:12.005,`B,9)
insert into trades values(2018.10.08T01:02:30.021,`A,10)
insert into trades values(2018.10.08T01:04:02.236,`A,29)
insert into trades values(2018.10.08T01:04:04.412,`B,32)
insert into trades values(2018.10.08T01:04:05.152,`B,23)

sleep(10)

select * from output1;
```

| time | sym | sumVolume |
| --- | --- | --- |
| 2018.10.08T01:02:00.000 | A | 38 |
| 2018.10.08T01:02:00.000 | B | 40 |
| 2018.10.08T01:03:00.000 | A | 25 |
| 2018.10.08T01:03:00.000 | B | 9 |

下面详细解释时间序列引擎的计算过程。为简便起见，以下提到时间时，省略相同的日期部分，只列出（小时:分钟:秒.毫秒）部分。

首先，时间序列引擎对第一个数据窗口的起始时间进行规整。第一个数据窗口的时间范围是 01:01:00.000 到
01:02:00.000，只包含左边界，不包含右边界。当(01:02:10.789,`A,15)到达时，触发第一个窗口 A
组计算；当(01:02:12.005,`B,9)到达时，触发第一个窗口 B 组计算。

第二个数据窗口的时间范围是 01:02:00.000 到
01:03:00.000。当(01:04:02.236,`A,29)到达时，触发第二个窗口 A
组计算；当(01:04:04.412,`B,32)到达时，触发第二个窗口 B 组计算。

由于 01:05:00.000 及之后没有数据，因此没有对 01:04:00.000 到 01:05:00.000
之间的数据进行计算。

输出表 output1 保存了时间序列引擎的计算结果。由于 *useWindowStartTime* 为
false，因此输出表 output1 中的时间为窗口的结束时间。若将 *useWindowStartTime* 设为
true，则输出表中的时间为窗口的起始时间。例如：

```
output2 = table(10000:0, ["time","sym","sumVolume"], [TIMESTAMP, SYMBOL, INT])
engine2 = createTimeSeriesEngine(name="engine2", windowSize=60000, step=60000, metrics=<[sum(volume)]>, dummyTable=trades, outputTable=output2, timeColumn="time", useSystemTime=false, keyColumn="sym", garbageSize=50, useWindowStartTime=true)
subscribeTable(tableName="trades", actionName="engine2", offset=0, handler=append!{engine2}, msgAsTable=true)

sleep(10)
select * from output2;
```

| time | sym | sumVolume |
| --- | --- | --- |
| 2018.10.08T01:01:00.000 | A | 38 |
| 2018.10.08T01:01:00.000 | B | 40 |
| 2018.10.08T01:02:00.000 | A | 25 |
| 2018.10.08T01:02:00.000 | B | 9 |

下例中指定 *updateTime* 为 1000（毫秒）：

```
share keyedTable(["time","sym"],10000:0, ["time","sym","sumVolume"], [TIMESTAMP, SYMBOL, INT]) as output3
engine3 = createTimeSeriesEngine(name="engine3", windowSize=60000, step=60000, metrics=<[sum(volume)]>, dummyTable=trades, outputTable=output3, timeColumn="time", useSystemTime=false, keyColumn="sym", garbageSize=50, updateTime=1000, useWindowStartTime=false)
subscribeTable(tableName="trades", actionName="engine3", offset=0, handler=append!{engine3}, msgAsTable=true)

sleep(2001)
select * from output3;
```

| time | sym | sumVolume |
| --- | --- | --- |
| 2018.10.08T01:02:00.000 | A | 38 |
| 2018.10.08T01:02:00.000 | B | 40 |
| 2018.10.08T01:03:00.000 | A | 25 |
| 2018.10.08T01:03:00.000 | B | 9 |
| 2018.10.08T01:05:00.000 | B | 55 |
| 2018.10.08T01:05:00.000 | A | 29 |

例2. 下例中指定 *updateTime* 为 0（毫秒）：

```
share streamTable(1000:0, ["time","sym","volume"], [TIMESTAMP, SYMBOL, INT]) as trades
share table(1000:0, ["time","sym","sumVolume"], [TIMESTAMP, SYMBOL, INT]) as output4
engine4 = createTimeSeriesEngine(name="engine4", windowSize=60000, step=60000, metrics=<[sum(volume)]>, dummyTable=trades, outputTable=output4, timeColumn="time", useSystemTime=false, keyColumn="sym", garbageSize=50, updateTime=0, useWindowStartTime=false)
subscribeTable(tableName="trades", actionName="engine4", offset=0, handler=append!{engine4}, msgAsTable=true);

insert into trades values(2018.10.08T01:01:01.785,`A,10)
insert into trades values(2018.10.08T01:01:02.125,`B,26)
insert into trades values(2018.10.08T01:01:10.263,`B,14)
insert into trades values(2018.10.08T01:01:12.457,`A,28)

sleep(100)

insert into trades values(2018.10.08T01:01:12.557,`B,21)
insert into trades values(2018.10.08T01:01:12.557,`A,28)

select * from output4;
```

*updateTime*=0 时，每收到一批数据就触发一次计算输出：

* 01:01:12.457 时，触发了第一批数据中 A、B 两组数据的计算输出。
* 01:01:12.557 时，再次触发第二批数据中 A、B 两组数据的计算输出。

最终得到：

| time | sym | sumVolume |
| --- | --- | --- |
| 2018.10.08 01:02:00.000 | A | 38 |
| 2018.10.08 01:02:00.000 | B | 40 |
| 2018.10.08 01:02:00.000 | B | 61 |
| 2018.10.08 01:02:00.000 | A | 66 |

下面以最后一个数据窗口为例，介绍时间序列引擎指定 *updateTime* 时如何进行计算。假设 time
列时间亦为数据进入时间序列引擎的时刻。

1. 在 01:04:04.236 时，A 分组的第一条记录到达后已经过 2000 毫秒，触发一次 A
   组计算，输出表增加一条记录(01:05:00.000, `A, 29)。
2. 在 01:04:05.152 时的 B 组记录为 01:04:04.412 所在小窗口[01:04:04.000,
   01:04:05.000)之后第一条记录，触发一次 B 组计算，输出表增加一条记录(01:05:00,"B",32)。
3. 2 秒（2\*updateTime个时间单位）后，在 01:04:07.152 时，由于 01:04:05.152
   时的 B 组记录仍未参与计算，触发一次B组计算，输出一条记录(01:05:00,"B",55)。由于输出表的主键为 time 和
   sym，并且输出表中已有(01:05:00,"B",32)这条记录，因此将该记录更新为(01:05:00,"B",55)。

下例中，共享流数据表 "pubT" 包含两个时间列，类型分别时 DATE 和 SECOND，创建时间序列引擎时，通过设置
*timeColumn* 来将原来流数据表的两个时间列整合为输出表 streamMinuteBar\_1min 中的一个类型为 DATETIME
的时间列。

```
colNames=["symbol","date","minute","price","type","volume"]
colTypes=[SYMBOL, DATE, SECOND, DOUBLE, STRING, INT]
pubTable = streamTable(10000:0,colNames,colTypes)
share pubTable as pubT

colNames = ["time","symbol","open","max","min","close","volume","amount","ret","vwap"]
colTypes = [DATETIME, SYMBOL, DOUBLE, DOUBLE, DOUBLE, DOUBLE, INT, DOUBLE, DOUBLE, DOUBLE]
share streamTable(10000:0,colNames, colTypes) as streamMinuteBar_1min

tsAggrOHLC = createTimeSeriesEngine(name="subT", windowSize=60, step=60, metrics=<[first(price) as open ,max(price) as max,min(price) as min ,last(price) as close ,sum(volume) as volume ,wsum(volume, price) as amount ,(last(price)-first(price))/first(price) as ret, (wsum(volume, price)/sum(volume)) as vwap]>, dummyTable=pubTable, outputTable=streamMinuteBar_1min, timeColumn=["date","minute"], useSystemTime=false, keyColumn="symbol", fill="none")
subscribeTable(tableName="pubT", actionName="subT", offset=-1, handler=append!{tsAggrOHLC}, msgAsTable=true)

insert into pubT values("000001", 2021.04.05, 09:25:01, 1, 'B', 1)
insert into pubT values("000001", 2021.04.05, 09:30:05, 2, 'B', 1)
insert into pubT values("000001", 2021.04.05, 09:31:06, 3, 'B', 1)
insert into pubT values("000001", 2021.04.05, 09:35:05, 4, 'S', 4)
insert into pubT values("000001", 2021.04.05, 09:40:05, 5, 'S', 5)
insert into pubT values("000001", 2021.04.06, 09:25:05, 6, 'S', 6)

pubT
```

| symbol | date | minute | price | type | volume |
| --- | --- | --- | --- | --- | --- |
| 000001 | 2021.04.05 | 09:25:01 | 1 | B | 1 |
| 000001 | 2021.04.05 | 09:30:05 | 2 | B | 1 |
| 000001 | 2021.04.05 | 09:31:06 | 3 | B | 1 |
| 000001 | 2021.04.05 | 09:35:05 | 4 | S | 4 |
| 000001 | 2021.04.05 | 09:40:05 | 5 | S | 5 |
| 000001 | 2021.04.06 | 09:25:05 | 6 | S | 6 |

```
select * from streamMinuteBar_1min
```

| time | symbol | open | max | min | close | volume | amount | ret | vwap |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2021.04.05T09:26:00 | 000001 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 1 |
| 2021.04.05T09:31:00 | 000001 | 2 | 2 | 2 | 2 | 1 | 2 | 1 | 2 |
| 2021.04.05T09:32:00 | 000001 | 3 | 3 | 3 | 3 | 1 | 3 | 2 | 3 |
| 2021.04.05T09:36:00 | 000001 | 4 | 4 | 4 | 4 | 4 | 16 | 3 | 4 |
| 2021.04.05T09:41:00 | 000001 | 5 | 5 | 5 | 5 | 5 | 25 | 4 | 5 |

```
share streamTable(1000:0, ["time","sym","qty"], [DATETIME, SYMBOL, INT]) as trades
share table(10000:0, ["time","sym","sumQty"], [DATETIME, SYMBOL, INT]) as output5

engine = createTimeSeriesEngine(name="engine", windowSize=6, step=6, metrics=<sum(qty)>, dummyTable=trades, outputTable=output5, timeColumn="time",keyColumn="sym", forceTriggerTime=7,fill=1000)
subscribeTable(tableName="trades", actionName="engine", offset=0, handler=append!{engine}, msgAsTable=true)
sleep(1000)
insert into engine values(2018.08.01T14:05:43,`A,1)
insert into engine values(2018.08.01T14:05:43,`C,3)
sleep(10)
insert into engine values(2018.08.01T14:05:44,`B,1)
sleep(80)
insert into engine values(2018.08.01T14:05:52,`B,3)
sleep(20)
insert into engine values(2018.08.01T14:05:54,`A,3)
sleep(10)
insert into engine values(2018.08.01T14:05:55,`A,5)
sleep(20)
insert into engine values(2018.08.01T14:05:57,`B,5)
sleep(50)
insert into engine values(2018.08.01T14:06:12,`A,1)
sleep(50)
select * from output5 order by sym
```

| time | sum | Qty |
| --- | --- | --- |
| 2018.08.01T14:05:46 | A | 1 |
| 2018.08.01T14:05:52 | A | 1,000 |
| 2018.08.01T14:05:58 | A | 8 |
| 2018.08.01T14:06:04 | A | 1,000 |
| 2018.08.01T14:06:10 | A | 1,000 |
| 2018.08.01T14:05:46 | B | 1 |
| 2018.08.01T14:05:52 | B | 1,000 |
| 2018.08.01T14:05:58 | B | 8 |
| 2018.08.01T14:05:46 | C | 3 |
| 2018.08.01T14:05:52 | C | 1,000 |

例3. 下例计算每个分组窗口的第一个和最后一个 volume，组合后输出为一个数组向量。

```
//通过 defg 自定义一个函数，引擎在调用该函数时会将返回值转换为数组向量
defg toVector(x){
	return x
}
share streamTable(1000:0, ["time","sym","volume","price"], [TIMESTAMP, SYMBOL, DOUBLE,DOUBLE]) as trades
//定义输出表，对应 toVector 指标输出的列需要定义为数组向量类型，此例中将其定义为 DOUBLE[]
share table(10000:0, ["time","sym","sumVolume","avg"], [TIMESTAMP,STRING,DOUBLE[],DOUBLE]) as output6
//metrics 中调用了 toVector 函数，将1分钟窗口内的第一个 volume 和最后一个 volume 组合到一个向量中。
engine1 = createTimeSeriesEngine(name="engine1", windowSize=60000, step=60000, metrics=<[toVector([first(volume),last(volume)]),avg(volume+price)]>, dummyTable=trades, outputTable=output6, timeColumn="time", keyColumn="sym" , useSystemTime=false, garbageSize=50, useWindowStartTime=false)

times = sort(2023.10.08T00:00:00.000 + rand(1..(1+3000*200), 30))
syms = rand("A"+string(1..10), 30)
volumes = rand(rand(100.0, 10) join 2.3 NULL NULL NULL NULL, 30)
prices = rand(rand(100.0, 10) join 2.3 NULL NULL NULL NULL, 30)
t=table(times as time, syms as sym, volumes as volume,prices as price)

engine1.append!(t)

select * from output6 where time between 2023.10.08T00:01:00.000 and 2023.10.08T00:05:00.000 order by time,sym
```

| time | sym | sumVolume | avg |
| --- | --- | --- | --- |
| 2023.10.08T00:01:00.000 | A1 | [57.66,] | 80.428 |
| 2023.10.08T00:01:00.000 | A2 | [,] |  |
| 2023.10.08T00:02:00.000 | A7 | [,] |  |
| 2023.10.08T00:02:00.000 | A8 | [,] |  |
| 2023.10.08T00:03:00.000 | A2 | [,41.25] | 101.7832 |
| 2023.10.08T00:03:00.000 | A3 | [41.25,41.25] | 68.4897 |
| 2023.10.08T00:03:00.000 | A6 | [,] |  |
| 2023.10.08T00:03:00.000 | A8 | [19.17,19.17] | 93.9934 |
| 2023.10.08T00:04:00.000 | A7 | [,] |  |
| 2023.10.08T00:05:00.000 | A3 | [2.05,2.05] | 95.433 |
| 2023.10.08T00:05:00.000 | A5 | [55.93,55.93] | 116.4669 |
| 2023.10.08T00:05:00.000 | A9 | [42.66,42.66] |  |

例4. 本例将说明 *subWindow* 参数的作用。

```
share streamTable(1000:0, ["time","sym","volume"], [TIMESTAMP, SYMBOL, INT]) as trades
share table(10000:0, ["time","sym","sumVolume"], [TIMESTAMP, SYMBOL, INT]) as output7
//在长度为 1 分钟的窗口内指定一个子窗口，未指定 closed 时，子窗口左闭右开。这里子窗口为每分钟的[0s, 10s)
engine4 = createTimeSeriesEngine(name="engine4", windowSize=60000, step=60000, metrics=<[sum(volume)]>, dummyTable=trades, outputTable=output7, timeColumn="time", useSystemTime=false, keyColumn="sym", garbageSize=50, useWindowStartTime=true, subWindow=0s:10s)

subscribeTable(tableName="trades", actionName="engine4", offset=0, handler=append!{engine4}, msgAsTable=true);

insert into trades values(2018.10.08T01:01:01.785,`A,10)
insert into trades values(2018.10.08T01:01:02.125,`B,26)
insert into trades values(2018.10.08T01:01:10.000,`A,14)
insert into trades values(2018.10.08T01:01:12.457,`A,28)

sleep(10)

select * from output7;
```

2018.10.08T01:01:10.000 时刻的数据触发 [2018.10.08T01:01:00.000, 2018.10.08T01:01:10.000)
区间内 A 组数据对应的 volume 的总和。在子窗口结束后没有再收到 B 组的数据，因此 B 组子窗口内数据未被触发计算。

| time | sym | sumVolume |
| --- | --- | --- |
| 2018.10.08T01:01:10.000 | A | 10 |

例5. 本例展示如何对包含多档价格与数量的数组向量字段，在时间窗口内按股票、买卖方向及委托价格分组，计算各价位的委托金额和委托笔数。

```
share streamTable(1000:0, ["time","sym","side","orderPrice","orderQty"],
    [TIMESTAMP, SYMBOL, SYMBOL, DOUBLE[], INT[]]) as orderStream

share table(10000:0, ["time","sym","side", "orderPrice", "totalValue", "orderCount"],
    [TIMESTAMP, SYMBOL, SYMBOL, DOUBLE, DOUBLE, INT]) as result

// 创建时序聚合引擎：按股票代码、买卖方向和委托价格分组
engine = createTimeSeriesEngine(
    name="orderEngine",
    windowSize=60000,
    step=60000,
    metrics=<[
        sum(orderPrice * orderQty),
        count(orderPrice)
    ]>,
    dummyTable=orderStream,
    outputTable=result,
    timeColumn="time",
    keyColumn=`sym`side`orderPrice,
    useSystemTime=false
)

n = 100
time = 2023.01.01T09:30:00.000 + (1..n)*1000
sym = take(`AAPL`MSFT, n)
side = take(`Buy`Sell, n)
orderPrice = arrayVector((1..n) * 5, rand(100.0 105.0, 5*n))
orderQty = arrayVector((1..n) * 5, rand(100 1000, 5*n))

insert into engine values(time, sym, side, orderPrice, orderQty)

// 查看结果表
select * from result
```

| time | sym | side | orderPrice | totalValue | orderCount |
| --- | --- | --- | --- | --- | --- |
| 2023.01.01 09:31:00.000 | AAPL | Buy | 100 | 4,430,000 | 74 |
| 2023.01.01 09:31:00.000 | AAPL | Buy | 105 | 5,050,500 | 76 |
| 2023.01.01 09:31:00.000 | MSFT | Sell | 100 | 4,720,000 | 76 |
| 2023.01.01 09:31:00.000 | MSFT | Sell | 105 | 3,654,000 | 69 |

例6. 将 *windowSize* 设为向量，同时计算 1 分钟窗口和 3 分钟窗口。

当 *windowSize* 为向量时，每个窗口长度可以对应一组独立的指标。本例同时输出 1 分钟成交量之和和 3 分钟价格均值。

```
share streamTable(1000:0, ["time","sym","volume","price"], [TIMESTAMP, SYMBOL, INT, DOUBLE]) as tradesWS
share table(1000:0, ["time","sym","sum1m","avgPrice3m"], [TIMESTAMP, SYMBOL, INT, DOUBLE]) as outputWS

engineWS = createTimeSeriesEngine(
  name="engineWS",
  windowSize=[60000, 180000],
  step=60000,
  metrics=(<[sum(volume) as sum1m]>, <[avg(price) as avgPrice3m]>),
  dummyTable=tradesWS,
  outputTable=outputWS,
  timeColumn="time",
  keyColumn="sym",
  useSystemTime=false
)

subscribeTable(tableName="tradesWS", actionName="engineWS", offset=0, handler=append!{engineWS}, msgAsTable=true)

insert into tradesWS values(2024.01.01T10:00:10.000, `A, 10, 100.0)
insert into tradesWS values(2024.01.01T10:00:20.000, `B, 16, 104.0)
insert into tradesWS values(2024.01.01T10:00:40.000, `A, 20, 101.0)
insert into tradesWS values(2024.01.01T10:01:10.000, `A, 15, 102.0)
insert into tradesWS values(2024.01.01T10:01:20.000, `B, 20, 105.0)
insert into tradesWS values(2024.01.01T10:02:05.000, `A, 30, 103.0)
insert into tradesWS values(2024.01.01T10:03:10.000, `A, 12, 104.0)

sleep(10)
select * from outputWS
```

输出如下：

| time | sym | sum1m | avgPrice3m |
| --- | --- | --- | --- |
| 2024.01.01 10:01:00.000 | A | 30 | 100.5 |
| 2024.01.01 10:01:00.000 | B | 16 | 104 |
| 2024.01.01 10:02:00.000 | A | 15 | 101 |
| 2024.01.01 10:03:00.000 | A | 30 | 101.5 |

其中：

* `windowSize=[60000, 180000]` 分别对应 1 分钟和 3 分钟窗口。
* *metrics* 的第一个元素对应 1 分钟窗口，第二个元素对应 3 分钟窗口。
* 输出表中两个结果列分别保存不同窗口长度下的聚合结果。

例7. 设置 *roundTime* 和 *step* 控制窗口的规整方式。

当时间精度为毫秒或秒，且 *step* 大于 1 分钟时，*roundTime* 会影响首个窗口边界的规整结果。本例使用两个参数相同、仅
*roundTime* 不同的引擎进行对比。

```
share streamTable(1000:0, ["time","volume"], [TIMESTAMP, INT]) as tradesRT
share table(1000:0, ["time","sumVolume"], [TIMESTAMP, INT]) as outputRTTrue
share table(1000:0, ["time","sumVolume"], [TIMESTAMP, INT]) as outputRTFalse

engineRTTrue = createTimeSeriesEngine(
   name="engineRTTrue",
   windowSize=240000,
   step=120000,
   metrics=<[sum(volume) as sumVolume]>,
   dummyTable=tradesRT,
   outputTable=outputRTTrue,
   timeColumn="time",
   useSystemTime=false,
   roundTime=true
)

engineRTFalse = createTimeSeriesEngine(
   name="engineRTFalse",
   windowSize=240000,
   step=120000,
   metrics=<[sum(volume) as sumVolume]>,
   dummyTable=tradesRT,
   outputTable=outputRTFalse,
   timeColumn="time",
   useSystemTime=false,
   roundTime=false
)

subscribeTable(tableName="tradesRT", actionName="engineRTTrue", offset=0, handler=append!{engineRTTrue}, msgAsTable=true)
subscribeTable(tableName="tradesRT", actionName="engineRTFalse", offset=0, handler=append!{engineRTFalse}, msgAsTable=true)

insert into tradesRT values(2024.01.01T10:03:30.500, 10)
insert into tradesRT values(2024.01.01T10:04:20.000, 20)
insert into tradesRT values(2024.01.01T10:06:01.000, 5)
```

对于 *roundTime*=true 的引擎，执行 `select * from outputRTTrue`，输出如下：

| time | sumVolume |
| --- | --- |
| 2024.01.01 10:04:00.000 | 10 |
| 2024.01.01 10:06:00.000 | 30 |

对于 *roundTime*=false 的引擎，执行 `select * from
outputRTFalse`，输出如下：

| time | sumVolume |
| --- | --- |
| 2024.01.01 10:05:00.000 | 30 |

* 本例中第一条数据时间为 `x=2024.01.01T10:03:30.500`；*windowSize* 为
  240000（4 分钟）。
* 当 *roundTime*=true 时，*step*=120000 属于毫秒精度下的 60001~120000 区间，对应的
  alignmentSize 为 120000（2 分钟）。先将 x 按 2
  分钟规整：`timestamp(x/120000*120000)=2024.01.01T10:02:00.000`；再代入公式得到左边界
  `2024.01.01T10:02:00.000 + 120000 - 240000 =
  2024.01.01T10:00:00.000`，所以首个窗口为 [10:00:00.000,
  10:04:00.000)。
* 当 *roundTime*=false 时，数据为毫秒精度且 *step*>30000，对应的 alignmentSize 为
  60000（1 分钟）。先将 x 按 1
  分钟规整：`timestamp(x/60000*60000)=2024.01.01T10:03:00.000`；再代入公式得到左边界
  `2024.01.01T10:03:00.000 + 120000 - 240000 =
  2024.01.01T10:01:00.000`，所以首个窗口为 [10:01:00.000,
  10:05:00.000)。
* 10:03:30.500 这条记录在两种设置下都落入首个窗口，但首个窗口的起止范围不同；进一步地，10:04:20.000 在
  *roundTime*=true 时落入下一个窗口 [10:02, 10:06)，而在 *roundTime*=false
  时仍落入首个窗口 [10:01, 10:05)。

例8. 设置 *closed* 控制边界点归属

*closed*='left' 表示左闭右开，*closed*='right'
表示左开右闭。若数据恰好落在窗口边界上，不同设置会影响该数据属于哪个窗口。

```
share streamTable(1000:0, ["time","volume"], [TIMESTAMP, INT]) as tradesCL
share table(1000:0, ["time","sumVolume"], [TIMESTAMP, INT]) as outputLeft
share table(1000:0, ["time","sumVolume"], [TIMESTAMP, INT]) as outputRight

engineLeft = createTimeSeriesEngine(
   name="engineLeft",
   windowSize=60000,
   step=60000,
   metrics=<[sum(volume) as sumVolume]>,
   dummyTable=tradesCL,
   outputTable=outputLeft,
   timeColumn="time",
   useSystemTime=false,
   closed="left"
)

engineRight = createTimeSeriesEngine(
   name="engineRight",
   windowSize=60000,
   step=60000,
   metrics=<[sum(volume) as sumVolume]>,
   dummyTable=tradesCL,
   outputTable=outputRight,
   timeColumn="time",
   useSystemTime=false,
   closed="right"
)

subscribeTable(tableName="tradesCL", actionName="engineLeft", offset=0, handler=append!{engineLeft}, msgAsTable=true)
subscribeTable(tableName="tradesCL", actionName="engineRight", offset=0, handler=append!{engineRight}, msgAsTable=true)

insert into tradesCL values(2024.01.01T10:00:10.000, 10)
insert into tradesCL values(2024.01.01T10:01:00.000, 20)
insert into tradesCL values(2024.01.01T10:01:10.000, 1)
```

对于 *closed*="left" 的引擎， 执行 `select * from outputLeft`，输出如下：

| time | sumVolume |
| --- | --- |
| 2024.01.01 10:01:00.000 | 10 |

对于 *closed*="right" 的引擎，执行 `select * from outputRight`，输出如下

| time | sumVolume |
| --- | --- |
| 2024.01.01 10:01:00.000 | 30 |

* *closed*="left" 时，第 2 条记录的时间正好是 10:01:00.000，属于下一个窗口 [10:01,
  10:02)，因此第一个窗口只统计到 10。
* *closed*="right" 时，同一条边界数据属于前一个窗口 (10:00, 10:01]，因此第一个窗口统计结果变为
  `10 + 20 = 30`。

例9. 设置 *outputElapsedMicroseconds* 与 *acceptedDelay*

* 通过 *acceptedDelay* 接收窗口结束后一定范围内到达的乱序数据；
* 通过 *outputElapsedMicroseconds*=true 输出每个结果从触发计算到写出结果的耗时。

```
share streamTable(1000:0, ["time","sym","volume"], [TIMESTAMP, SYMBOL, INT]) as tradesAD
share table(1000:0, ["time","sym","elapsedUs","sumVolume"], [TIMESTAMP, SYMBOL, LONG, INT]) as outputAD

engineAD = createTimeSeriesEngine(
   name="engineAD",
   windowSize=60000,
   step=60000,
   metrics=<[sum(volume) as sumVolume]>,
   dummyTable=tradesAD,
   outputTable=outputAD,
   timeColumn="time",
   keyColumn="sym",
   useSystemTime=false,
   acceptedDelay=5000,
   outputElapsedMicroseconds=true
)

subscribeTable(tableName="tradesAD", actionName="engineAD", offset=0, handler=append!{engineAD}, msgAsTable=true)

insert into tradesAD values(2024.01.01T10:00:10.000, `A, 10)
insert into tradesAD values(2024.01.01T10:00:40.000, `A, 20)
insert into tradesAD values(2024.01.01T10:01:02.000, `A, 1)
insert into tradesAD values(2024.01.01T10:00:55.000, `A, 30)
insert into tradesAD values(2024.01.01T10:01:06.000, `A, 2)

sleep(10)
select * from outputAD
```

输出如下：

| time | sym | elapsedUs | sumVolume |
| --- | --- | --- | --- |
| 2024.01.01 10:01:00.000 | A | 2 | 60 |

* 本例中窗口为 [10:00:00, 10:01:00)。
* 当 *acceptedDelay*=5000 时，窗口在结束后的 5 秒内仍可接收迟到数据。
* 第 4 条记录 10:00:55.000 虽然晚于 10:01:02.000 到达，但仍在允许延迟范围内，因此仍计入第一个窗口。
* 第 5 条记录时间为 10:01:06.000，满足“收到时间戳大于等于当前窗口结束的时间戳 + acceptedDelay
  的数据”这一条件，因此触发第一个窗口输出，结果为 10 + 20 + 30 = 60。

例10. 设置 outputHandler 与 msgAsTable

设置 *outputHandler* 后，引擎计算结果不会写入 outputTable，而是调用定义的一元函数处理计算结果。*msgAsTable*
用于控制回调参数的结构：

* *msgAsTable*=false：回调参数是由各列组成的元组；
* *msgAsTable*=true：回调参数是一个表。

```
share streamTable(1000:0, ["time","volume"], [TIMESTAMP, INT]) as tradesOH
share table(1000:0, ["time","sumVolume"], [TIMESTAMP, INT]) as ignoredTuple
share table(1000:0, ["time","sumVolume"], [TIMESTAMP, INT]) as ignoredTable
share table(1000:0, ["time","sumVolume"], [TIMESTAMP, INT]) as tupleResult
share table(1000:0, ["time","sumVolume"], [TIMESTAMP, INT]) as tableResult

def handleTuple(msg){
   tupleResult.tableInsert(msg[0],msg[1])
}

def handleTable(msg){
   tableResult.append!(msg)
}

engineTuple = createTimeSeriesEngine(
   name="engineTuple",
   windowSize=60000,
   step=60000,
   metrics=<[sum(volume) as sumVolume]>,
   dummyTable=tradesOH,
   outputTable=ignoredTuple,
   timeColumn="time",
   useSystemTime=false,
   outputHandler=handleTuple,
   msgAsTable=false
)

engineTable = createTimeSeriesEngine(
   name="engineTable",
   windowSize=60000,
   step=60000,
   metrics=<[sum(volume) as sumVolume]>,
   dummyTable=tradesOH,
   outputTable=ignoredTable,
   timeColumn="time",
   useSystemTime=false,
   outputHandler=handleTable,
   msgAsTable=true
)

subscribeTable(tableName="tradesOH", actionName="engineTuple", offset=0, handler=append!{engineTuple}, msgAsTable=true)
subscribeTable(tableName="tradesOH", actionName="engineTable", offset=0, handler=append!{engineTable}, msgAsTable=true)

insert into tradesOH values(2024.01.01T10:00:10.000, 10)
insert into tradesOH values(2024.01.01T10:00:40.000, 20)
insert into tradesOH values(2024.01.01T10:01:10.000, 5)
```

分别执行 `select * from tupleResult` 和 `select * from
tableResult`。

tupleResult 和 tableResult 的结果都为：

| time | sumVolume |
| --- | --- |
| 2024.01.01 10:01:00.000 | 30 |

* engineTuple 中，`handleTuple` 接收到的是列元组，一元函数中使用
  `tableInsert` 将 `msg[0]` 和
  `msg[1]` 插入到目标表。
* engineTable 中，`handleTable` 直接接收到结果表，一元函数中使用
  `append!` 将结果表插入到目标表。

分别执行 `select * from ignoredTuple` 和 `select * from
ignoredTable`，输出结果均为空。这是因为设置了 *outputHandler*，计算结果不会写入 ignoredTuple
和 ignoredTable。

**相关信息**

* [createDailyTimeSeriesEngine](createDailyTimeSeriesEngine.html "createDailyTimeSeriesEngine")
