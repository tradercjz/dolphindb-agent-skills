<!-- Auto-mirrored from upstream `documentation-main/rn/server/datax_writer.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# DataX-dolphindbwriter

## 新功能

* 新增配置参数 *writeTimeout*，支持设置任务执行的超时时间。（**1.30.22.4**）
* 新增支持写入 DECIMAL32, DECIMAL64, DECIMAL128 类型数据。（**1.30.22.1**）
* 新增配置参数 *preSql*，支持在插入数据前预执行一段脚本。（**1.30.21.5**）
* 新增配置参数 *postSql*，支持在插入数据后预执行一段脚本。（**1.30.21.5**）
* 新增配置参数 *userName*，指定 DolphinDB 的用户名，与原有参数 *userId*
  兼容。（**1.30.21.5**）
* 新增配置参数 *passWord*，指定 DolphinDB 用户名的对应密码，与原有参数 *pwd*
  兼容。（**1.30.21.5**）

## 功能优化

* 优化 *preSql* 和 *postSql* 的执行逻辑。（**1.30.22.4**）
* 执行 *preSql* 报错时终止当前任务并抛出异常。（**1.30.22.4**）
* 将 fastjson 库从版本 1.1.46sec01 更新至 1.2.83。（**1.30.22.3**）
* 优化部分报错信息。（**1.30.22.2**）
* 当 STRING 和 BLOB 类型数据超过指定类型最大长度时，将其截断至最大长度。（**1.30.22.1**）
* *batchSize* 参数默认值从 10,000,000 修改为 100,000 以避免发生
  OOM。（**1.30.22.1**）

## 故障修复

* 故障修复：修复当连接出现异常时，未抛出正确报错信息的问题。（**1.30.21.5**）
