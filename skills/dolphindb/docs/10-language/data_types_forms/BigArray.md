<!-- Auto-mirrored from upstream `documentation-main/progr/data_types_forms/BigArray.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 大数组 (bigarray)

大数组专为大数据分析而设计。常规数组使用连续内存。如果没有足够的连续内存，则会出现内存不足的错误。一个大数组由许多小块内存组成，而不是一大块内存。因此，大数组有助于缓解内存碎片问题。但是，对于某些操作，这可能会带来轻微的性能损失。对于不需要担心内存碎片问题的大多数用户，他们应该使用常规数组而不是大数组。

大数组的最小容量为16 MB。用户可以使用函数 bigarray 声明一个大数组。常规数组的函数和操作也适用于大数组。

当我们调用函数 array
时，如果没有足够的连续内存块可用，或者如果数组占用的内存超过一定阈值（默认阈值为2048MB），系统将创建一个大数组。我们可以通过重新设定
*regularArrayMemoryLimit* 属性的值来覆盖配置文件中的默认阈值。

## 语法

`bigarray(dataType, initialSize, [capacity], [defaultValue])`

或

`bigarray(template, [initialSize], [capacity], [defaultValue])`

## 例子

```
// 很多数据类型的默认值都是 0，字符串和符号的默认值是 NULL。
x=bigarray(INT,10,10000000);
x;

[0,0,0,0,0,0,0,0,0,0]

// 默认值设为1
x=bigarray(INT,10,10000000,1);
x;

[1,1,1,1,1,1,1,1,1,1]

x=bigarray(INT,0,10000000).append!(1..100);
x[0];

1
sum x;

5050
x[x>50&&x<60];

[51,52,53,54,55,56,57,58,59]

x=array(DOUBLE, 40000000);
typestr x;

HUGE DOUBLE VECTOR
```

在顺序操作上，数组和大数组的性能几乎相同。

```
n=20000000
x=rand(10000, n)
y=rand(1.0, n)
bx= bigarray(INT, 0, n).append!(x)
by= bigarray(DOUBLE,0,n).append!(y);

timer(100) wavg(x,y);

Time elapsed: 4869.74 ms
timer(100) wavg(bx,by);

Time elapsed: 4762.89 ms

timer(100) x*y;

Time elapsed: 7525.22 ms
timer(100) bx*by;

Time elapsed: 7791.83 ms
```

对于随机访问，大数组将会有轻微的性能劣势。

```
indices = shuffle 0..(n-1);
timer(10) x[indices];

Time elapsed: 2942.29 ms
timer(10) bx[indices];

Time elapsed: 3547.22 ms
```
