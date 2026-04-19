<!-- Auto-mirrored from upstream `documentation-main/progr/operators/lshift.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# lshift(<<)

## 语法

`X<<a`

## 参数

* **X** 可以是整数标量、数据对、向量或矩阵；
* **a** 是要移的位数。

## 详情

*lshift* 将X按二进制展开后整体往左移动a位数。右侧以0填充。

## 例子

```
lshift(2, 10);
// output
2048

1..10 << 1;
// output
[2,4,6,8,10,12,14,16,18,20]

1..10 << 10;
// output
[1024,2048,3072,4096,5120,6144,7168,8192,9216,10240]

1:10<<10;
// output
1024 : 10240
```

相关函数： rshift
