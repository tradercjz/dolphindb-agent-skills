# cumrank

## 语法

`cumrank(X, [ascending=true], [ignoreNA=true],
[tiesMethod='min'], [percent=false])`

部分通用参数说明和窗口计算规则请参考：累计窗口系列（cum 系列）

## 详情

对 *X* 中的每一个元素，返回其在累计窗口内的排名。

注：

如果 *ignoreNA* =
true，则 NULL 值不参与排序，结果中 NULL 值的排名为空。

## 参数

**ascending** 是一个布尔值，表示是否按升序排序。默认值是 true。

**ignoreNA** 是一个布尔值，表示是否忽略 NULL 值。true 表示忽略 NULL 值（默认值），false 表示 NULL 值参与排名，此时
NULL 值为最小值。

**tiesMethod** 是一个字符串，表示窗口内若存在重复值时，排名如何选取。

* 'min'表示取最小排名。
* 'max'表示取最大排名。
* 'average'表示取排名的均值。

**percent** 是一个布尔值，表示是否以百分比形式显示返回的排名，默认值为 false。

## 返回值

INT 类型，其数据形式同 *X*。

## 例子

```
cumrank(1 3 2 3 4);
// output: [0,1,1,2,4]

cumrank(1 3 2 2 4 NULL, ignoreNA=true);
// output: [0,1,1,1,4,]

cumrank(1 3 2 2 4 NULL, ignoreNA=false);
// output: [0,1,1,1,4,0]

cumrank(1 3 2 2 4 NULL, ignoreNA=false, tiesMethod='max');
// output: [0,1,1,2,4,0]

m=matrix(1 4 2 3 4, 4 NULL 6 1 2);
m;
```

| #0 | #1 |
| --- | --- |
| 1 | 4 |
| 4 |  |
| 2 | 6 |
| 3 | 1 |
| 4 | 2 |

```
cumrank(m);
```

| #0 | #1 |
| --- | --- |
| 0 | 0 |
| 1 |  |
| 1 | 1 |
| 2 | 0 |
| 3 | 1 |

相关函数：rank
