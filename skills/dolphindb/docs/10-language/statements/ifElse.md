<!-- Auto-mirrored from upstream `documentation-main/progr/statements/ifElse.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# if-else

## 语法

```
if (condition){

statement

}

else{

statement

}
```

## 详情

"if"后面必须加上括号。如果一个分支需要执行多行语句，必须通过花括号{}将多条块语句括起来；一条语句的话，花括号可省略。

请注意，如果condition是NULL或者!NULL，则按照false处理，执行else语句。

## 例子

```
def temp(const a) {
    if (a>10)
        return a\10  //若只执行一条语句，花括号{}可以省略
    else if (a<=10 && a>1)
        return a
    else{
        b=abs(a)*10  //若需要执行多条语句，必须使用花括号括起来
        return b
    }
};

temp 10;
// output
10
temp 11;
// output
1.1
temp 0.5
// output
5
```
