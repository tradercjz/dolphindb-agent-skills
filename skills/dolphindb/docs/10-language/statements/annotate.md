<!-- Auto-mirrored from upstream `documentation-main/progr/statements/annotate.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 注解

注解主要在单元测试中使用，在当前会话中生成数据对，用于打印输出一个测试用例的细节。

## 语法

```
@<topic>:<sub_topic1>=<expr1>,
<sub_topic2>=<expr2>,
...
```

## 例子

```
1:3+1;
ct = count(1..10)
assert ct == 11;
// output
Testing case testing count failed

@testing:case="function_and_ex", exception=1;

@testing_case;
// output
function_and_ex

@testing_exception;
// output
1
```
