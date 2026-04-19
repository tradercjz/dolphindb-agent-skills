# toArray

## 语法

`toArray(X)`

## 详情

与 group by 搭配使用，按照分组将 *X*
转换为数组向量（array
vector）。如果单独使用则没有效果。

## 参数

**X** 是表的列字段名称或包含列字段的计算表达式。

## 返回值

数据类型同 *X* 的数组向量。

## 例子

```
t = table(1 1 3 4 as id, 1 3 5 6 as v1)
new_t = select toArray(v1) as newV1 from t group by id
/*
id newV1
-- -----
1  [1,3]
3  [5]
4  [6]
*/

new_t = select toArray(v1+1) as newV1 from t group by id
/*
id newV1
-- -----
1  [2,4]
3  [6]
4  [7]
*/
```

**相关函数：**toColumnarTuple, toTuple。
