<!-- Auto-mirrored from upstream `documentation-main/rn/compat3.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 三级兼容性标准

三级兼容性标准在二级兼容性标准的基础上，实现插件和 SDK 的二进制兼容。

**具体要求包括：**

1. 兼容旧版本的配置；
2. 兼容旧版本的函数和脚本；
3. 兼容旧版本的存储数据，包括分布式表数据，持久化的流数据表数据，定时任务，函数视图和用户权限数据等；
4. 插件和 SDK 满足二进制兼容性，即插件和 SDK 不需要升级也能继续运行。

**升级指南：**

升级前必须做好控制节点和数据节点的元数据备份。回退时需要先恢复备份的旧版本的元数据。
