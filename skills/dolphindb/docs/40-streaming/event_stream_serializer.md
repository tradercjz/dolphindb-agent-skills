<!-- Auto-mirrored from upstream `documentation-main/stream/event_stream_serializer.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 事件流序列化与反序列化

## 事件流序列化器

事件流序列化器（Stream Event Serializer）负责将来自各种数据源的实时事件流序列化并写入 DolphinDB
异构流数据表，方便进行网络传输和数据持久化。事件流序列化发生在以下两个地方：

* 在将事件注入 CEP 引擎之前，需要先将其序列化为 BLOB 格式写入异构流表中。
* CEP 子引擎对事件处理后，需要输出到一个异构流表以供后续操作使用。

可使用 `streamEventSerializer` 函数定义事件流序列化器。

**详情**

将事件序列化为 BLOB 格式，写入到异构流表。

**语法**

```
streamEventSerializer(name, eventSchema, outputTable, [eventTimeField], [commonField])
```

**参数**

**name** 字符串，表示序列化引擎的名称，可包含字母，数字和下划线，但必须以字母开头。

**eventSchema** 可以是事件类型定义或一个表。用于指定进行序列化的事件及其声明的成员变量。

* 如果指定为事件类型定义，则可以指定为一个或多个事件类型定义。例如：定义了两个事件类型类，event1 和 event2，则可指定为
  *eventSchema*=[event1, event2]
* 如果指定为表，则必须具有如下表结构（可通过 `getCEPEngineStat(engine).eventSchema` 获得
  CEP 引擎中所有事件的结构）：

| 列名 | 含义 |
| --- | --- |
| eventType | 字符串，表示事件类型 |
| eventField | 字符串，表示事件类型中所声明的字段名。多个字段名之间以逗号（,）分隔 |
| fieldType（可选） | 字符串，表示 eventField 中各字段对应的数据类型的名称，多个名称之间以逗号（,）分隔 |
| fieldTypeId | 整型数组向量，表示 eventField 中各字段对应的数据类型的 ID。 |
| fieldFormId | 整型数组向量，表示 eventField 中各字段对应的数据形式的 ID。整型数组向量，0：标量；1：向量；2：数据对；3：矩阵；4：集合；5：字典；6：表  注意：目前只能指定标量和向量。 |

**outputTable**：事件流序列化之后输出的表，是一个异构流表（未分区的内存表/流数据表），至少包含三列：

其中：

* 如果指定 *eventTimeField*，第一列为时间戳；
* 第二列为 STRING 类型，表示事件类型；
* 第三列为 BLOB 类型，用于存储事件序列化后的结果。
* 此外，若如果指定了 *commonField*，则输出由它指定的列。

**eventTimeField** 可选，字符串标量或向量，用于指定事件时间的字段名字。如果所有事件的时间字段名都相同，则
*eventTimeField* 是一个标量，否则 *eventTimeField* 是一个向量，其长度和
*eventSchemes* 的长度一相同，每个元素分别代表每个事件的时间字段。

**commonField** 可选，字符串标量或向量，用于指定所有事件中具有相同名字的字段名称。在订阅时可以通过指定的字段对数据进行过滤。

## 事件流反序列化器

事件流反序列化器（Stream Event Deserializer）将序列化的流事件数据转换回原始事件对象。CEP 引擎内部实现了
StreamEventDeserializer，因此无需额外定义反序列化器，引擎便会自动反序列化从订阅的异构流表中获取到的数据。
