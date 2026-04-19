<!-- Auto-mirrored from upstream `documentation-main/tutorials/module_testing_guide.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 模块测试指南

第三方模块的测试文件应包含测试要点文档和回归测试代码：

* 测试要点文档：针对模块功能特点，具体描述测试要点。后续测试脚本应覆盖所有要点。
* 回归测试代码：DolphinDB 测试脚本。验证第三方模块时，DolphinDB 会执行回归测试，所有用例必须通过。

## 测试用例编写规范

1. 1.【强制】一个正向的合法测试用例声明格式为：`@testing: case =
   “testName”`，测试用例中断言需要使用 assert 语句。

   正例：

   ```
   @testing:case="test_sum_int_vetcor" re = sum([1,2,3])
                 assert
               1,eqObj(re,6)
   ```
2. 【强制】一个异常测试用例声明格式为：@testing: case = “testName”, exception=1。

   正例：

   ```
   @testing:case="sum_not_support_matrix_zero_column", exception=1
                 m = matrix(`INT, 10, 0);
                 sum(m)
   ```
3. 【强制】由于解析错误抛出的异常，异常测试用例声明格式为：@testing: case = “testName”, syntaxError=1。

   正例：

   ```
   @testing:case="parse_constant_vector_void_type", syntaxError=1
                 {,}
   ```
4. 【推荐】同一测试用例中多个结果比较时，每个比较对应一个断言，断言编号不能重复。否则某断言失败时，无法定位具体断言。

   正例：

   ```
   @testing:case="test_sum_int_vetcor" re = sum([1,2,3])
                 assert 1,eqObj(re,6)
                 re = sum([1]) assert
               2,eqObj(re,1)
   ```

   反例：

   ```
   @testing:case="test_sum_int_vetcor" re = sum([1,2,3])
                 assert 1,eqObj(re,6)
                 re = sum([1]) assert
               1,eqObj(re,1)
   ```
5. 【推荐】测试用例名不要重复，否则难以根据结果定位失败用例。
6. 【推荐】比较实际结果和预期是否完全一致时，推荐使用`eqObj`函数，避免直接使用`==` 或
   `eq`函数。因为`eqObj`只有当类型和值都相同时，函数才会返回 true。
   如果值相同但类型不同，则此函数仍返回 false。
7. 【推荐】断言时，如果要比较两个表的结果是否一致，推荐使用each(eqObj,
   re.values(),ex.values())的比较方式，避使用eqObj(re.values(),ex.values())。前者是逐列比较，返回的是一个和表的列数长度相同的向量；后者是将表转换成字典再作比较，返回的是一个标量。推荐使用前者的原因是，如果两个表的某几列不相同的话，前者可以非常直观地看出哪个列不相同，而后者无法定位差异列。

以 demo
模块为例，它的回归测试代码示例如下：

```
try { use demo; }catch(x) { print(x) }
@testing:case="test_demo_minmax_table", exception=1
demo::minmax(table([1] as c1))
@testing:case="test_demo_minmax_scalar"
ret = demo::minmax(1);
assert 1, eqObj([1,1], ret)
@testing:case="test_demo_minmax_vector"
ret = demo::minmax([12,3,4]);
assert 1, eqObj([3,12], ret)
@testing:case="test_demo_echo_no_input", syntaxError=1
demo::echo(1,2,3);
@testing:case="test_demo_echo_string"
ret = demo::echo("foo");
assert 1, eqObj("foo",ret)
```

## 回归测试文件运行方式

使用
`test`函数进行测试：

```
test("/path_to_demo/test_demo.dos", "/path_to_demo/test_demo_output.txt");
```

输出中显示未通过的用例。全部通过时显示：

```
#Fail/#Total Testing Cases: 0/5
```

## 用例编写通用要点

**基本的参数校验**

* 非法输入：比如参数的类型是 STRING ，输入 INT ；参数的数据接口是 vector ，输入 scalar 等。
* 参数个数不对：比如接口的必选参数个数为3，但输入参数个数为2或4。
* 输入NULL值：比如参数的类型是 STRING ，输入NULL和string(NULL)；参数的数据结构是字典，key 或 value
  为对应类型的 NULL。

**不合理使用**

* 未`use`模块就调用其接口。

**内存泄漏和文件描述符泄漏**

* 多次执行相同代码，观察内存是否持续上涨。
* 关注是否有删库删表等危险操作。
* 关注是否有建库建表等额外操作。

**结果校验**

* 如果是计算类的接口，需要校验结果正确性。
* 如果是订阅类的接口，需要校验数据正确性和完整性。

**关注模块的错误提示和日志输出**

* 错误提示是否合理。
* 终端中的输出是否过多。
* 日志中的输入是否过多。

### 基本的参数校验

### 不合理使用

### 内存泄漏和文件描述符泄漏

### 结果校验

### 关注模块的错误提示和日志输出
