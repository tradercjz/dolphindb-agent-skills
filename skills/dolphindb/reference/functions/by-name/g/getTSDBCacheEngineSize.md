# getTSDBCacheEngineSize

## 语法

`getTSDBCacheEngineSize()`

## 详情

查询 TSDB 引擎 Cache Engine 允许使用的内存上限（单位为字节）。

## 参数

无

## 返回值

一个 LONG 类型数据。

## 例子

```
setTSDBCacheEngineSize(0.5)
getTSDBCacheEngineSize()
// output: 536870912
```

相关函数： setTSDBCacheEngineSize
