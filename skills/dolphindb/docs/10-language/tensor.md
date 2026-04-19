<!-- Auto-mirrored from upstream `documentation-main/progr/tensor.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 张量

在深度学习和机器学习领域，张量（tensor）是一个核心概念，主要用于表示多维数据。为了与深度学习框架（如 PyTorch）更好地集成，DolphinDB 引入了 tensor
数据结构。tensor 本质上是一个多维数组，采用行优先的存储方式，即内存中的元素按行连续排列。

tensor 包含两个重要属性：shape 和 strides。shape 是一个向量，表述 tensor 各个维度的大小（size），描述了 tensor 的形状，其中
shape[i] 表示第 i+1 个维度的大小（通常 i=0 表示第一个维度）。strides 是一个和 shape
长度相同的向量，指示了在内存中跳过多少元素以沿着某个轴移动到下一个位置。在 DolphinDB 中创建的 tensor 是连续的，strides 可以根据 shape
计算得出，以一个3 维 tensor 为例进行说明，假如 shape=[D, H, W]，则 strides 是 [H\*W, W, 1]。

目前在 DolphinDB 中，tensor 通过函数 tensor 生成，主要应用于 DolphinDB 插件（如 LibTorch
等），与深度学习框架进行数据交换。关于如何生成 tensor，请参考函数 tensor。

注：

DolphinDB 中的 tensor 目前暂不支持直接存储和计算，并且不支持直接访问和修改其元素。
