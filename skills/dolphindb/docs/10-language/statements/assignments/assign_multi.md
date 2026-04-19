<!-- Auto-mirrored from upstream `documentation-main/progr/statements/assignments/assign_multi.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 多变量赋值

多个值可一次性赋予多个变量。

```
x,y=1 2 3, 2:5;
x;
// output
[1,2,3]
y;
// output
2 : 5

x,y=(1 2 3, 2:5);
x;
// output
[1,2,3]
y;
// output
2 : 5

// 通过函数返回多个值，一次性对多个变量同时赋值
def foo(a,b): [a+b, a-b]
x,y = foo(15,10);
x;
// output
25
y;
// output
5

// 将一个值赋予多个变量
x,y=10;
x;
// output
10
y;
// output
10

// 通过使用矩阵的列来进行多值赋值。变量会按顺序获取矩阵的各列。变量数量必须等于矩阵列数。
x,y = 1..10$5:2;
x;
// output
[1,2,3,4,5]
y;
// output
[6,7,8,9,10]

// 通过表对多个变量赋值。将表中的每一行的值赋给一个变量，因此变量的数量必须等于表的行数。
t = table(1 2 3 as id, 4 5 6 as value, `IBM`MSFT`GOOG as name);
t;
```

| id | value | name |
| --- | --- | --- |
| 1 | 4 | IBM |
| 2 | 5 | MSFT |
| 3 | 6 | GOOG |

```
a,b,c = t;
a;
// output
name->IBM
value->4
id->1

b;
// output
name->MSFT
value->5
id->2

c;
// output
name->GOOG
value->6
id->3
```
