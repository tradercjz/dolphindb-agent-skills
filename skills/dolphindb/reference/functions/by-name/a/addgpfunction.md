# addGpFunction

## 语法

`addGpFunction(engine, func)`

注：

社区版 License 暂不支持该函数，如需使用此功能，请联系技术支持。

## 详情

在现有训练函数的基础上增加用户自定义函数，用于初始化公式树和进化时使用。支持的算子详见附录。

## 参数

**engine** 通过函数 `createGPLearnEngine` 创建引擎的返回对象。

**func** 用户自定义函数。自定义函数目前不支持复杂赋值、if、for 等语句，只支持 return 语句，return
值为已支持的训练函数的组合。例如：

```
def f(x, y){
  return cos(x+y)
}
```

## 例子

```
def f(x, y){
  return cos(x+y)
}
addGpFunction(engine,f)
```

## 附录

目前已支持的训练函数：

注：

对于所有的 m 系列函数，如果当前窗口小于 n，则会直接返回 0。而 DolphinDB 默认返回空值。

| 函数名 | 入参数量 | 描述 |
| --- | --- | --- |
| add(x,y) | 2 | 加法 |
| sub(x,y) | 2 | 减法 |
| mul(x,y) | 2 | 乘法 |
| div(x,y) | 2 | 除法， 如果除数的绝对值小于0.001，返回1 |
| max(x,y) | 2 | 最大值 |
| min(x,y) | 2 | 最小值 |
| sqrt(x) | 1 | 按照绝对值开方 |
| log(x) | 1 | `iif(x < 0.001, 0, log(abs(x)))` |
| neg(x) | 1 | 相反数 |
| reciprocal(x) | 1 | 倒数，如果x的绝对值小于0.001，将返回0 |
| abs(x) | 1 | 绝对值 |
| sin(x) | 1 | 正弦函数 |
| cos(x) | 1 | 余弦函数 |
| tan(x) | 1 | 正切函数 |
| sig(x) | 1 | sigmoid函数 |
| signum(x) | 1 | 返回 x 的符号标志 |
| mcovar(x, y, n) | 2 | 滑动窗口为n时，x和y的协方差 |
| mcorr(x, y, n) | 2 | 滑动窗口为n时，x和y的相关性 |
| mstd(x, n) | 1 | 滑动窗口为n时，x的样本标准差 |
| mmax(x, n) | 1 | 滑动窗口为n时，x的最大值 |
| mmin(x, n) | 1 | 滑动窗口为n时，x的最小值 |
| msum(x, n) | 1 | 滑动窗口为n时，x的和 |
| mavg(x, n) | 1 | 滑动窗口为n时，x的平均数 |
| mprod(x, n) | 1 | 滑动窗口为n时，x的积 |
| mvar(x, n) | 1 | 滑动窗口为n时，x的样本方差 |
| mvarp(x, n) | 1 | 滑动窗口为n时，x的总体方差 |
| mstdp(x, n) | 1 | 滑动窗口为n时，x的总体标准差 |
| mimin(x, n) | 1 | 滑动窗口为n时，x的最小值下标 |
| mimax(x, n) | 1 | 滑动窗口为n时，x的最大值下标 |
| mbeta(x, y, n) | 2 | 滑动窗口为n时，x在y上的回归系数的最小二乘估计 |
| mwsum(x, y, n) | 2 | 滑动窗口为n时，x和y的内积 |
| mwavg(x, y, n) | 2 | 滑动窗口为n时，x以y为权重的加权平均值 |

**相关信息**

* [Shark GPLearn 快速上手](../../tutorials/gplearn.html "Shark GPLearn 快速上手")
