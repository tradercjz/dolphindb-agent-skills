# abs

## 语法

`abs(X)`

## 详情

对 *X* 内每个元素求绝对值并返回。

与 Python/NumPy/scipy.stats 的 `abs`
函数功能相同，区别在于：Python/NumPy/scipy.stats 的 `abs` 函数支持计算复数的绝对值；而 DolphinDB
的 `abs` 函数不支持计算复数绝对值，可通过DolphinDB signal 插件中的 abs
函数计算复数绝对值（见例子）。

## 参数

**X** 是可以标量、数据对、向量、矩阵、字典或表。

## 返回值

返回结果的数据形式和数据类型与输入 *X* 保持一致。若 *X* 为标量，返回标量；若为向量、矩阵或表，返回相同维度的向量、矩阵或表。

## 例子

```
abs(-2.0);
// output: 2

abs(-2 -3 4);
// output: [2, 3, 4]
```

通过 signal
插件，计算复数的绝对值。

```
// 查看插件市场是否存在 signal 插件
listRemotePlugins()
// 从插件市场下载 signal 插件
installPlugin("signal")
// 加载 signal 插件
loadPlugin("signal")
// 创建复数
z = complex(3, 4)  // 3.0+4.0i
// 计算复数绝对值
abs = signal::abs(z)
abs
// output: 5
```
