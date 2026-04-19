<!-- Auto-mirrored from upstream `documentation-main/progr/class_objects.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 类和对象

类定义了对象的属性（成员变量），构造方法和行为（成员方法）。在深入介绍类的定义和使用之前，让我们先了解 DolphinDB 对类的一些约定：

1. 类的命名规范：类名不能以数字开头，不能包含空格，或除了下划线（`_`）外的其他特殊字符。
2. 成员声明顺序要求：在调用方法之前，该方法必须至少在代码中先进行声明或定义。同时，且成员变量必须在方法之前声明。
3. 避免命名冲突：DolphinDB 中类名、共享表名和函数名共享同一命名空间。后定义的对象会覆盖先定义的同名对象，因此建议使用不同的命名规则来避免冲突。
4. DolphinDB 中不支持 const 关键字，类的成员函数均可能修改对象属性，因此无法应用于只读对象。

## 类的定义

**语法**

```
class ClassName{
    // 类的属性（成员变量）
    attribute1 :: dataType
    attribute2 :: dataType

    // 类的构造方法，和类名同名的构造函数，有且只有一个
    //参数名不能和属性名相同，否则会覆盖属性名
    def ClassName(parameter1, parameter2){
        attribute1 = parameter1
        attribute2 = parameter2
    }
    // 类的方法（成员方法）
    def method1(){
        // 方法的实现
    }
    def method2(parameter){
        // 方法的实现
    }
}
```

其中，attribute1, attribute2 表示成员变量名；dataType 表示变量的类型；parameter1, parameter2
表示构造函数的参数。

**注意事项**

* 暂不支持 JIT。
* 暂不支持析构函数。

以下定义一个名为 `Person`
的类：

```
class Person {
  name :: STRING
  age :: INT
  def Person(name_, age_) {
    name = name_
    age = age_
  }
  def setName(newName) {
    name = newName
  }
  def getName(year, gender) {
          if(year<2020)
                  return year
    else
            return name
  }
}
```

## 实例化对象

类是对象的抽象定义，而对象是类的具体实例化。

以下示例实例化 `Person` 类的对象：

```
a = Person("Harrison",20)
```
