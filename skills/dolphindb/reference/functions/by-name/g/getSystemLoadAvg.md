# getSystemLoadAvg

## 语法

`getSystemLoadAvg()`

## 详情

返回实时系统平均负载。使用该函数前，需要启动性能监控，即在配置文件中把 *perfMonitoring* 设为1。

## 返回值

DOUBLE 类型标量。

## 例子

```
getSystemLoadAvg();

// output: 5.664062
```
