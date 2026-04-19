# disableDynamicScriptOptimization

## 语法

`disableDynamicScriptOptimization()`

## 详情

关闭脚本引擎优化。

此命令须在控制节点由管理员执行。

此命令的影响将在系统重启后失效。若要永久生效，请在配置文件（集群模式为 controller.cfg，单节点模式为 dolphindb.cfg）中修改配置参数
*enableDynamicScriptOptimization*
。

## 例子

```
disableDynamicScriptOptimization()
```

**相关函数：**
enableDynamicScriptOptimization
