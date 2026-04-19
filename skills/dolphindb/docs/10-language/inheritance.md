<!-- Auto-mirrored from upstream `documentation-main/progr/inheritance.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 继承和多态

## 继承

在 DolphinDB 脚本中，虽然只支持单继承模式，即一个类仅能从一个父类继承，但得益于其动态语言的特性和鸭子类型（duck
typing）的概念，对象的类型由其行为决定，而非其继承关系。这意味着，即使没有多继承，一个类也能模拟多个类的特性，只要它实现了所需的方法和属性。

**用法**

在 DolphinDB
脚本中，类的继承允许派生类继承基类的属性和方法。但是，需要特别注意的是，派生类中的属性名必须是唯一的，不能与基类中的属性名重复。

```
class Base {
	alpha :: INT
	def Base(a) {
		alpha = a
	}
	def method() {
		print(alpha)
	}
}

class Derived : Base {
	beta :: INT
    // 派生类中的属性名不能和基类中的重复，会出现报错
//	alpha :: INT
	def Derived(a, b) {
		alpha = a
		beta = b
	}
	def method2() {
		method()
		// 可以使用基类中的属性
		print(alpha + beta)
	}
}

x = Derived(1,2)
x.method2()

//output: 1 3
```

在派生类中可以调用基类的构造函数。

```
class Base {
	alpha :: INT
	def Base(a) {
		alpha = a
	}
	def method() {
		print(alpha)
	}
}

class Derived : Base {
	beta :: INT
	def Derived(a, b) {
		Base(a)
		beta = b
	}
	def method2() {
		method()
	}
}

x = Derived(1,2)
x.method2()

//output: 1
```

## 多态

在类的定义中，方法的行为类似于 C++
中的虚函数，它们支持多态性。当派生类中出现与基类同名的方法时，派生类的方法将覆盖基类的方法。为了实现正确的方法覆盖（重写），派生类的方法必须与基类的方法具有相同的函数签名（参数列表和返回类型）是相同的。

```
class Base {
	def Base() {}
	def virtualMethod() {}
	def doSomething() {
		virtualMethod()
	}
}
class Derived : Base {
	alpha :: INT
	def Derived(a) {
		alpha = a
	}
	// override
	def virtualMethod() {
		print(alpha)
	}
}
d = Derived(100)
d.doSomething()

// output: 100
```
