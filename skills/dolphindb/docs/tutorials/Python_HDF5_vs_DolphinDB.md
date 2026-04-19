<!-- Auto-mirrored from upstream `documentation-main/tutorials/Python_HDF5_vs_DolphinDB.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# SecurityIDs 为要计算的全部股票列表
SecurityIDs_splits = np.array_split(SecurityIDs, n)
Parallel(n_jobs=n)(delayed(ParallelBySymbol)(SecurityIDs,pathDir) for SecurityIDs in SecurityIDs_splits)
```

### 3.3. 计算性能对比

基于前述内容，本节我们进行不同并行度的 Python + HDF5 因子计算和 DolphinDB 库内一体化因子计算的性能比对。计算的数据量为 1992 只股票，3天总计 2200万行。我们调节不同的并行度，测试在使用不同 CPU 核数的情况下，两种方式计算因子的耗时。所有测试均在清除操作系统缓存后进行。测试结果如下表：

| CPU核数 | Python+HDF5(秒) | DolphinDB（秒） | （Python+HDF5）/ DolphinDB |
| --- | --- | --- | --- |
| 1 | 2000 | 21.0 | 95 |
| 2 | 993 | 11.5 | 86 |
| 4 | 540 | 6.8 | 79 |
| 8 | 255 | 5.8 | 44 |
| 16 | 133 | 4.9 | 27 |
| 24 | 114 | 4.3 | 26 |
| 40 | 106 | 4.2 | 25 |

从比对结果可以看到。本次测试中，在单核的前提下，DolphinDB 库内计算比 Python + HDF5计算快接近100倍。随着可用 CPU 核数逐渐增加，DolphinDB 库内计算和 Python + HDF5 计算耗时比逐渐趋近 1:25 左右。考虑两种计算方式的特点，原因大概如下：

* DolphinDB 自有的数据存储系统的读取效率远优于 Python 读取使用通用存储方式的 HDF5 文件存储。
* DolphinDB 的针对性移动计算函数滑动窗口系列（m 系列）对于不同的移动窗口计算优化可提供更佳计算性能

尽管 HDF5 格式的数据文件读取可以从技术层面进行针对性的冗余存储或者其他针对性优化，但同时会带来额外的硬件资源成本、数据使用和管理成本等。相比之下，DolphinDB 的自有数据存储系统在使用上更为高效、方便和简单。 因此 DolphinDB 的库内一体化因子计算在完整的因子数据读取、计算全过程上的计算速度是远优于 Python + HDF5 的因子计算方式的。

从计算性能的对比中，不难发现以下现象：

* 代码实现方面，DolphinDB 的库内 Sql 计算更易于实现因子计算调用及并行调用。
* 并行计算方面，DolphinDB 可以自动使用当前可用的 CPU 资源，而Python 脚本需要通过并行调度代码实现，但更易于控制并发度。
* 计算速度方面，DolphinDB 的库内计算比 Python + HDF5 的计算方式快 25 倍以上。

### 3.4. 计算结果对比

上一节中，我们比对了两种计算的方式的计算性能。DolphinDB 的库内因子计算在计算速度上要远优于 Python + HDF5 的因子计算方式。但是计算快的前提是计算结果要正确一致。我们将 Python +HDF5 和 DolphinDB 的因子计算结果分别存入 DolphinDB 的分布式表中。部分计算结果比对展示如下图，显示的部分结果完全一致。全部的数据比对通过 DolphinDB 脚本进行，比对结果也是完全一致。

![](images/Python_HDF5_vs_DolphinDB/3_2.png)

也可以通过如下代码进行全数据验证，输出 int[0] 则表示两张表内容一致。

```
resTb = select * from loadTable("dfs://tempResultDB","result_cyc_test")
resTb2 = select * from loadTable("dfs://tempResultDB","result_cyc_test2")
resTb.eq(resTb2).matrix().rowAnd().not().at()
```

验证结果显示，采用Python + HDF5 和 DolphinDB 两种方式进行计算，结果完全一致。

## 4. 总结

本篇文章的比较结果显示，在使用相同核数 CPU 的前提下：

* DolphinDB 的库内一体化计算性能约为 Python + HDF5 因子计算方案的 25 倍左右，计算结果和 Python 方式完全一样。
* 两种方案的因子开发效率相近
* 在数据的管理和读取方面：
  + 每个 HDF5 文件的读取或写入基本是单线程处理的，难以对数据进行并行操作。 此外 HDF5 文件中数据读取效率较依赖于数据在 HDF5 的 group 和 dataset 组织结构。为了追求更好的读写效率，经常要考虑不同的数据读取需求来设计存储结构。需要通过一些数据冗余存储来满足不同场景的高效读写。这种数据操作方式在数据量逐渐上升到 T 级之后，数据管理和操作的复杂度更会大幅增加，实际使用中会增加大量的时间成本和存储空间成本。
  + 而 DolphinDB 的数据管理、查询、使用更为简单便捷。得益于 DolphinDB 的不同存储引擎及分区机制，用户可以以普通数据库的方式轻松管理、使用 PB 级及以上数量级别的数据。

综合而言，在生产环境中，使用 DolphinDB 进行因子计算和存储远比使用 Python + HDF5 计算方式更加高效。

## 5. 附录

本教程中的对比测试使用了以下测试脚本：

* [createDBAndTable.dos](script/Python%2BHDF5_vs_DolphinDB/createDBAndTable.dos)
* [ddbFactorCal.dos](script/Python%2BHDF5_vs_DolphinDB/ddbFactorCal.dos)
* [gentHdf5Files.py](script/Python%2BHDF5_vs_DolphinDB/gentHdf5Files.py)
* [pythonFactorCal.py](script/Python%2BHDF5_vs_DolphinDB/pythonFactorCal.py)
