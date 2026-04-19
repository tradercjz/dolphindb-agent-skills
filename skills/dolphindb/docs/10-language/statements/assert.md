<!-- Auto-mirrored from upstream `documentation-main/progr/statements/assert.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# assert

## 语法

`assert <expr>`

或

`assert <subCase>, <expr>`

## 参数

* **subCase** 是一个字符串。若值没有使用引号，也会被解析为字符串。
* **expr** 是一个布尔值或返回布尔值的表达式。

## 详情

*assert* 语句最适合用于单元测试。和注解一起使用可以打印输出测试用例的详细信息。

## 例子

```
@testing: case = "inner product"
assert [1,2,3]**[4,5,6]==32;

assert [1,2,3]**[4,5,6]==33;
// output
Testing case inner product failed

assert 1==2;
// output
Testing case adhocTesting failed

@testing: case = "equal"
assert "one", 1==2
assert "two", 3==4
```
