<!-- Auto-mirrored from upstream `documentation-main/progr/member_function.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 成员方法

成员方法，也称为成员函数，是定义在类内部的函数，用于操作类的对象数据。成员方法可以访问类的成员变量，并提供了对对象进行操作的接口。

**语法**

```
class Volume{
	def Volume() {
	}
	//定义了类 Volume 的成员方法。它接受 self 参数，用于表示对象实例本身。
	def testSelf() {
		print(self)
	}
}
```

## 声明、定义分离

在 DolphinDB
类中，允许先声明一个函数或变量，然后在其他地方再进行函数的定义。在调用方法之前，该方法必须至少在代码中先进行声明或定义。同时，成员变量必须在方法之前声明。

```
class Test1 {
	def Test1() {}
	// 声明 b1 方法但是没有进行定义
	def b1()

	def a1() {
		// 定义 a1 函数，在此可调用 b1
		b1()
	}
	// 定义 b1
	def b1() {
		print("test")
	}
}
```

**变量的解析顺序**

在 DolphinDB 中，当成员方法中使用到变量时，解析顺序如下：

1. **方法参数**：当在方法内部引用一个变量时，首先会查找函数参数是否与该变量同名，如果是，则解析为函数参数。下例中，在
   `method` 方法中，引用了变量 b，该方法的参数名也是 b，因此 b 被解析为
   `method` 的参数。
2. **对象属性**：如果方法参数中没有同名变量，将会访问对象的属性，即成员变量。如果变量名称与对象的属性名称相同，则解析为对象的属性。下例中，在
   `method` 方法中，方法内部未定义变量 a，因此继续查询对象属性，查询到存在成员变量
   a，因此最终打印对象属性 a 的值。
3. **共享变量**：如果变量既不与方法参数同名，也不与成员变量同名，则会查询类定义外部的共享变量。
4. **变量不存在** ：经过以上3个步骤都没有找到同名的变量，将报错提示变量不存在。

```
share table(1:0, `sym`val, [SYMBOL, INT]) as tbl
go

class Test2 {
  a :: INT
  b :: DOUBLE

  def Test2() {
    a = 1
    b = 2.0
  }

  def method(b) {
    print(b) // 解析为函数参数b
    print(a) // 解析为对象属性a
    print(tbl) // 解析为共享变量tbl
    print(qwert) // 变量不存在，报错
  }
}
```

这种顺序保证了在成员方法中使用变量时遵循就近原则，即首先考虑方法参数，其次是对象的成员变量，最后是共享变量，确保在成员方法中对变量的引用和赋值都符合预期的逻辑

## self 引用

通过 `self` 变量，可以在类的方法中引用当前实例化的对象。这种方法类似于 Python 中的 self，Java、C++ 语言中的
this 指针。

```
class Volume{
	a :: INT
	b :: INT
	def Volume() {
		a = 1
		b = 2
	}
	def testSelf() {
		print(self)
	}
}

a = Volume()
a.testSelf()

// output: <Instance of Class '::Volume'
```

注意，当前 DolphinDB 类不支持以下操作：

* 不支持通过 self 修改对象的属性值，即不支持 `self.属性名 = newValue`。
* 不支持通过 `obj.name=newValue` 直接设置对象的属性值。可以借助
  `setAttr` 函数来设置对象的属性值。

## 部分应用

部分应用是 DolphinDB 语言的一个重要特性，其应用很广泛，因此在 DolphinDB 语言中，类的方法可以通过部分应用（partial
application）的方式被调用。通过 { } 固定部分参数，生成部分应用。接着上例中定义的类，我们使用 {}
固定参数：

```
a = Person("Harrison",20)
f = a.getName{2015}
f(true)

// output: 2015
```

## 特殊成员方法

* `str()` 方法：通过 `print()` 函数打印对象，会打印该方法的返回结果。
* `repr()` 方法：通过 VSCode，web，GUI 等运行对象，会打印
  `repr()` 的返回结果。

如果类中没有定义这两个方法，则打印对象时将返回 <Instance of Class '类名'>。
