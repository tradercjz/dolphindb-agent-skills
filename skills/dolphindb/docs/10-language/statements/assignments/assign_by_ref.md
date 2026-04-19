<!-- Auto-mirrored from upstream `documentation-main/progr/statements/assignments/assign_by_ref.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 引用赋值

DolphinDB使用 "&" 来表示引用赋值。和值赋值不同，引用赋值是直接引用原值的内存地址，并不拷贝原值。
引用赋值的主要优点是避免不必要的对象拷贝。引用赋值可以有效地节约内存空间。

## 语法

`&<variable>=<object>`

## 例子

```
y=6 4 7;
y;
// output
[6,4,7]

&x=y;
x;
// output
[6,4,7]

// 修改y
y[1]=0;
y;
// output
[6,0,7]
// 修改y内容的同时修改了x内容
x;
// output
[6,0,7]

// 修改x
x[0]=3;
x;
// output
[3,0,7]
// 修改x内容的同时修改了y内容
y;
// output
[3,0,7]

y=1..3;
&x=y;
y=6..4;
x;
// output
[1,2,3]
// 若赋予y另一个向量，x也不受影响
```

下面这个例子展示是：在进行数据交互时，使用引用赋值的效率高于使用值赋值的效率。

```
n=20000000;
// 生成两个包含2千万个double元素的向量
x=rand(200000.0, n);
y=rand(200000.0, n);

// 值赋值交换数据
timer {t=x;x=y;y=t};
// output
Time elapsed: 292.005 ms

// 引用赋值交换数据
timer {&t=x;&x=y;&y=t};
// output
Time elapsed: 0 ms
```
