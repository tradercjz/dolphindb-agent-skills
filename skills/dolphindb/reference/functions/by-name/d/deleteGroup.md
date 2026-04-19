# deleteGroup

## 语法

`deleteGroup(groupName)`

## 详情

删除一个群组。这可能会影响群组内所有成员的权限。

注：

该函数只能由管理员在控制节点、数据节点和计算节点运行。

## 参数

**groupName** 是表示群组名称的字符串。

## 返回值

无。

## 例子

```
deleteGroup(`Production);
```

**相关信息**

* [deleteGroupMember](deleteGroupMember.html "deleteGroupMember")
* [deleteUser](deleteUser.html "deleteUser")
