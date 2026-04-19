# cubicSpline

## 语法

`cubicSpline(x, y, bc_type="not-a-knot")`

## 详情

生成三次样条插值曲线。

* 当 *bc\_type* 是一个字符串标量或长度为 1 的向量时，以此作为曲线两端的限制条件。
* 当 *bc\_type* 是一个数据对或长度为 2 的向量时，两个元素分别作为曲线左端和右端的限制。

## 参数

**x** 是一个数值向量，代表自变量的值。x 的长度不小于 3，必须严格递增，且不包含空值。

**y** 是一个数值向量，代表因变量的值。y 必须与 x 长度相等。

**bc\_type** 是一个字符串标量、字符串数据对、或长度小于等于 2
的向量，用于限定边界条件。字符串支持”not-a-knot“、”clampe“、”natural“，默认值为”not-a-knot“。

* not-a-knot：曲线的前两段和最后两段的三阶导数相等。
* clamped：曲线两端点处的一阶导数为零。
* natural：曲线两端点处的二阶导数为零。

## 返回值

一个字典，包含如下键：

* c：三次样条函数的分段多项式的系数
* x：输入的 x 向量
* predict：模型的预测函数，`predict` 函数将返回在 X 点处的三次样条插值结果。可通过
  `model.predict(X)` 或 `predict(model, X)`
  进行调用。其中：
  + model：字典类型，即 `cubicSpline` 的输出。
  + X： 数值向量，表示需要求值的点的 x 坐标。
* modelName：字符串类型，表示模型名称，值为 “cubicSpline”。

## 例子

```
n = 10
x = 0..(n-1)
y = sin(x)
model = cubicSpline(x, y, bc_type="not-a-knot")
print(model)
```

返回：

```
x->[0,1,2,3,4,5,6,7,8,9]
predict->cubicSplinePredict
modelName->cubicSpline
c->[-0.0418500756165063,-0.2612720445455365,1.1445931049699394,0.0,-0.0418500756165067,-0.3868222713950554,0.4964987890293473,0.8414709848078965,0.1468910600890447,-0.5123724982445756,...]
```

**相关信息**

* [cubicSplinePredict](cubicsplinepredic.html "cubicSplinePredict")
