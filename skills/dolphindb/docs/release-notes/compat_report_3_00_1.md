<!-- Auto-mirrored from upstream `documentation-main/rn/compat_report_3_00_1.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 3.00.1

## 3.00.1.0

### 影响存储或版本回退的修改

* 在当前版本中，由于 SQL DELETE 和 INSERT INTO 语句的持久化协议发生变化，在函数视图或定时作业等需要持久化函数的功能中使用
  DELETE 或 INSERT INTO 后，将不能回退至之前版本。
* 在当前版本中，新增了定时任务或某次增删定时任务触发了 checkPoint（sysmgmt 目录下会生成
  jobCheckPoint.meta），将不能回退至之前版本。
* 在当前版本中，在主键引擎数据库中创建了表，将不能回退至之前版本。
* 在当前版本中，在 OLAP，TSDB，PKEY 存储引擎中使用了新的压缩算法
  chimp，将不能回退至之前版本。
* 在当前版本中，TSDB 数据库中创建了使用了向量索引的表，将不能回退至之前版本。
* 在当前版本中，触发过 3 级 Level File 合并，将不能回退至之前版本。

### 缺陷修复带来的系统影响

* `restore` 函数的*snapshot* 参数的默认值发生变化。

  + 在之前版本中，*snapshot* 的默认值为
    true。这导致在进行非首次恢复时可能导致数据库中未在备份中的数据被删除。
  + 在当前版本中，*snapshot* 的默认值修改为 false，以防止误删数据。

注：

如果需要兼容旧版本的行为，需要显式地指定 `restore` 的
*snapshot* 参数为 true。

* 将 bigarray 的 subarray 进行类型转换时，返回的类型结果发生变化：

  + 在之前的版本中，返回 FAST <DATATYPE> VECTOR。
  + 在当前版本中，返回 HUGE <DATATYPE> VECTOR。

  ```
  x=bigarray(INT,10,10000000,1)
  subx=subarray(x, 0:5000)
  // 进行类型转换后查看类型
  typestr(char(subx))
  // 之前版本：FAST CHAR VECTOR
  // 当前及之后版本：HUGE CHAR VECTOR
  ```
* `std`, `stdp`, `var`,
  `varp`, `skew`,
  `kurtosis`（原始函数以及 m\* 系列，tm\* 系列）在以下某种情况中计算结果的精度可能发生变化：
  + 数据为极小值、数据为极大值、数据变化幅度为极小值、数据变化幅度为极大值。
* 如果 `flatten` 的输入值为元组类型，其处理逻辑发生变化。

  + 在之前版本中，将元组转为一维向量。
  + 在当前版本中，会把值为元组的元素先转化为一维向量，返回的结果仍然是一个元组。

  ```
  list2 = (("aa", "bb", "cc"), ("dd", "ee", "ff"))
  flatten(list2)
  //之前版本返回string vector:[`aa,`bb,`cc,`dd,`ee,`ff]
  //现在及之后版本返回any vector：(["aa", "bb", "cc"], ["dd", "ee", "ff"])

  //可以通过多次flatten的方法来兼容旧版本的行为：
  flatten(flatten(list))
  //当前版本返回string vector， [`aa`bb`cc`dd`ee`ff]
  ```
* 对于自定义 JIT 函数，当返回为多个标量时，返回的数据形式发生变化：

  + 在之前版本中，返回向量。
  + 在当前版本中，返回元组。

  ```
  @jit
  def f(a, b, c){
      return a, b, c
  }

  a = 1
  b = -1
  c = int(NULL)

  typestr(f(a, b, c))
  // 在之前版本中，返回 FAST INT VECTOR
  // 在当前版本中，返回 ANY VECTOR
  ```

  在新版本中，可通过显式转换数据类型实现旧版本行为：

  ```
  res = cast(f(a, b, c),INT)
  typestr(res) //output: FAST INT VECTOR
  ```

## 3.00.1.3

### 缺陷修复带来的系统影响

* 函数 `getUserAccess`和 `getGroupAccess`
  的返回结果表中，\*\_allowed 和 \*\_denied 字段类型发生变化：

  + 在之前版本中，\*\_allowed 和 \*\_denied 字段类型为 STRING。
  + 在当前版本中，\*\_allowed 和 \*\_denied 字段类型为 BLOB。
* `flatten` 函数处理包含 NULL 值、包含常规类型元和嵌套元组的元组的逻辑发生改变。

  + 检查元素类型时，取消对 NULL 值的限制。

    ```
    flatten((3, NULL, 5))
    // 之前版本报错：Couldn't flatten the vector because some elements of the vector have inconsistent types.'
    // 当前版本返回：[3,,5]
    ```
  + 允许展开混合了常规类型和嵌套元组的元组。

    ```
    flatten([(1, "aa"), 2.5, 3])
    // 之前版本报错：Couldn't flatten the vector because some elements of the vector have inconsistent types.'
    // 当前版本返回：[1，aa,2.5,3]
    ```
* 当 wsum, wavg 等聚合函数的输入参数为一个标量和一个空数组时，结果发生变化：

  + 在之前版本中，返回错误结果。
  + 在当前版本中，返回空值。

    ```
    wsum(1, array(int, 0, 1))
    // 之前版本返回错误结果：111,023,352
    // 当前版本返回空值
    ```
