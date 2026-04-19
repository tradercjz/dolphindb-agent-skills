<!-- Auto-mirrored from upstream `documentation-main/db_distr_comp/cfg/para_cfg.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 参数配置

DolphinDB 提供了一系列配置参数，方便用户根据实际情况进行合理的配置，以充分利用机器的硬件资源。

用户可通过 getConfig
函数，查看配置项的值。

注：

大部分参数数据节点和计算节点均可配置。由于计算节点不存储数据，因此无需配置磁盘相关的参数。
