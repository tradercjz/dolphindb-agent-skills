# getGroupsByUserId

## 语法

`getGroupsByUserId(userId)`

## 详情

查询用户所在的组。

注：

该函数只能由管理员在控制节点、数据节点和计算节点运行。

## 参数

**userId** 是表示用户名的字符串。

## 返回值

字符串向量。

## 例子

```
getGroupsByUserId("admin")

// output: ["MVP","MYMVP"]
```
