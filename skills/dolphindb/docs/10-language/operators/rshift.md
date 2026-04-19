<!-- Auto-mirrored from upstream `documentation-main/progr/operators/rshift.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# rshift(>>)

## 语法

`X>>a`

## 参数

* **X** 可以是整数标量、数据对、向量或矩阵；
* **a** 是要移的位数。

## 详情

*rshift* 是将X按二进制展开后整体往右移动a位数。原来右侧的位数被截去。

## 例子

```
rshift(2048, 2);
// output
512

1..10 >> 1;
// output
[0,1,1,2,2,3,3,4,4,5]

1:10>>1;
// output
0 : 5
```

相关函数： lshift
