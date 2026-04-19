<!-- Auto-mirrored from upstream `documentation-main/rn/server/grafana.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# Grafana 数据源插件

DolphinDB 提供两种 Grafana 数据源插件：dolphindb-datasource 和
dolphindb-datasource-next。需要注意的是，dolphindb-datasource 插件自 3.0.1 版本起已停止维护。

## DolphinDB Datasource Next

### 新增功能

* 支持 Grafana v12.1~v12.4。（**3.0.500**）
* 支持 Grafana 11.5.2。（**3.0.400**）
* 新增对 Linux ARM64 架构的支持。（**3.0.300**）
* 支持 Grafana Alert （告警）功能。（**3.0.1**）
* 支持混合数据源查询，在同一个面板中合并来自多个数据源的数据（只支持非流数据）。（**3.0.1**）

### 功能优化

* 使用 Go 语言重写查询接口，提高并发查询性能。（**3.0.1**）

### 故障修复

* 修复查询完成后未及时关闭数据库连接的问题，从而导致内存持续占用。（**3.0.500**）
* 修复执行无返回值的脚本时出现报错的问题。（**3.0.300**）
* 修复整型空值未能正确显示为空的问题。（**3.0.300**）
* Grafana 仪表盘选择时区后，数据未能按所选时区显示。（**3.0.200**）
* 某些数据类型在值为空时显示错误。（**3.0.200**）

## DolphinDB Datasource

* 通过前端链接数据库。
* 使用 WebSocket 进行通信。
* 要求浏览器和数据库处于同一网络中。
