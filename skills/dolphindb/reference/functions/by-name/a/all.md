# all

## 语法

`all(X)`

## 详情

如果 *X* 中包含 false 或0，返回 false；反之返回 true。NULL 值不参与计算。

说明：DolphinDB `all` 函数与 Python `all` 和
`numpy.all` 函数功能相同，但在空值处理上存在不同：

* DolphinDB `all` 函数忽略空值。
* Python `all` 将 None 视为 False。
* `numpy.all` 将 np.nan 视为非零值。

## 参数

**X** 可以是标量、数据对、向量或矩阵。

## 返回值

* 当 *X* 是标量、向量、数据对时，返回一个布尔值。
* 当 *X* 是矩阵时，返回一个布尔向量。

## 例子

```
all(1 2 3)
// output: true

all(0 1 2)
// output: false

all(true false)
// output: false

all(true true true)
// output: true

all(1..10$2:5)
// output: [true,true,true,true,true]

all(0..9$2:5);
// output: [false,true,true,true,true]
```

相关函数：any
