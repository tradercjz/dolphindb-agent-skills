# between

## 语法

`between(X, Y)`

## 详情

检查 *X* 的每个元素是否在 *Y* 确定的范围内（两个边界都是包含在内的）。返回结果的长度或维度与 *X* 相同。

## 参数

**X** 可以是标量、数据对、向量或矩阵；

**Y** 是一个表示范围的数据对。

## 返回值

布尔类型，其数据形式同 *X*。

## 例子

```
between([1, 5.5, 6, 8], 1:6);
// output
[1,1,1,0]
// 1, 5.5 和 6 在 1 和 6 之间，但 8 不是。

between(1 2.4 3.6 2 3.9, 2.4:3.6);
// output
[0,1,1,0,0]
```

`between` 可以搭配 `select`
使用，用于筛选列的范围：

```
t = table(`abb`aac`aaa as sym, 1.8 2.3 3.7 as price);
select * from t where price between 1:3;
```

| sym | price |
| --- | --- |
| abb | 1.8 |
| aac | 2.3 |

下例说明数据对 a:b 中出现空值的处理方式。若配置 *nullAsMinValueForComparison*
=true，则 NULL 值当同数据类型的而最小值处理， 若配置 *nullAsMinValueForComparison* =false，则 NULL
值仍保留为 NULL。也可以使用 nullCompare 函数，无论
*nullAsMinValueForComparison* 设置为何值都保留 NULL 值。

```
between(10,:10)
// output
true      // 配置 nullAsMinValueForComparison=true 时的返回结果
between(10,:10)
// output
NULL     // 配置 nullAsMinValueForComparison=false 时的返回结果
nullCompare(between, 10, :10)
// output
NULL
```
