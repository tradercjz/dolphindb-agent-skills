<!-- Auto-mirrored from upstream `documentation-main/stream/cep_events_defining.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 定义事件

在 CEP 中，定义一个事件时需要指定事件类型及其每个属性的名称和类型。属性决定了事件的结构，同一个事件的每个事件实例都具有相同名称及顺序的属性集。

## 事件属性类型及形式

根据数据形式的不同，事件中的属性支持的类型有所区别：

| 属性形式 | 属性类型 |
| --- | --- |
| 标量 | 可以是 DolphinDB 的任何数据类型。 |
| 常规向量 | BOOL, CHAR, SHORT, INT, INDEX, LONG, DATE, MONTH, TIME, MINUTE, SECOND, DATETIME, TIMESTAMP, NANOTIME, NANOTIMESTAMP, DATEHOUR, FLOAT, DOUBLE, STRING, BLOB, INT128, UUID, IPADDR, POINT, COMPLEX, DECIMAL（所有类型)） DURATION, ANY。 |
| 数组向量 | 基础数据类型+方括号 “[]“，如 INT[]，DOUBLE[]，DECIMAL32(3)[] 等，表示数组向量类型。 |

## 定义事件类型的方法

**语法**

```
class eventType {
  //定义成员变量
  field_name1 :: filed_type1
  ...
  field_namen :: field_typen

  //定义和类名相同的构造函数
  def eventType(a,..., b){
  //初始化成员变量
  field_name1 = a
  ...
  field_namen = b
  }
}
```

**语法说明**

eventType：类名，表示事件类型。在 DolphinDB
中，类名不能以数字开头，不能包含空格，或除了下划线（`_`）外的其他特殊字符。

field\_name1 … field\_namen：变量名，表示属性的名称。

field\_type1 … field\_typen：变量类型，表示属性的类型。

## 事件定义示例

定义一个名为 orders 的事件，包含了 6 个属性和一个构造函数：

```
class orders{
    trader :: STRING
    market :: STRING
    code :: STRING
    price :: DOUBLE
    qty :: INT
    eventTime :: TIMESTAMP
    def orders(t, m, c, p, q){
        trader = t
        market = m
        code = c
        price = p
        qty = q
        eventTime = now()
    }
}
```
