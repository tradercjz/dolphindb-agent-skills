<!-- Auto-mirrored from upstream `documentation-main/progr/sql/setTraceMode.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# setTraceMode

## 语法

`setTraceMode(mode)`

## 参数

**mode** 布尔值，用于开启或关闭 SQL Trace。

## 详情

该命令用于控制 SQL Trace 功能的开启或关闭。

注：

* 一次完整的跟踪流程必须以 setTraceMode(true) 作为开启标识，并以
  setTraceMode(false) 作为结束标识。
* DolphinDB
  从开启跟踪功能后的接收到的第一次请求开始进行跟踪。因此该命令必须单独执行，而不能和待跟踪的语句放在一个脚本中一起执行。
