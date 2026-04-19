# attributeTypes

首发版本：3.00.4.2，3.00.3.2

## 语法

`attributeTypes(obj)`

## 参数

**obj** 类实例。

## 详情

获取类或类实例中所有属性及其对应的类型。

## 返回值

一个表，包含如下列：

* attr：属性名称。
* type：数据类型。

## 例子

```
class Person {
	name :: STRING
	age :: INT
	def Person(name_, age_) {
		name = name_
		age = age_
	}
}
p1 = Person("Sam", 12)
attributeTypes(p1)  // 或者 attributeTypes(Person)
```

| attr | type |
| --- | --- |
| name | STRING |
| age | INT |

**相关函数**：attributeNames、attributeValues
