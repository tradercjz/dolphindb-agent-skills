<!-- Auto-mirrored from upstream `documentation-main/progr/data_types_forms/Pair.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 返回：
"Hello" : "World"
```

## 访问数据对

用 X[Y] 的形式访问数据对数据。Y 可以是整数也可以是整数向量，或者数据对。例如：

```
x = 3:6;
x[1];
```

返回：6

```
x[0 1];
```

返回：[3,6]

## 修改数据对

数据对中的两个值可以分别被修改。例如：

```
x=3:6;
x[0]=4;
x;
```

返回：4:6

```
x=3:6+1;
x;
```

返回：4:7
