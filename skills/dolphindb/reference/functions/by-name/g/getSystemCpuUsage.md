# getSystemCpuUsage

## 语法

`getSystemCpuUsage()`

## 详情

返回当前节点上 DolphinDB 进程实时占用 CPU 的百分比。

注意，若 DolphinDB 进程占用多个 CPU，则返回各个 CPU 占用率的总和。

## 参数

无

## 返回值

DOUBLE 标量。

## 例子

```
getSystemCpuUsage();

// output: 1.771654
```
