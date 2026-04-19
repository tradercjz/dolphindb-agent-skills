<!-- Auto-mirrored from upstream `documentation-main/progr/statements/doWhile.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# do-while

## 语法

```
do{

[statements]

}

while (conditions);
```

## 详情

do-while循环首先执行do语句，然后检查循环体中的条件，保证循环体至少被执行一次。语句不能以"while"开头。do-while语句中都是必须使用圆括号()和花括号{}。

请注意，如果conditions是NULL或者!NULL，则按照false处理。

## 例子

```
x=1
do {x+=2} while(x<100)
x;
// output
101

x=1
y=0
do {x+=y; y+=1} while(x<100 and y<10);
x;
// output
46
y;
// output
10
```
