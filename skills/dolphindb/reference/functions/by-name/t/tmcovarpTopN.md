# tmcovarpTopN

首发版本：3.00.5

## 语法

`tmcovarpTopN(T, X, Y, S, window, top, [ascending=true],
[tiesMethod='latest'])`

参数说明和窗口计算规则请参考：tmTopN

## 详情

在给定长度（以时间 *T* 衡量）的滑动窗口内，根据 *ascending* 指定的排序方式将 *X* 和 *Y* 按照
*S* 进行稳定排序后，取前 *top* 个元素，计算 *X* 和 *Y* 的总体协方差。

## 返回值

DOUBLE 类型向量。

## 例子

```
T=2026.01.03+1..7
X = [2, 1, 4, 3, 4, 3, 1]
Y=[1, 7, 8, 9, 0, 5, 8]
S = [5, 8, 1, , 1, 1, 3]  //S 中包含的空值不参与排序，对应位置的 X 和 Y 不参与计算
tmcovarpTopN(T,X,Y,S,6,4)
// output: [0,-1.5,1.22,1.22,-0.75,0.875,-2]

T=2026.01.03 2026.01.07 2026.01.08 2026.01.10 2026.01.11 2026.01.12
X=8 3 1 2 5 2
Y=1 7 8 9 0 5
S=1 5 2 3 1 1
t=table(T as time, X as val1, Y as val2, S as id)
select tmcovarpTopN(time,val1,val2,id,4,3) as topN from t
```

| topN |
| --- |
| 0 |
| 0 |
| -0.5 |
| -0.33 |
| -6.44 |
| -4.67 |

相关函数：covarp
