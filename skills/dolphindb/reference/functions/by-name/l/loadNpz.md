# loadNpz

## 语法

`loadNpz(fileName)`

## 详情

读取 Python Numpy 的 npz 格式二进制文件，并转化为 DolphinDB 的对象。Numpy 对象中的 NaN
值会被转化为 DolphinDB 的 NULL 值。

Python np.array 和 DolphinDB 对象对照表：

支持转换的数据类型有：BOOL, CHAR, SHORT, INT, LONG, FLOAT, DOUBLE,
STRING（只支持一维）

| numpy array | DolphinDB object |
| --- | --- |
| 一维 | 向量 |
| 二维 | 矩阵 |
| 三维 | 元组。元组的每一个元素是一个矩阵 |

## 参数

**filename** 是字符串，表示 npz 文件的路径。

## 返回值

一个字典，键为 npz 文件中数组的名称，值为对应的向量、矩阵或元组。

## 例子

在 Python 中导出 npz 格式文件：

```
import numpy as np
a = np.array([[[97, 98]]], dtype=np.int8)
a1 = np.array(['133', '211', '3dds', 'ddd4', 'e5', 'w6'])
b1 = np.array([[0.7, 0.8, 9.2], [0, np.nan, np.nan], [1.5, 2.8, 0.2]])
c1 = np.array([[[0.2, 3.3], [1.9, 4.3]], [[5, 6], [1, 2]]])
np.savez('my_path/array_save.npz', char=a, a1=a1, b1=b1, c1=c1)
```

在 DolphinDB 中加载 npz 文件：

```
path="my_path/array_save.npz"
loadNpz(path)
// output
a1->[133,211,3dds,ddd4,e5,w6]
char->(#0  #1
'a' 'b'
)
c1->(#0  #1
0.2 3.3
1.9 4.3
,#0 #1
5  6
1  2
)
b1->
#0  #1  #2
0.7 0.8 9.2
0
1.5 2.8 0.2
```

相关函数：loadNpy
