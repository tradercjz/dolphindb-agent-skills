# pop!

## 语法

`pop!(X)`

## 详情

移除 *X* 中的最后一个元素。

## 参数

**X** 是一个向量。

## 返回值

一个标量，类型同 *X*，表示被移除的元素。

## 例子

```
x = 1 2 3;
pop!(x);
// output
3

x;
// output
[1,2]
```

**相关函数：**drop、removeHead!、removeTail!、remove!
