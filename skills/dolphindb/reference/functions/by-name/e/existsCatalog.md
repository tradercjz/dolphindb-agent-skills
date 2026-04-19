# existsCatalog

## 语法

`existsCatalog(catalog)`

## 详情

检查指定 catalog 是否存在。

## 参数

**catalog** 字符串标量，表示 catalog 的名称。

## 返回值

布尔类型标量。 false 和 true 分别表示指定的 catalog 不存在、存在。

## 例子

```
// 检查名为 trading 的 catalog 是否存在
existsCatalog("trading")
// Output: false

// 创建 catalog
createCatalog("trading")

existsCatalog("trading")
// Output: true
```
