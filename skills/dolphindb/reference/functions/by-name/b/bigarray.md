# bigarray

## 语法

`bigarray(dataType|template, [initialSize], [capacity],
[defaultValue])`

## 详情

大数组是专门为进行大数据分析的用户设计的。常规的数组使用连续的内存。如果没有足够的连续内存，就会产生内存不足的异常。大数组由许多小的内存块组成，而不是一个大的内存块。所以，大数组缓解了内存碎片问题。但这可能会对某些操作造成轻微的性能损失。对于多数不需要担心内存碎片问题的用户而言，应该使用常规数组，而不是大数组。

大数组的最小容量是 16 MB。用户可以用 `bigarray` 函数声明一个大数组。

操作大数组的方法和操作一个常规数组一样。

当我们调用 array
函数时，如果没有足够的连续内存块，或数组占据的内存超过了一个特定的阈值（默认的阈值是 2048 MB），系统会改为创建一个大数组。

## 参数

**dataType** 是大数组的数据类型。

**template** 是已有的向量。已有的向量作为模板，它的数据类型决定了新的大数组的数据类型。

**initialSize**
是正整数，表示大数组的初始长度，即该大数组新建时的元素数量。如果第一个参数是数据类型，*initialSize*是必需参数。如果第一个参数是已有的大数组，*initialSize*是可选参数。

**capacity** 是正整数，表示大数组的容量，即该大数组新建时系统为该大数组分配的内存（以元素数为单位）。当元素数超过 *capacity*
时，系统会自动扩充容量。系统首先会分配当前容量1.2~2倍的内存，然后复制数据到新的内存空间，最后释放原来的内存。

**defaultValue** 是大数组的默认值。如果不指定默认值，对于多数数据类型，默认值是 0。对于字符串和符号（Symbol），默认值是 NULL。

## 返回值

返回一个大数组，其数据类型同 *dataType*/*template*。

## 例子

```
x=bigarray(INT,10,10000000);
x;
// output
[0,0,0,0,0,0,0,0,0,0]

// 默认值设为 1
x=bigarray(INT,10,10000000,1);
x;
// output
[1,1,1,1,1,1,1,1,1,1]

x=bigarray(INT,0,10000000).append!(1..100);
x[0];
// output
1
sum x;
// output
5050

x[x>50&&x<60];
// output
[51,52,53,54,55,56,57,58,59]

x=array(DOUBLE, 40000000);
typestr x;
// output
HUGE DOUBLE VECTOR
```

数组和大数组的性能比较：

```
// 对于顺序操作，数组和大数组的表现几乎相同。
n=20000000
x=rand(10000, n)
y=rand(1.0, n)
bx= bigarray(INT, 0, n).append!(x)
by= bigarray(DOUBLE,0,n).append!(y);

timer(100) wavg(x,y);
// output
Time elapsed: 4869.74 ms
timer(100) wavg(bx,by);
// output
Time elapsed: 4762.89 ms

timer(100) x*y;
// output
Time elapsed: 7525.22 ms
timer(100) bx*by;
// output
Time elapsed: 7791.83 ms

// 对于随机访问，大数组有轻微的性能损失。
indices = shuffle 0..(n-1);
timer(10) x[indices];
// output
Time elapsed: 2942.29 ms
timer(10) bx[indices];
// output
Time elapsed: 3547.22 ms
```
