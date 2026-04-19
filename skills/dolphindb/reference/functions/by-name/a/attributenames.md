# attributeNames

## 语法

`attributeNames(obj)`

## 详情

获取类实例的所有属性名称。

## 参数

**obj** 类实例。

## 返回值

字符串向量

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

p = Person("Sam", 12)
attributeNames(p)

// output: ["name","age"]
```
