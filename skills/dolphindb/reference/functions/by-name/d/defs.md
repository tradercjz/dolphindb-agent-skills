# defs

## 语法

`defs([X])`

## 详情

查询系统中所有函数信息。

## 参数

**X**
可选参数，是一个是字符串，用于匹配函数名，支持通配符"%"和"?"。"%"表示0，1或多个字符，“?”表示1个字符。

## 返回值

返回一个表：

* 如果没有指定 *X*，返回系统的所有函数信息。
* 如果指定了 *X*，返回匹配 *X* 的所有函数信息。

## 例子

```
defs();
```

| name | isCommand | userDefined | minParamCount | maxParamCount | syntax |
| --- | --- | --- | --- | --- | --- |
| !=\_2 | 0 | 0 | 2 | 2 | (X, Y) |
| !\_1 | 0 | 0 | 1 | 1 | (X) |
| $\_2 | 0 | 0 | 2 | 2 | (obj, type) |
| %\_2 | 0 | 0 | 2 | 2 | (X, Y) |
| &&\_2 | 0 | 0 | 2 | 2 | (X, Y) |
| &\_2 | 0 | 0 | 2 | 2 | (X, Y) |
| \*\*\_2 | 0 | 0 | 2 | 2 | (X, Y) |
| \*\_2 | 0 | 0 | 2 | 2 | (X, Y) |
| +\_2 | 0 | 0 | 2 | 2 | (X, Y) |
| -\_1 | 0 | 0 | 1 | 1 | (X) |
| ... |  |  |  |  |  |

```
typestr defs();
// output
IN-MEMORY TABLE;

select * from defs() where name like "bit%";
```

| name | isCommand | userDefined | minParamCount | maxParamCount | syntax |
| --- | --- | --- | --- | --- | --- |
| bitAnd | 0 | 0 | 2 | 2 | (X, Y) |
| bitNot | 0 | 0 | 1 | 1 | (X) |
| bitOr | 0 | 0 | 2 | 2 | (X, Y) |
| bitXor | 0 | 0 | 2 | 2 | (X, Y) |

```
defs("bit%");
```

| name | isCommand | userDefined | minParamCount | maxParamCount | syntax |
| --- | --- | --- | --- | --- | --- |
| bitAnd | 0 | 0 | 2 | 2 | (X, Y) |
| bitNot | 0 | 0 | 1 | 1 | (X) |
| bitOr | 0 | 0 | 2 | 2 | (X, Y) |
| bitXor | 0 | 0 | 2 | 2 | (X, Y) |

```
defs("%sin");
```

| name | isCommand | userDefined | minParamCount | maxParamCount | syntax |
| --- | --- | --- | --- | --- | --- |
| asin | 0 | 0 | 1 | 1 | (X) |
| sin | 0 | 0 | 1 | 1 | (X) |

```
defs("?sin");
```

| name | isCommand | userDefined | minParamCount | maxParamCount | syntax |
| --- | --- | --- | --- | --- | --- |
| asin | 0 | 0 | 1 | 1 | (X) |
