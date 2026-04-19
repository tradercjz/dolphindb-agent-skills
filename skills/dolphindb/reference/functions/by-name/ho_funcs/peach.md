# peach

## 语法

`peach(func, args...)`

## 详情

*peach* 是并行计算版本的 *each* 高阶函数。对于执行时间较长的任务，*peach* 比
*each* 能节省大量的时间。但对于小任务，*peach* 可能执行时间要比each更长，因为并行函数调用的开销很大。

## 例子

对于执行时间长的任务，使用 *peach* 进行并行计算，可以节约任务执行时间。

```
m=rand(1,20000:5000)
timer f=peach(mskew{,8},m)

Time elapsed: 3134.71 ms
timer f=mskew(m,8)

Time elapsed: 8810.485 ms
```
