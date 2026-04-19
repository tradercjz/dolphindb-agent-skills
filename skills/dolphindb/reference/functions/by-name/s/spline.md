# spline

## 语法

`spline(X, Y, resampleRule, [closed='left'], [origin='start_day'],
[outputX=false])`

## 详情

该函数根据 *resampleRule*, *closed*, *origin* 确定的采样规则，对
*X* 进行重采样操作。并根据重采样后的 *X*，对 *Y* 进行三次样条插值（Cubic Spline
Interpolation）。

## 参数

**X** 严格递增的时间类型向量。

**Y** 同 *X* 等长的数值型向量。

**resampleRule** 一个字符串，可选值请参考 resample 的
*rule* 参数。

**closed** 和 **origin** 同 resample 的
*closed* 和 *origin* 参数。

**outputX** 布尔类型，表示是否输出 *X* 按照 *resampleRule*, *closed*,
*origin* 重采样后的向量。默认值为 false。

## 返回值

若不指定 *outputX*，仅返回一个对 *Y* 插值后的向量。若指定 *outputX* =
true，则返回一个 tuple，其第一个元素为 *X* 重采样后的向量，第二个元素为对 *Y* 插值后的向量。

## 例子

**例
1**

```
spline([2016.02.14 00:00:00, 2016.02.15 00:00:00, 2016.02.16 00:00:00], [1.0, 2.0, 4.0], resampleRule=`60min);

// output
[1,1.0313,1.0626,1.0942,1.1262,1.1585,1.1914,1.225,1.2593,1.2944,1.3306,1.3678,1.4062,1.446,1.4871,1.5298,1.5741,1.6201,1.668,1.7178
,1.7697,1.8237,1.8801,1.9388,2,2.0638,2.1301,2.1987,2.2697,2.3428,2.418,2.4951,2.5741,2.6548,2.7371,2.821,2.9062,2.9928,3.0806,3.1694
,3.2593,3.35,3.4414,3.5335,3.6262,3.7192,3.8126,3.9063,4]
```

**例 2** 不同 *closed*
取值的影响。

```
X = 2022.01.01T00:00:00 + [0, 3, 6, 9] * 60
Y = [1.0, 3.0, 7.0, 13.0]

// closed='left'（默认）：00:03 归入 [00:03, 00:06) 的起点
spline(X, Y, `3min, closed=`left, outputX=true)

// closed='right'：00:03 归入 (00:00, 00:03] 的终点
// 重采样 X 的起始点不同，样条曲线形状不同
spline(X, Y, `3min, closed=`right, outputX=true)
```

**例 3** 不同 *origin*
取值的影响。

```
X = 2022.01.01T00:00:30 + (0..4) * 60
Y = [2.0, 4.0, 7.0, 11.0, 16.0]

// origin='start_day'（默认）：从当天零点对齐
spline(X, Y, `1min, origin=`start_day, outputX=true)

// origin='start'：从第一个数据点 00:00:30 对齐
spline(X, Y, `1min, origin=`start, outputX=true)

// origin=自定义时间戳：从 00:00:10 对齐
spline(X, Y, `1min, origin=2022.01.01T00:00:10, outputX=true)
```

**例 4** 不同 *outputX*
取值的影响。

```
X = [2016.02.14T00:00:00, 2016.02.15T00:00:00, 2016.02.16T00:00:00]
Y = [1.0, 2.0, 4.0]

// outputX=false（默认）：只返回三次样条插值后的 Y 向量
spline(X, Y, `60min)

// outputX=true：返回 tuple，[0] 为重采样后的时间戳，[1] 为插值 Y
result = spline(X, Y, `60min, outputX=true)
result[0]
result[1]
```
