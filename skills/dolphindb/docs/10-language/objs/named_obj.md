<!-- Auto-mirrored from upstream `documentation-main/progr/objs/named_obj.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 命名对象

## 语法

```
<Object Definition> as <ObjectName>
```

命名对象是一个显示声明名称的对象。目前，命名对象仅限于向量。当向量绑定了变量时，向量将隐式使用变量名称作为向量对象名称。

## 例子

(1) 创建一个表

```
t = table(1..5 as id, rand(100, 5) as price);
t;
// t.id和t.price是命名对象
```

| id | price |
| --- | --- |
| 1 | 34 |
| 2 | 33 |
| 3 | 28 |
| 4 | 84 |
| 5 | 6 |

(2) SQL语句

```
select price as x from t;
```

| x |
| --- |
| 34 |
| 33 |
| 28 |
| 84 |
| 6 |

(3) 绘图

```
plot([1..10 as x, 21..30 as y], 2016.10.01..2016.10.10 as date)
```
