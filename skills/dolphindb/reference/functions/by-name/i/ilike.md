# ilike

## 语法

`ilike(X, pattern)`

## 详情

判断字符串 *X* 中是否包含字符串 *pattern*。和函数 like 不同，比较是不区分大小写的。

## 参数

**X** 可以是标量、向量或矩阵。

**pattern** 是一个字符串，通常包含类似 "%" 的通配符。

## 返回值

布尔标量、向量、矩阵。

## 例子

```
ilike(`ABCDEFG, `de);
// output
0

ilike(`ABCDEFG, "%de%");
// output
1

a=`IBM`ibm`MSFT`Goog`YHOO`ORCL;
a ilike  "%OO%";
// output
[0,0,0,1,1,0]

a[a ilike  "%OO%"];
// output
["Goog","YHOO"]
```

相关函数：like
