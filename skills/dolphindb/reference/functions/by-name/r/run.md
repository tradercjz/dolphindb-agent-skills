# run

## 语法

`run(scriptFile, [newSession=false],
[clean=true])`

## 详情

执行一个已经保存的程序文件。

如果设置 *newSession* = false，程序文件在当前 session 中运行。如果设置
*newSession* = true，程序文件在新开的 session 中运行。运行结束，关闭该 session。

**注意**：该命令必须要用户登录后才能执行。非管理员用户执行该命令须满足以下条件：（1）获得 SCRIPT\_EXEC 权限；（2）配置项 *strictPermissionMode* 为 false（即默认值）。

## 参数

**scriptFile** 是服务器端的脚本所在路径。

**newSession** 是否新开一个 session 运行脚本。

**clean** 是否清理当前 session 中的变量。默认为 true，即 `run`
运行后会清除变量。

## 例子

```
run "/home/DolphinDB/test.dos";

d = dict(STRING, ANY)
d["TradePrice"] = 1..1000
// clean 参数设置为 false，当前 session 中定义的变量 d 不会被清除。
run("/home/DolphinDB/test.dos", clean=false)
parseExpr("avg(TradePrice)",d).eval()
// output
500.5
```
