<!-- Auto-mirrored from upstream `documentation-main/rn/server/datax_dolphindbreader_0.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# DataX-dolphindbreader

## 新功能

* 新增支持自动切分多任务。特别地，支持在配置 *querySql* 时自动切分多任务。（**1.30.22.3**）
* 新增支持数据类型 DECIMAL32、DECIMAL64、DECIMAL128。（**1.30.22.3**）
* 新增支持自定义配置项参数 querySql。（**1.30.22.2**）

## 功能优化

* 优化了内部实现逻辑。（**1.30.22.3**）

## 故障修复

* 字符串的长度超长的情况下导出数据报错。（**1.30.22.3**）
* 修复*channel* 参数配置问题。（**1.30.22.3**）
