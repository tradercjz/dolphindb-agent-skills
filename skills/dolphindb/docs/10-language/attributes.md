<!-- Auto-mirrored from upstream `documentation-main/progr/attributes.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 成员变量

成员变量是类中定义的变量。它们属于类的实例,每个实例都有自己的一套成员变量。成员变量可以在类的方法中访问和修改。

## 声明成员变量

成员声明时需要指定成员变量的类型，在 DolphinDB 中根据变量的数据不同，声明方法也不同：

**标量**

标量包括基本的数据类型，如 INT, CHAR, FLOAT, DOUBLE, STRING 等。声明方式为：`变量名 ::
数据类型`。例如：`age :: INT`、`name ::
STRING`。

**常规向量**

在声明常规向量的成员变量时，其方式与声明标量相似，但需在数据类型后添加 VECTOR
以指明该成员变量为一个常规向量。声明方式为：`变量名 :: 数据类型
VECTOR`。例如：`age :: INT
VECTOR`、`name :: STRING VECTOR`。

**数组向量**

在声明数组向量的成员变量时，其方式与声明常规向量相似，但需在数据类型后添加 []
以指明该成员变量为一个数组向量。声明方式为：`变量名 :: 数据类型[]
VECTOR`。例如：`age :: INT[] VECTOR`。

## 获取成员变量

提供
`attributeNames`、`attributeValues`、`attributeTypes`方法，可以获取类实例的所有成员变量名称、属性值、成员变量类型。

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

attributeValues(p)
/* output:
name->Sam
age->12
*/

attributeTypes(p)
```

| attr | type |
| --- | --- |
| name | STRING |
| age | INT |
