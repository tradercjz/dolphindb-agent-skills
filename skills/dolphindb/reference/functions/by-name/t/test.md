# test

## 语法

`test(scriptFile, [outputFile], [testMemLeaking=false])`

## 详情

用于单元测试的系统命令。该命令必须要用户登录后才能执行。

如果 *scriptFile* 是一个目录，将执行测试目录中所有脚本文件，不会执行子目录中的文件。

如果 *outputFile* 没有指定，测试结果将会显示在屏幕上。如果 *outputFile* 指定为相对路径，则测试结果文件输出到
<HomeDir>。

## 参数

**scriptFile** 是字符串，表示服务器端的测试脚本文件或目录。可以是相对路径或绝对路径。

**outputFile** 是字符串，表示服务器端的测试结果输出文件。可以是相对路径或绝对路径。

**testMemLeaking** 是布尔值，表示是否测试内存泄漏。

## 返回值

无。

## 例子

```
test("/home/Data/test.dos", "/home/Data/result.dos");
test("/home/Data");
```
