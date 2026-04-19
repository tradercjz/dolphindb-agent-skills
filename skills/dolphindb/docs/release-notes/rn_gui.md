<!-- Auto-mirrored from upstream `documentation-main/rn/rn_gui.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# GUI

Notice：

为提升用户体验，DolphinDB GUI 客户端的版本号现已调整。新的版本号与 DolphinDB Server 系列对齐，并向前兼容。

## 3.00.4.0

### 新增功能

* 脚本解析器新增 KDB Parser 选项。
* 支持高亮关键字 COMPUTE\_GROUP\_EXEC。
* 支持展示 INSTRUMENT、MKTDATA 类型数据。

### 故障修复

* 修复了在关闭确认页面时，系统错误释放共享变量的问题。
* 修复 array vector 类型列展示不正确的问题。

## 3.00.3.0

### 新增功能

* 新增支持 COMPUTE\_GROUP\_EXEC 关键字高亮。

## 3.00.2.3

### 故障修复

* 切换 server 后，点击登录按钮报错。
* 未登录状态下，状态栏不显示连接的 IP 和 port 信息。

## 3.00.2.2

### 功能优化

* 支持限制访客（guest）用户在 GUI 中可以执行的操作，以增强安全性。

### 故障修复

* 导出 CSV 文件时，数组向量格式错误。
* 导出 CSV 文件时，解析多条 SQL 语句错误。
* “Help>GUI Workbench Documentation” 按钮跳转错误。

## *3.00.2.1*

### 功能优化

* 支持显示 IOTANY 类型的 NULL 数据。

## *3.00.2.0*

### 新增功能

* 支持 IOTANY 向量类型。

### 功能优化

* 支持 outer join, OUTER JOIN 关键字高亮。

## *3.00.1.1*

### 功能优化

* Export Table 导出 CSV 文件时，将空值（null）显示为空白字段。

### 故障修复

* [DGUI-432] 使用 `plot` 画图时报错。

## *3.00.1.0*

### 新增功能

* 支持在日志中展示 Tensor 型数据。

## *3.00.0.0*

### 新增功能

* 支持 DECIMAL 类型的矩阵。
* 导出 CSV 的输入框支持：

  + 换行解析同条 SQL 语句。
  + 使用分号“;”划分不同 SQL 语句。

### 功能优化

* 支持 CATALOG、catalog 关键字高亮。
* 取消用单引号括起报错信息。
* 优化了长文本报错消息的展示。

### 故障修复

* 报错信息显示错误的脚本行号。
* 导出大数据量的 CSV 文件时进度条显示错误。
* 导出 CSV 文件时获取 `count` 值报错。

## *2.00.11.1*

### 故障修复

* 修复错误码的异常跳转链接。
* 修复调用 plot 时，在参数 *extras* 中指定 *multiYAxes* 为 false 未生效的问题。

## *2.00.11.0*

### **新增功能**

支持将交易所标识相关的时间表示处理为 DURATION 类型。

## *2.00.10.1*

### 故障修复

修复大表数据展示卡顿的问题。

## *1.30.22.2*

### 新增功能

* 新增支持定时自动保存文件功能，时间间隔为5s。
* 新增支持展示 Data Browser 中某一单元格对应的所有数据功能。
* 新增支持上传 CSV 文件为内存表、并配备引导确认其 schema 的功能。
* 新增支持加密存储用户名、密码等敏感信息。
* 新增支持 Log 打印过长信息自动换行功能。

### 功能优化

* 优化了连接失败时的报错信息。
* 优化了同步文件到 server 失败时的报错信息，将说明具体失败原因。
* 优化了使用 `plot` 函数生成图像时：

  + 若横坐标为时间类型，右侧数轴保留。
  + 删去了折线图中折点默认添加的符号。
* Log 和 Data Browser 中若展示负数或 DECIMAL32/64/128类型数据，整数部分使用标准的千位分隔符（逗号）。

### 故障修复

* 修复连接失败时 GUI 冻结的问题，新增了重连时间限制。
* 修复 `rename` 文件名后实际文件系统中未对应修改的问题。
* 修复 Python Parser 解析模式下创建维度表报错的问题。
* 修复若 Data Browser 中某一单元格数据为负数，其拷贝结果不正确的问题。

## *1.30.22.1*

### 新增功能

* 新增支持 DECIMAL128 数据。
* 语言选择下拉框新增 Oracle、MySQL 选项。
* 新增支持 select Null 语句。
* 新增支持以下关键字高亮。

  JOIN、FULL
  JOIN、LEFT SEMI JOIN、DECIMAL128、DATEHOUR、IS、CREATE DATABASE、create
  database、inner join、sub、full outer join、right outer join、left outer
  join、drop table、if exists 、drop database、update...set、alter xxx
  drop/rename/add、create table、nulls first
* 新增 refresh 选项 ，支持刷新功能。
* 新增加密同步选项“Synchronize module to server”，支持同步 module 到
  server 并保存为加密 .dom 文件。

### 功能优化

优化了 #include 导入脚本的逻辑。

## *1.30.21.3*

### 故障修复

修复了同步 modules 时目标路径错误的问题。

## *1.30.21.1*

### 功能优化

* 支持将内存表以 DolphinDB 私有格式保存到本地或上传至服务器。
* 支持部分标准 SQL 的关键字高亮。
* 支持查看 DECIMAL 类型数据。
* 支持 DECIMAL32 和 DECIMAL64 关键字高亮。
* 支持查看列类型为 ANY VECTOR 的表。

### 故障修复

* 修复了 Data Browser 中 NULL 值显示不正确。
* 修复了解析服务器返回的 month(0)~month(11) 的结果显示数据不正确。

## *1.30.19.2*

### 新增功能

增加export前的路径检查功能。

### 功能优化

* 当 Server 重启后，实现 GUI 自动重连。
* 优化export table信息显示，在GUI下方的log窗口中显示成功与失败的文件。

### 故障修复

修复 python 模式下，GUI 端运行 nanotimestamp(-1)出现计算错误的问题。

## *1.30.19.1*

### 功能优化

优化报错信息显示。

### 故障修复

修复通过 GUI 变量浏览器无法查看 array vector 类型变量的问题。

## *1.30.13*

### 功能优化

GUI 画图函数 plot 多曲线可共享y轴。

## 其他说明

* 1.30 及以上版本的 Server 不兼容低于 1.30.0 版本的 GUI，请从官网下载最新版本 GUI 客户端。
* 1.30.7 及以上版本的 Server, 需要配合 GUI1.30.7 版本使用 DURATION 类型。
