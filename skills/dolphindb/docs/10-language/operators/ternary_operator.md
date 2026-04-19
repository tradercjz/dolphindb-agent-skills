<!-- Auto-mirrored from upstream `documentation-main/progr/operators/ternary_operator.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 三元运算符(?:)

## 语法

`condition ? trueClause :
falseClause`

## 参数

**condition** BOOL 类型的标量、向量，或者是可产生BOOL 类型的标量、向量的变量、函数调用或者表达式。注意：

* 不可为空。
* 如果是一个表达式，则必须使用括号包裹。
* 如果是常量、变量或函数调用，则可以不使用括号包裹。

**trueClause 和 falseClause** 变量、函数调用或者表达式。不要求必须使用括号包裹。

## 详情

三元运算符 (`?:`) 也称为三元条件运算符或条件运算符，用于计算布尔表达式（对应参数
*condition*），并根据其计算结果为 `true` 还是 `false`
来选择性执行两个表达式（对应参数 *trueClause*, *falseClause*）。

* 如果 *condition* 是一个布尔型标量：

  + 若结果为 true，只执行 *trueClause*，并作为结果返回。
  + 若结果为 false，只执行 *falseClause*，并作为结果返回。
* 如果 condition 是一个布尔型向量，则当作 `iif(condition, trueClause,
  falseClause)` 处理，即 *trueClause* 和 *falseClause*
  都可能被执行。

注意：

* *trueClause* 和 *falseClause* 可以是另一个三元表达式，即支持嵌套。
* 可以在 SQL 和非 SQL 环境中使用。
* 表达式中可以使用变量和字段。

## 例子

以下给出一些简单的使用示例。

```
true ? 1 : 0
//output: 1

true true true false false false ? 1..6 : 6..1
//output: [1,2,3,3,2,1]

(1..6==4) ? 1 : 0
//output: [0,0,0,1,0,0]

a = 1..6
a1 = a>3
a1 ? 1 : 0
//output: [0,0,0,1,1,1]

b = 1 2 3
(b<=2) ? 4*b : 5*b-1
//output: [4,8,14]

true ? add(1,1) : and(1,4)
//output: 2
```

此处给出一个实际例子。在工业物联网行业中，用户经常需要监控各种传感器数据，并根据预设的阈值来触发警报或调整设备操作。本例中，获取到某温度传感器的设备状态
`deviceStatus` 和温度值 `temperature`
，通过三元表达式可以快速判断当前设备数据是否在线且温度超出阈值。

```
deviceStatus = "online"
temperature = 55
(deviceStatus == "online" && temperature<=45) ?  "pass" :  "warning"
//output: warning
```

*trueClause* 和 *falseClause*
可以是任意数据类型、数据形式。以下给出一个简单示例。

```
x = 1 2 3 4;
y = 2.3 4.6 5.3 6.4;
p = dict(x, y);

q = 1:3

((3 add 2)<=6) ? p : q

/*output:
key	value
1	2.3
2	4.6
3	5.3
4	6.4
*/
```

下例对表运用三元运算符。此处先生成两张表。

```
t = table(1..5 as id, 11..15 as x);
t1 = table(take(12,5) as a, take(14,5) as b);
t;
```

表 1.

|  |  |
| --- | --- |
| id | x |
| 1 | 11 |
| 2 | 12 |
| 3 | 13 |
| 4 | 14 |
| 5 | 15 |

```
t1;
```

表 2.

|  |  |
| --- | --- |
| a | b |
| 12 | 14 |
| 12 | 14 |
| 12 | 14 |
| 12 | 14 |
| 12 | 14 |

此处在 SQL 语句中使用嵌套后的三元运算式，对表 t 中的数据进行更新。

```
update t set x = ((x < t1.a) ?  t1.a : (x>t1.b) ? t1.b :  x);
t;
```

表 3.

|  |  |
| --- | --- |
| id | x |
| 1 | 12 |
| 2 | 12 |
| 3 | 13 |
| 4 | 14 |
| 5 | 14 |

相关函数：iif
