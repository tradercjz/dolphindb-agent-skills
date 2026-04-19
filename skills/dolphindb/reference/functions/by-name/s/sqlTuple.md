# sqlTuple

## 语法

`sqlTuple(colNames)`

## 详情

生成一个元代码，其内容是一个元组表达式，元组的元素为 colNames 指定的列。常与函数 sql，makeUnifiedCall
共同使用，用于动态生成 SQL 语句。

## 参数

**colNames** 字符串标量或向量，表示列名。

## 返回值

CODE 类型标量。

## 例子

下例中，函数 makeUnifiedCall 以 sqlTuple 生成的元组表达式的元代码为参数，调用自定义函数
f，其结果作为函数 sql 的参数 select ，从而生成元代码 c 。

```
// 自定义函数
f = def (x,y)->(x-y)/(x+y)

// 定义待查询的表
t = table(1.0 2.0 3.0 as qty1, 1.0 3.0 7.0 as qty2)

// 生成查询的元代码
c = sql(select=makeUnifiedCall(f, sqlTuple(`qty1`qty2)), from=t)

// 执行对应元代码
c.eval()
```

| \_qty1 |
| --- |
| 0 |
| -0.2 |
| -0.4 |

**相关信息**

* [makeUnifiedCall](../m/makeUnifiedCall.html "makeUnifiedCall")
