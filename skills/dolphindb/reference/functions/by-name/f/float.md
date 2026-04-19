# float

## 语法

`float([X])`

## 详情

将输入数据的类型转换为 FLOAT。

## 参数

**X** 可选参数。任意数据类型，并且可以是任意数据形式。

## 返回值

FLOAT 类型的数据，数据形式同 *X*。

## 例子

创建一个 FLOAT 类型的变量，默认值为 NULL。

```
x=float()
x // 输出 null
typestr x // 输出 'FLOAT'
```

转换用于表示数字的字符串。

```
x=float("123")
x // 输出 123
typestr x // 输出 'FLOAT'
```

转换布尔值。

```
x=float([true, false])
x // 输出 [1, 0]
typestr x // 输出 'FAST FLOAT VECTOR'
```

转换 DOUBLE 类型的数据。

```
x=123456789.1234567 // 16 位数字
typestr x // 输出 'DOUBLE'

y=float(x)
y // 输出 123,456,792 （FLOAT 最多只能包含 9 位数字）
typestr y // 输出 'FLOAT'
```

创建值为正无穷和负无穷的变量。

```
// 创建值为正无穷的变量
posInf=float("inf")
posInf // 输出 ∞
typestr posInf // 输出 'FLOAT'
posInf > 1000000000 // 输出 true

// 创建值为负无穷的变量
negInf=float("-inf")
negInf // 输出 -∞
typestr negInf // 输出 'FLOAT'
negInf < NULL // 输出 true
```
