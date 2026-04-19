# getOrcaDataLineage

首发版本：3.00.4

## 语法

`getOrcaDataLineage(name)`

## 详情

查询流图中指定公共流表的数据血缘关系，包括当前及曾经存在的历史血缘。

**当** ***name*** **是一个表名**，返回一个 JSON 对象，包含该数据表所在的每个流图中其上游依赖的节点信息。

每个流图的 key 是流图内部名称，value 是该流图的属性以及上游节点：

* fqn：字符串标量，表示该流图的全限定名。
* isDeleted：布尔值，指示该流图是否已被删除。
* 每个节点的 key 是节点名称，value 是该节点的属性，包括：

  + isRoot：布尔值，指示该节点是否为根节点。
  + parent：字符串向量，包含该节点所有直接父节点名称。若为根节点，则为空数组 `[]`。
  + isTable：布尔值，指示该节点是否为数据表。
  + isEngine：布尔值，指示该节点是否为引擎。

**当** ***name*** **是一个 TimerEngine 名**，返回一个 JSON 对象，包含以下字段：

* input：引擎 *func* 的输入参数信息，键为参数名，值为数据类型。若无入参，则为 `{}`。
* output：引擎 *func* 的返回值信息，

  + 若返回值是 TABLE 标量，则键为字段名，值为字段类型。
  + 若返回值是其他形式的标量，则键为 "return"，值为数据类型。
  + 其他情况，键为 "return"，值为数据形式。

## 参数

**name** STRING 类型标量，表示需要查询的公共流表名称或 timerEngine 名。表名称支持两种格式：

* 完全限定名，例如 `"catalog_name.orca_table.table_name"`
* 内部名称格式，例如
  `"public_stream_table_05056f34_92b0_16b2_204e_c3c63e3f8a84"`

## 返回值

一个 JSON 对象。

## 例子

```
// 创建并提交流图
createCatalog("test")
go
use catalog test

def myFunc(x,y,z){
    return table(x as col1,y as col2,z as col3)
}
a = ["aaa"]
b = ["bbb"]
c = ["ccc"]
t = table(1..100 as id, 1..100 as value, take(09:29:00.000..13:00:00.000, 100) as timestamp)

g1 = createStreamGraph("factor1")
g1.source("snapshot1", schema(t).colDefs.name, schema(t).colDefs.typeString)
  .reactiveStateEngine([<cumsum(value)>, <timestamp>])
  .setEngineName("rse1")
  .timerEngine(3, myFunc, a, b, c)
  .setEngineName("myJob")
  .buffer("end")
g1.submit()

g2 = createStreamGraph("factor2")
g2.source("snapshot2", schema(t).colDefs.name, schema(t).colDefs.typeString)
  .reactiveStateEngine([<cumsum(value)>, <timestamp>])
  .setEngineName("rse2")
  .buffer("end")
g2.submit()

// 删除流图 factor2
dropStreamGraph("factor2")

// 查询血缘
getOrcaDataLineage("test.orca_table.end")
/*
{
  "40d12999-f8f3-9cb5-4a49-813bdee46a9f": {
    "fqn": "test.orca_graph.factor1",
    "isDeleted": false,
    "test.orca_engine.rse1": {
      "isRoot": false,
      "isTable": false,
      "isEngine": true,
      "parents": [
        "test.orca_table.snapshot1"
      ]
    },
    "test.orca_table.end": {
      "isRoot": false,
      "isTable": true,
      "isEngine": false,
      "parents": [
        "test.orca_engine.rse1"
      ]
    },
    "test.orca_table.snapshot1": {
      "isRoot": true,
      "isTable": true,
      "isEngine": false,
      "parents": []
    }
  },
  "4cee4ed3-007b-f38a-8743-f6776a6172d9": {
    "fqn": "test.orca_graph.factor2",
    "isDeleted": true,
    "test.orca_engine.rse2": {
      "isRoot": false,
      "isTable": false,
      "isEngine": true,
      "parents": [
        "test.orca_table.snapshot2"
      ]
    },
    "test.orca_table.end": {
      "isRoot": false,
      "isTable": true,
      "isEngine": false,
      "parents": [
        "test.orca_engine.rse2"
      ]
    },
    "test.orca_table.snapshot2": {
      "isRoot": true,
      "isTable": true,
      "isEngine": false,
      "parents": []
    }
  }
}
*/

// 查看 timerEngine func
getOrcaDataLineage("test.orca_engine.myJob")
/*
{
  "input": {
    "x": "STRING",
    "y": "STRING",
    "z": "STRING"
  },
  "output": {
    "col1": "STRING",
    "col2": "STRING",
    "col3": "STRING"
  }
}
*/
```
