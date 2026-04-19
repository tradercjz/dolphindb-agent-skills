<!-- Auto-mirrored from upstream `documentation-main/rn/compat_report_3000.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 3.00.0

使用当前版本需要升级 *dolphindb.dos* 文件为最新版本。

## 3.00.0.1

### 缺陷修复带来的系统影响

管理员用户调用 `shell` 函数的权限发生了变化：

* 之前版本，允许管理员用户调用。
* 当前版本，默认不允许任何用户调用。可通过设置配置参数 *enableShellFunction*=true
  ，允许管理员用户调用。

## 3.00.0.0

### 涉及保持一致性或兼容行业惯例的修改

* 执行函数别名时的行为发生改变。

  + 在 2.00 系列的版本中，按照函数原名处理。
  + 在当前版本中，按照定义时传入的函数别名处理。

  例1：在 lamdba 表达式中调用 `pow` 函数（原名
  `power`），其返回结果中的函数名发生变化。

  ```
  def f1(x){return def(k): pow(x,k)}
  f1(1)
  //2.00系列的版本中，返回结果：{def (x, k)->power(x, k)}{1}
  //当前版本中，返回结果：{def (x, k)->pow(x, k)}{1}
  ```

  例2：在 SQL 语句中使用`mean`函数（原名
  `avg`）时，其根据函数名间接生成的列名发生变化。

  ```
  t=table([1,2,3,4] as a,[2,3,45,6] as b)
  select mean(b) from t

  /*
  2.00系列的版本中，返回结果：
  avg_b
  14
  */

  /*
  当前版本中，返回结果：
  mean_b
  14
  */
  ```
