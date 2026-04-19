# getMemoryStat

## 语法

`getMemoryStat()`

## 详情

获取当前节点已分配的内存和未使用的内存。

## 参数

无

## 返回值

返回一个字典，其 key 值的含义为：

* freeBytes：当前节点未使用的内存，单位为字节。
* allocatedBytes：当前节点已分配的内存，单位为字节。

## 例子

```
getMemoryStat();

// output
freeBytes->6430128
allocatedBytes->35463168
```
