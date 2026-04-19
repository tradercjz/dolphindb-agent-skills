# loadHaMvccTable

首发版本：3.00.5

## 语法

`loadHaMvccTable(tableName)`

## 详情

加载并返回指定名称的高可用 MVCC 表的句柄。

注：

* `loadHaMvccTable` 是非 Leader 节点上使用高可用 MVCC 表的唯一方式。
* 对高可用 MVCC 表查询（select）可在 Leader 和 Follower 上执行，推荐在 Leader 上执行。

## 参数

**tableName** 字符串标量，表示要加载的高可用 MVCC 表的名称。

## 返回值

返回高可用 MVCC 表的句柄。

## 例子

```
hmvcct = loadHaMvccTable("demoHaMvcc")
```

**相关函数**：haMvccTable
