# getLevelFileIndexCacheStatus

## 语法

`getLevelFileIndexCacheStatus()`

## 详情

获取所有 level file 的索引内存占用的情况。

## 参数

无

## 返回值

返回一个字典，包含以下 key 值：

* capacity：level file 索引内存占用上限；
* usage：level file 索引使用的内存，单位为字节。

## 例子

```
getLevelFileIndexCacheStatus()

// output
usage->0
capacity->429496729
```
