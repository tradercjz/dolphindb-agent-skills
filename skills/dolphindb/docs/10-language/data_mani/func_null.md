<!-- Auto-mirrored from upstream `documentation-main/progr/data_mani/func_null.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 函数和空值

在二元函数或二元运算符中，如果涉及空值操作，结果也将是空值。

```
x = 1.0 + 5.6 * 3 + NULL + 3
isNull(x)
// output: 1
typestr x;
// output: DOUBLE

5 + NULL      //返回空值

x=1 2 NULL NULL 3;
y=2 NULL NULL 3 4;
x+y;
// output: [3,,,,7]

false || 00i     //返回空值
true && 00i      //返回空值
```

在比较运算符
`>`、`>=`、`<`、`<=`、`between`
中，空值默认被视为最小值。如果希望空值与其他值的比较结果仍为逻辑空值，则需将配置参数 *nullAsMinValueForComparison* 设置为
false。然而，比较运算符 `!=`、`<>`、 `==`
不受该配置参数的影响，空值始终被视为最小值。因此，在 DolphinDB 中，比较两个空值是否相等时返回 true，而比较两个空值是否不相等时返回 false。

```
// nullAsMinValueForComparison = true
1 < NULL // output: false
1 > NULL // output: true
NULL == NULL // output: true
NULL != NULL // output: false

// nullAsMinValueForComparison = false
1 < NULL // output: 00b
1 > NULL // output: 00b
NULL == NULL // output: true
NULL != NULL // output: false
```

逻辑运算符 `and` 和 `xor`
的行为与一般的四则运算相同，只要有一个操作数为空值，结果也为空值。

```
false || 00i     //返回空值
true && 00i      //返回空值
```

逻辑运算符 `or`
的规则稍有不同：在默认情况下（*logicOrIgnoreNull*=true），如果只有一个操作数为空，结果等于另一个非空操作数。若两个操作数均为空，则返回空值。当设置
*logicOrIgnoreNull*= false 时，若有一个操作数为空，结果将返回空值。

```
// logicOrIgnoreNull = true
NULL or true // output: true
NULL or false // output: false
NULL or NULL // output: 00b

// logicOrIgnoreNull = false

NULL or true // output: 00b
NULL or false // output: 00b
NULL or NULL // output: 00b
```

聚合函数如 `sum`/`avg`/`med`
通常忽略空值。同样，内部使用了聚合函数的向量函数如 `msum / cumsum` 也遵循这一规则。

```
x = 1 2 NULL NULL 3;
log x;
// output: [0,0.693147,,,1.098612]

avg x;
// output: 2

sum x;
// output: 6

med x;
// output: 2

cumsum(x)
// output: 1 3 3 3 6
```

在部分函数，如`ols`、`olsEx`、`corrMatrix`、`olsEx`
中，空值会被替换为 0。

```
m = take(rand(10.0, 20) join NULL, 30) $10:3
corrMatrix(m)
```

| col1 | col2 | col3 |
| --- | --- | --- |
| 1 | -0.13 | -0.0463 |
| -0.13 | 1 | 0.5853 |
| -0.0463 | 0.5853 | 1 |
