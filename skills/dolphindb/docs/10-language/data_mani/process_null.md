<!-- Auto-mirrored from upstream `documentation-main/progr/data_mani/process_null.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 空值运算

通常来说，如果函数或运算符的其中一个参数是空值，结果也会是空值。

```
x = 1.0 + 5.6 * 3 + NULL + 3
isNull(x)
// output: 1

typestr x;
// output: DOUBLE
```

但存在如下特殊情况：

* 在比较运算符 >, >=, <, <=, between
  中，默认情况下（*nullAsMinValueForComparison*=true），空值表示最小值。当设置参数
  *nullAsMinValueForComparison*=false 时，比较的最终结果是空值。

  ```
  // nullAsMinValueForComparison = true
  1 < NULL // output: false
  1 > NULL // output: true

  // nullAsMinValueForComparison = false
  1 < NULL // output: 00b
  1 > NULL // output: 00b
  ```
* 在比较运算符 !=, <>, == 中，空值表示最小值，且两个空值被认为是相等的。

  ```
  NULL == NULL // output: true
  NULL != NULL // output: false
  ```
* 在 `or`
  函数中，默认情况下（*logicOrIgnoreNull*=true），如果只有一个操作数为空，结果等于另一个非空操作数。若两个操作数均为空，则返回空值。当设置
  *logicOrIgnoreNull*= false 时，若有一个操作数为空，结果将返回空值。

  ```
  // logicOrIgnoreNull = true
  NULL or true // output: true
  NULL or false // output: false
  NULL or NULL // output: 00b

  // logicOrIgnoreNull = false

  NULL or true // output: 00b
  NULL or false // output: 00b
  NULL or NULL // output: 00b
  ```
* 聚合函数（如 `sum/avg/med` 等） 中的空值会被忽略。

  ```
  x = 1 2 NULL NULL 3;
  sum(x)
  // output: 6

  avg(x)
  // output: 2
  ```
* 向量中的元素进行排序时，空值表示最小值。
* 在
  `ols`、`olsEx`、`corrMatrix`、`olsEx`
  函数中，参数中的空值会被替换为 0。
