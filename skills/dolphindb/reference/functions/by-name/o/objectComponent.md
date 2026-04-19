# objectComponent

## 语法

`objectComponent(obj)`

## 详情

获取对象的组成信息。

## 参数

**obj** 任意数据类型的对象。

## 返回值

一个字典：

* 当 *obj* 不是 CODE 类型，字典包含 *obj* 的组成部分。
* 当 *obj* 是 CODE 类型，字典包含 *obj* 所表征对象的组成部分。

## 例子

```
objectComponent(<select col1,col2 from pt>)

/*
output:
exec->0
select->(< col1 >,< col2 >)
from->< objByName("pt") >
where->()
groupBy->()
groupFlag->
cgroups->0
csort->()
having->
orderBy->()
rowOffset->
rowCount->
hint->0
segment->
*/
```
