<!-- Auto-mirrored from upstream `documentation-main/progr/statements/for.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# for

for语句用于循环遍历向量、矩阵或表中的元素。

## 语法

```
for(s in X)

{

statements

}
```

## 详情

类似"If-Else"，for后面的括号是必须的。若循环体中需要执行多条语句，那么必须用花括号{}；只有一条语句时，花括号可省略。

X
可以是数据对、向量、矩阵或表。for循环以列为单位遍历一个矩阵，以行为单位遍历一个表。当遍历矩阵时，每一列以向量的形式表示；当遍历表时，每一行以字典表示，该字典以列名作为key，以单元格值作为value。

## 例子

遍历数据对：

```
for(s in 2:4){print s};
// output
2
3
for(s in 4:1) print s;
// output
3
2
1
```

遍历向量：

```
x=4 0 1 3;
for(s in x) print s;
// output
4
0
1
3
```

逐列遍历矩阵：

```
m=1..6$3:2;
m;
```

| #0 | #1 |
| --- | --- |
| 1 | 4 |
| 2 | 5 |
| 3 | 6 |

```
for(s in m){print s};
// output
[1,2,3]
[4,5,6]
```

逐行遍历表：

```
x = 1 2 3
y = 4 5 6
t = table(x,y)
for(s in t) print s;
// output
y->4
x->1

y->5
x->2

y->6
x->3
```
