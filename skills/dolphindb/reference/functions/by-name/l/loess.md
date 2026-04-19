# loess

## 语法

`loess(X, Y, resampleRule, [closed='left'], [origin='start_day'],
[outputX=false], [bandwidth=0.3], [robustnessIter=4], [accuracy=1e-12])`

## 详情

该函数根据 *resampleRule*, *closed*, *origin* 确定的采样规则，对
*X* 进行重采样操作。并根据重采样后的 *X*，对 *Y* 按照局部回归算法进行插值（Loess
Interpolatiion）。

## 参数

**X** 严格递增的时间类型向量。

**Y** 同 *X* 等长的数值型向量。

**resampleRule** 一个字符串，可选值请参考 resample 的
*rule* 参数。

**closed** 和 **origin** 同 resample 的
*closed* 和 *origin* 参数。

**outputX** 布尔类型，表示是否输出 *X* 按照 *resampleRule*, *closed*,
*origin* 重采样后的向量。默认值为 false。

**bandwidth** 数值型标量，取值范围为(0,1]。对特定点进行 loess 拟合时，计算最小二乘回归时会考虑最接近当前点的这部分源点。

**robustnessIter** 正整数，表示进行 loess 平滑处理时进行的鲁棒性迭代的次数。

**accuracy** 一个大于0的数。若鲁棒性迭代过程中的中值残差小于此参数设置值，则停止迭代。

## 返回值

若不指定 *outputX*，仅返回一个对 *Y* 插值后的向量。若指定 *outputX* =
true，则返回一个 tuple，其第一个元素为 *X* 重采样后的向量，第二个元素为对 *Y* 插值后的向量。

## 例子

**例 1**

```
loess([2016.02.14 00:00:00, 2016.02.15 00:00:00, 2016.02.16 00:00:00], [1.0, 2.0, 4.0], resampleRule=`60min, bandwidth=1)

// output
[1,1.0521,1.104,1.1558,1.2072,1.2582,1.3086,1.3584,1.4074,1.4556,
1.5027,1.5488,1.5937,1.6374,1.6795,1.7202,1.7593,1.7966,1.832,1.8655,
1.897,1.9263,1.9533,1.9779,2,2.0195,2.0366,2.0513,2.0637,2.0739,
2.082,2.0882,2.0926,2.0952,2.0962,2.0957,2.0938,2.0905,2.0861,2.0806,
2.0741,2.0667,2.0586,2.0498，2.0405,2.0308,2.0207,2.0104,2]
```

**例 2** 不同 *closed*
取值的影响。

```
X = 2022.01.01T00:00:00 + [0, 3, 6, 9] * 60
Y = [1.0, 3.0, 7.0, 13.0]

// closed='left'（默认）：00:03 归入 [00:03, 00:06) 的起点
loess(X, Y, `3min, closed=`left, outputX=true, bandwidth=1)

// closed='right'：00:03 归入 (00:00, 00:03] 的终点
// 局部回归的拟合点位置不同，输出结果不同
loess(X, Y, `3min, closed=`right, outputX=true, bandwidth=1)
```

**例 3** 不同 *origin*
取值的影响。

```
X = 2022.01.01T00:00:30 + (0..4) * 60
Y = [2.0, 4.0, 7.0, 11.0, 16.0]

// origin='start_day'（默认）：从当天零点对齐
loess(X, Y, `1min, origin=`start_day, outputX=true, bandwidth=1)

// origin='start'：从第一个数据点 00:00:30 对齐
loess(X, Y, `1min, origin=`start, outputX=true, bandwidth=1)

// origin=自定义时间戳：从 00:00:10 对齐
loess(X, Y, `1min, origin=2022.01.01T00:00:10, outputX=true, bandwidth=1)
```

**例 4** 不同 *outputX*
取值的影响。

```
X = [2016.02.14T00:00:00, 2016.02.15T00:00:00, 2016.02.16T00:00:00]
Y = [1.0, 2.0, 4.0]

// outputX=false（默认）：只返回局部回归插值后的 Y 向量
loess(X, Y, `60min, bandwidth=1)

// outputX=true：返回 tuple，[0] 为重采样后的时间戳，[1] 为插值 Y
result = loess(X, Y, `60min, outputX=true, bandwidth=1)
result[0]
result[1]
```
