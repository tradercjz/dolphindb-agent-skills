<!-- Auto-mirrored from upstream `documentation-main/progr/operators/member.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# member(.)

## 语法

`X.Y`

## 参数

* **X** 是一个对象。
* **Y** 是对象的成员或属性。

## 详情

返回对象的指定成员或属性。

## 例子

```
x=1 2 3;
y=4 5 6;
t=table(x,y);

t.x;
// output
[1,2,3]
t.y;
// output
[4,5,6]

t.rows();
// output
3
t.cols();
// output
2
t.size();
// output
3
// 一个表的长度指的是其包含的数据行数。
```

从2.00.11.1/1.30.23.1版本开始，系统支持在 member(.) 运算符之前换行。在链式调用比较长时，可以进行适当的换行。

```
t = table(take(1..5,10) as a, take(6..10,10) as b, take(1..2,10) as c)

t.replaceColumn!("a",lpad(string(t.a),6,"0"))
     .replaceColumn!("b",rpad(string(t.b),6,"0")).add(100)
```
