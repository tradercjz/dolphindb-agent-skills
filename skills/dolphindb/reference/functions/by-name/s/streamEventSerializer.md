# streamEventSerializer

## 语法

`streamEventSerializer(name, eventSchema, outputTable, [eventTimeField],
[commonField])`

## 详情

将事件序列化为 BLOB 格式，并写入到异构流表。

## 参数

**name** 字符串，表示序列化引擎的名称，可包含字母，数字和下划线，但必须以字母开头。

**eventSchema** 可以是事件定义或一个表。用于指定进行序列化的事件及其声明的成员变量。

* 如果指定为事件类型定义，则可以指定为一个或多个事件类型定义。例如：定义了两个事件类型类，event1 和 event2，则可指定为
  *eventSchema*=[event1, event2]
* 如果指定为表，则必须具有如下表结构（可通过 `getCEPEngineStat(engine).eventSchemas` 获得
  CEP 引擎中所有事件的结构）：

  | 列名 | 含义 |
  | --- | --- |
  | eventType | 字符串，表示事件类型 |
  | eventField | 字符串，表示事件类型中所声明的字段名。多个字段名之间以逗号（,）分隔 |
  | fieldType（可选） | 字符串，表示 eventField 中各字段对应的数据类型的名称，多个名称之间以逗号（,）分隔 |
  | fieldTypeId | 整型数组向量，表示 eventField 中各字段对应的数据类型的 ID。 |
  | fieldFormId | 整型数组向量，表示 eventField 中各字段对应的数据形式的 ID。整型数组向量，0：标量; 1：向量; 2：数据对; 3：矩阵; 4：集合; 5：字典; 6：表  注意：目前只能指定标量和向量。 |

**outputTable**：事件流序列化之后输出的表，是一个异构流表（未分区的内存表/流数据表），至少包含三列：其中：

**eventTimeField** 可选，字符串标量或向量，用于指定事件时间的字段名字。如果所有事件的时间字段名都相同，则
*eventTimeField* 是一个标量，否则 *eventTimeField* 是一个向量，其长度和
*eventSchemes* 的长度一相同，每个元素分别代表每个事件的时间字段。

**commonField** 可选，字符串标量或向量，用于指定所有事件中具有相同名字的字段名称。在订阅时可以通过指定的字段对数据进行过滤。

## 返回值

返回一个表对象。

## 例子

```
class MarketData{
    market :: STRING
    code :: STRING
    price :: DOUBLE
    qty :: INT
    def MarketData(m,c,p,q){
        market = m
        code = c
        price = p
        qty = q
    }
}
class Orders{
    trader :: STRING
    market :: STRING
    code :: STRING
    price :: DOUBLE
    qty :: INT
    def Orders(t, m,c,p,q){
        trader = t
        market = m
        code = c
        price = p
        qty = q
    }
}
class Trades{
    trader :: STRING
    market :: STRING
    code :: STRING
    price :: DOUBLE
    qty :: INT
    def Trades(t, m,c,p,q){
        trader = t
        market = m
        code = c
        price = p
        qty = q
    }
}
share streamTable(array(STRING, 0) as eventType, array(BLOB, 0) as blobs) as events
serializer = streamEventSerializer(name=`serOutput, eventSchema=[MarketData, Orders, Trades], outputTable=events)
```
