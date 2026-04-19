# eqPercent

## 语法

`eqPercent(X, Y,[toleranceLevel=0.0001])`

## 详情

根据自定义约束条件，判断两个输入参数的每个对应位置上的元素是否都相等。

## 参数

**X** 和 **Y** 要比较的两个数值，仅支持长度相同的标量、向量、数据对或矩阵。数据类型仅支持 BOOL, CHAR, SHORT, INT,
LONG, FLOAT, DOUBLE, DECIMAL。注意：*X* 和 *Y* 中的元素在比较时可以是不同的数据类型。

**toleranceLevel** 可选参数，数值标量，值域为(0,100)，表示可容许误差的百分位数，默认值为 0.0001。即两元素差值的绝对值不多于
*Y* 绝对值的 `toleranceLevel%`。如 *Y* 输入
1000，*toleranceLevel* 取默认值 0.0001，则可容忍误差为 1000\*0.0001%=0.001，即[999.999,
1000.001]之间的 *X* 会被认为相等。

## 返回值

输出一个 BOOL 标量，true 代表 *X* 与 *Y* 每个对应位置的元素都在约束下相等；false 反之。

注意：

* 如果传入的参数 *X* 或 *Y* 的类型不受支持，则返回 `eqObj(X, Y)`
  的结果值。
* NULL 值和其他值不相等。
* 不同类型之间的 NULL 值被认为相等。

## 例子

以下给出几个简单示例。

```
eqPercent((1.9999 2.9999), (2 3))
//Output:true

eqPercent((1.9 2.9), (2 3), 2)
//Output:false

eqPercent((1.99f 2.99), (2 3h), 2)
//Output:true
//X和Y中的元素在比较时可以是不同的数据类型

eqPercent((1.9999 NULL), (2 3))
//Output:false

a=double(NULL)
eqPercent(a,NULL)
//Output:true
//DOUBLE类型和VOID类型的NULL相等

eqPercent(2012.06M, 2)
//Output:false
//传入不支持其类型的X，返回eqObj(X, Y)的结果值。
```

相关函数：eqObj
