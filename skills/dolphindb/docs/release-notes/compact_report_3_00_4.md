<!-- Auto-mirrored from upstream `documentation-main/rn/compact_report_3_00_4.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 3.00.4

## 涉及保持一致性或兼容行业惯例的修改

* 对 FICC 系列函数（
  `bondAccrInt`、`bondCashflow`、`bondConvexity`、`bondDirtyPrice`、`bondDuration`、`bondYield`
  ）的参数结构进行了调整，部分参数名已修改，接口更为统一，功能更强大。原有参数结构将不再兼容，请根据新接口进行适配。此外，*dayCountConvention*
  参数中原先的规则 "ActualActual" 已调整为 "ActualActualISMA"。
* 在 SELECT 中给 GROUP BY 列使用别名（例如 id as id1）的行为发生变化：旧版本允许执行，新版本会报错，必须在 GROUP BY
  子句中定义别名。

  ```
  t = table(10:0, [`id,`sym,`flag, `val], [INT, SYMBOL, BOOL, DOUBLE])
  insert into t values(1, `a, true, 1.0)
  select id as id1,sum(val) from t group by id
  // 老版本可以执行，返回
  id id1 sum_val
  -- --- -------
  1  1   1
  // 当前版本会报错：Alias for a GROUP BY field should be defined in the GROUP BY clause, not in the SELECT clause. Please use 'select ... group by x as y' instead of 'select x as y ... group by x'.
  ```
* 将矩阵转换为表时，自动生成列名的规则发生了变化：旧版本生成的列名前缀固定为
  “col”，不显示矩阵变量名；新版本的列名前缀改为使用矩阵变量名。

  ```
  m = rand(100, 4)$2:2
  t = table(m)
  t.colNames()
  // 老版本返回：["col0","col1"]
  // 当前返回：["m0","m1"]
  ```
* 通过 `toJson` 转换矩阵时，输出 JSON 中的 name 字段行为发生变化。旧版本 name
  字段为空，新版本会显示矩阵变量名。

  ```
  b = matrix(1 6 2, 3 4 5);
  re = toJson(b);
  re
  // 老版本返回：{"name":"matrix","form":"matrix","type":"int","size":"3","value":[{"name":"","form":"vector","type":"int","size":"6","value":[1,6,2,3,4,5]},{"name":"row","form":"scalar","type":"int","value":"3"},{"name":"col","form":"scalar","type":"int","value":"2"},{"name":"","form":"scalar","type":"void","value":""},{"name":"","form":"scalar","type":"void","value":""}]}
  // 当前返回：{"name":"matrix","form":"matrix","type":"int","size":"3","value":[{"name":"b","form":"vector","type":"int","size":"6","value":[1,6,2,3,4,5]},{"name":"row","form":"scalar","type":"int","value":"3"},{"name":"col","form":"scalar","type":"int","value":"2"},{"name":"","form":"scalar","type":"void","value":""},{"name":"","form":"scalar","type":"void","value":""}]}
  ```
* `string`、`symbol`、`blob` 对
  table、tuple、dictionary
  等数据结构的输入行为发生变化。旧版本返回标量或向量，新版本返回与输入数据结构一致的对象，且对象内部元素类型相应转换为字符串。

  ```
  t = table(1..10 as id)
  re = string(t)
  typestr(re)
  // 老版本返回：STRING
  // 当前返回：IN-MEMORY TABLE，返回结果中的每一列转换为string类型
  re = string([])
  typestr(re)
  // 老版本返回：STRING VECTOR
  // 当前返回：ANY VECTOR
  ```
* `string` 函数不再支持输入数组向量。旧版本可以执行，新版本会报错。可使用 `snippet`
  或 `brief`
  函数作为替代。

  ```
  a = array(INT[],0).append!([[],[NULL,3],[34,2]])
  string(a)

  // 老版本可以正常执行
  // 当前版本报错：The base type of an array vector can't be STRING.
  // 当前版本使用 snippet 可以执行
  ```
* `all` 和 `any` 函数对不同形式的入参，计算行为发生变化
  + 入参为元组、字典时，将按行计算。
  + 入参为矩阵、表时将按列计算。

    ```
    value=(1 2 3, 0 2 3)
    all(value)
    // 老版本：false
    // 新版本：false true true

    value=1 2 3 0 1 2$2:3
    all(value)
    // 老版本：false
    // 新版本：true fasle true

    value=dict(1 2, [1 2 3, 0 1 2])
    all(value)
    // 老版本：报错The object can't be converted to boolean scalar.
    // 新版本：false true true

    value=table(1 2 as x, 0 1 as y)
    all(value)
    // 老版本：The object can't be converted to boolean scalar.
    // 新版本：true fasle

    value=(0 2 1, 0 0 0)
    any(value)
    // 老版本：false
    // 新版本：false true true

    value=0 0 3 0 1 2$2:3
    any(value)
    // 老版本：true
    // 新版本：false true true

    value=dict(1 2, [0 2 3, 0 0 0])
    any(value)
    // 老版本：报错The object can't be converted to boolean scalar.
    // 新版本：false true true

    value=table(1 2 as x, 0 0 as y)
    any(value)
    // 老版本：The object can't be converted to boolean scalar.
    // 新版本：true fasle
    ```
* `objectComponent` 函数的入参是二元运算表达式时，返回值的字段发生变化。旧版本返回 optrs 和 objs
  字段，新版本返回 left、operator 和 right
  字段。

  ```
  objectComponent(<1+2>)
  // 旧版本：
  optrs->(+)
  objs->(1,2)
  // 新版本：
  left->< 1 >
  operator->+
  right->< 2 >
  ```
* `unifiedExpr` 函数的参数数量上限从未限制变为 1024。旧版本允许任意长度表达式，新版本当参数超过 1024
  时将报错。

  ```
  n = 2000
  a = rand(100, n)
  x = array(ANY, 0, size(a))
  for(i in 0..(size(a)-1)){
  	x.append!(expr(a[i], *, 0.1))
  }
  funcs = take(sub, (size(a)-1))
  re = unifiedExpr(x, funcs)
  // 旧版本可以正常执行
  // 新版本报错：The number of objects in an expression cannot exceed 1024.
  ```
* 系统生成的表达式在字符串化时可能会增加括号。旧版本返回 `{def (x, y)->x * x + y * y}`，新版本返回
  `{def (x, y)->(x * x) + (y *
  y)}`。该变更仅涉及显示格式，语义不变。

  ```
  re2 = {x, y ->x*x + y*y}
  string(re2)
  // 旧版本返回 {def (x, y)->x * x + y * y}
  // 新版本返回 {def (x, y)->(x * x) + (y * y)}
  ```
* Orca API
  `StreamGraph::source`、`StreamGraph::haSource`、`StreamGraph::keyedSource`、`StreamGraph::haKeyedSource`、`StreamGraph::latestKeyedSource`
  移除了 *capacity:size* 参数。新版本默认使用 1:0。
* 运维函数 `getOrcaCheckpointJobInfo` 返回值新增了一列（partitionId）。
* `dropStreamGraph` 的删除行为发生变化：旧版本会同时删除引用计数为 0 的流表，新版本默认不会删除，需显式指定参数
  `includTables=true`。
* Shark 版本的 server 在新版本中要求在配置文件中显式指定
  `dolphinModulePath=libskgraph.so,libshark.so`才能使用。单节点配置文件：dolphindb.cfg，集群环境配置文件：cluster.cfg。

## 缺陷修复带来的系统影响

* 当以下函数的入参为 DECIMAL 类型的矩阵时，返回值形式由向量变为矩阵：`iif`,
  `max`, `min`, `maxIgnoreNull`,
  `minIgnoreNull`。

  ```
  x = 1..10 $2:5 $DECIMAL32(3)
  y = 10..1 $2:5 $DECIMAL32(3)
  z=iif(x>5, y, x)
  typestr(z)
  // 老版本返回：FAST DECIMAL32 VECTOR
  // 当前返回：FAST DECIMAL32 MATRIX
  re = max(x, y)
  typestr(re)
  // 老版本返回：FAST DECIMAL32 VECTOR
  // 当前返回：FAST DECIMAL32 MATRIX
  ```
* 时间类型与 NULL 的计算结果的数据类型发生变化。旧版本返回整型，新版本返回时间类型。
* `iif` 函数要求 *trueResult* 与 *falseResult*
  数据类型一致。旧版本允许不同类型混用，新版本将报错。
* 键值内存表和索引内存表的主键列（*keyColumns*）不再参与计算。

  ```
  t = indexedTable(`id, 1..10 as id, 11..20 as val)
  stretch(t,20)
  // 老版本可正常执行
  // 当前返回：All columns must be of the same length.
  n = 5
  id = 1..10
  val = 11..20
  t = indexedTable(`id, id as id, val as val)
  re = moving(sum, t, n, 1)
  re
  // 老版本返回：
  id val
  -- ---
  1  11
  3  23
  6  36
  10 50
  15 65
  20 70
  25 75
  30 80
  35 85
  40 90
  // 当前返回：
  id val
  -- ---
  1  11
  2  23
  3  36
  4  50
  5  65
  6  70
  7  75
  8  80
  9  85
  10 90
  ```
* `med` 计算表中的 ANY 类型列的行为发生变化。旧版本允许执行，但结果全为 NULL；新版本将根据配置项
  *processVectorFunctionOverTupleByRow* 决定按行或按列计算，返回的结果为向量。需要注意，在 SQL
  中直接使用该函数会报错。如需返回向量，可在外层封装
  `toArray`。

  ```
  n = 50
  num = 30
  cid = rand(1..20, n+1)
  cshort = cut(take(short(-100..100 join NULL), n*num), num) join short(1..num)
  t = table(cid, cshort)
  re = select med(cshort) from t group by cid
  // 老版本可以正常执行，但返回的 med_cshort 是 NULL
  // 当前版本会报错：The column 'med(cshort)' must use aggregate function. RefId: S02022.
  // 可以封装 toArray，获得计算结果。
  re = select toArray(med(cshort)) from t group by cid
  ```
* 字典和元组的计算行为发生变化。旧版本可能按列计算或报错，新版本统一按行计算，并在类型不确定或不支持时报错。但对于向量函数，可通过配置项
  *processVectorFunctionOverTupleByRow*
  设置计算按列还是按行计算。此外，不再允许对字典或元组使用原地修改函数。**字典计算行为**

  ```
  value =(-2 2 3, 0 1 2 ,2.2 -3 1)
  a = dict(1 2 3, value, true)
  cumsum(a)
  //老版本按列计算: dict(1 2 3, each(cumsum, value))
  //新版本按行计算：dict(1 2 3, each(cumsum, value.double().transpose()).transpose().flatten().cut(3))
  msum(a,2)
  //老版本按列计算:  dict(1 2 3, each(msum{,2}, value))
  //新版本按行计算：dict(1 2 3, each(msum{,2}, value.double().transpose()).transpose().flatten().cut(3))
  wsum(a,a)
  //老版本报错：Usage: wsum(X, Y). X must be a vector, matrix, scalar, or table.
  //新版本按行返回结果： each(wsum, value.double().transpose(), value.double().transpose())

  d = {-1:NULL,0:NULL,"c":NULL,"long":NULL}
  d = dict(d.keys(),d.values(),true)
  re = cumstdp(d)
  //老版本可以计算
  //新版本报错：When a tuple is the input, the elements of the tuple must be scalars or regular vectors with identical length.
  ```

  **元组计算行为**

  ```
  value =(-2 2 3, 0 1 2 ,2.2 -3 1)
  sum(value)
  //新老版本一致，each(sum, value.transpose())
  cumsum(value)
  //老版本按列计算: each(cumsum, value)
  //新版本按行计算：each(cumsum, value.double().transpose()).transpose().flatten().cut(3)
  msum(value,2)
  //老版本按列计算: each(msum{,2}, value)
  //新版本按行计算：each(msum{,2}, value.double().transpose()).transpose().flatten().cut(3)
  wsum(value,value)
  //老版本报错：X and Y must be numeric.
  //新版本按行计算：each(wsum, value.double().transpose(), value.double().transpose())

  re = cumstdp((NULL, 1, 1))
  //老版本可以计算
  //新版本报错：When a tuple is the input, the elements of the tuple must be scalars or regular vectors with identical length.

  元组现在不允许使用原地修改函数修改：
  a = array(any,0,3).append!(00F).append!(00f).append!(00i)
  nullFill!(a, 3)
  //老版本可以正常执行
  //新版本报错 Can't apply a in-place function to a dictionary or tuple of vectors.
  //新版本设置配置项后可以正常执行 processVectorFunctionOverTupleByRow = false
  ```
* 高可用流表不再允许执行 `undef` 操作。旧版本允许
  `undef`，新版本会抛出异常。

  ```
  colNames = `ctime`sym`qty`price;
  colTypes = [TIMESTAMP,SYMBOL,INT,DOUBLE];
  t = table(1:0,colNames,colTypes);
  haStreamTable(11, t,`trades_undef,100000);
  go
  data = table(take(now(), 1000) as ctime, take(`A`B`C`D, 1000) as sym, 1..1000 as qty, take(11.9 33.4, 1000) as price);
  trades_undef.append!(data);
  undef(`trades_undef, SHARED)
  // 旧版本可以执行
  // 当前版本抛异常
  ```
* `loadText` 函数的解析行为发生变化，输入空布尔值时，旧版本会解析为 true，新版本解析为 NULL。
* `enlist` 函数在处理 key 为字符串的字典时的行为发生变化。旧版本返回包含原字典的
  tuple，新版本返回一行的表格。

  ```
  ans = enlist(dict(`a`b`c, (1, 2 3, 4)))
  // 老版本返回一个包含原字典的 tuple：
  // ans 为只有一个元素的 tuple, ans[0] 为原字典
  // 新版本返回一行 table:
  c b     a
  - ----- -
  4 [2,3] 1
  ```
* `flatten` 函数在字典上的行为发生变化。之前的版本中，对字典调用 `flatten`
  会直接返回字典本身；在新版本中，将对字典的值执行
  `flatten`。

  ```
  d = {-1:-1,0:0,"c":1,"short":5h,"int":3,"long":5l,"double":1.32,"float":2.2f}
  re = flatten(d)

  老版本：返回原字典
  新版本：报错 Couldn't flatten the vector because some elements of the vector have inconsistent types.

  d = {-1:-1,0:0}
  re = flatten(d)
  // 新版本返回 -1 0
  ```
