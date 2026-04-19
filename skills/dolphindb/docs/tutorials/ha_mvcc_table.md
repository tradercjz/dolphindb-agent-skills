<!-- Auto-mirrored from upstream `documentation-main/tutorials/ha_mvcc_table.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 高可用 MVCC 与普通 MVCC 的性能基准测试

## 1. 测试环境

| 配置项 | 参数 |
| --- | --- |
| **CPU** | Intel(R) Xeon(R) Gold 5320 CPU @ 2.20GHz |
| **内存** | 754 GB |
| **网卡** | 200 Gbps |
| **测试数据量** | 3,500,000 行 |

## 2. 写入场景

### 2.1 场景描述

分别对高可用 MVCC 表和 MVCC 表进行批量写入测试。测试单线程和多线程并发写入性能。

数据写入脚本如下：

```
INSERT INTO sales_plan_table
      (row_id, id, plan_version, branch_company_code, branch_company_name,
       channel_type, year_code, season_name, category_lv1_code, structure,
       year_month_col, new_old_tag, month_tag, level_tag, sort_col,
       year_month_sort, sales_amount_ratio_channel_diff, sales_amount_ratio,
       sales_amount, sales_unit_price, sales_qty, sales_cost_price,
       gross_profit, sales_cost_amount, ...)
  VALUES
      (1, '1', 'v1.0', 'BC001', '华东', '线上', '2024', '春', 'CAT001', ...),
      (2, '2', 'v1.0', 'BC002', '华南', '线下', '2024', '夏', 'CAT002', ...),
      ...
```

### 2.2 测试参数

| 参数 | 值 |
| --- | --- |
| 数据量 | 3,500,000 行 |
| 批次大小 | 50,000 行/批 |
| 线程数 | 单线程 / 12 线程 |

### 2.3 测试结果对比

**单线程写入**

| 指标 | 高可用 MVCC | MVCC | 差异 |
| --- | --- | --- | --- |
| 总耗时 | 15.34 秒 | **6.96 秒** | MVCC 快 2.2x |
| 写入速率 | 228,206 行/秒 （129.9 MB/s） | **502,729 行/秒（286.2 MB/s）** | MVCC +120% |

**多线程写入 (12 线程)**

| 指标 | 高可用 MVCC | MVCC | 差异 |
| --- | --- | --- | --- |
| 总耗时 | 10.01 秒 | **5.00 秒** | MVCC 快 2.0x |
| 写入速率 | 349,791 行/秒 （199.15 MB/s） | **699,301 行/秒（286.2 MB/s）** | MVCC +100% |

**结论**：在写入场景下，普通 MVCC 相比高可用 MVCC 具有更高性能，单线程和多线程写入性能分别提升约 **2.2 倍**和 **2.0
倍**，主要由于高可用 MVCC 需要额外的 Raft 一致性协议开销。

## 3. 更新场景

### 3.1 场景描述

对两种表进行随机范围更新测试，更新操作涉及对销售金额、数量、单价、成本等多个字段的计算与写入。

数据写入脚本如下：

```
update loadHaMvccTable(tableName)   -- 或 loadMvccTable
     set
         sales_amount = sales_amount * 1.05,
         sales_qty = sales_qty * 1.02,
         sales_unit_price = sales_amount / sales_qty,
         sales_cost_price = sales_unit_price * 0.65,
         sales_cost_amount = sales_qty * sales_cost_price,
         gross_profit = sales_amount - sales_cost_amount,
         update_time = format(now(), "yyyy-MM-dd HH:mm:ss"),
         update_by = "update_" + string(updateId)
     where row_id >= startRowId and row_id <= endRowId
```

### 3.2 测试参数

| 参数 | 值 |
| --- | --- |
| 底表数据量 | **3,500,000 行** |
| 每次更新行数 | **30,000 行** |
| 线程数 | 单线程 / 12 线程 |
| 测试轮次 | 单线程 10 轮 / 多线程持续 30 秒 |

### 3.3 测试结果对比

**单线程更新**

| 指标 | 高可用 MVCC | MVCC | 差异 |
| --- | --- | --- | --- |
| 平均耗时 | **0.14 秒** | 0.15 秒 | 持平 |
| 最小耗时 | **0.10 秒** | 0.11 秒 | 持平 |
| 最大耗时 | 0.28 秒 | **0.26 秒** | 高可用 MVCC 更稳定 |
| 理论 QPS | 6.94 | **6.84** | 基本持平 |

**多线程更新 (12 线程)**

| 指标 | 高可用 MVCC | MVCC | 差异 |
| --- | --- | --- | --- |
| 完成更新数 | 462 次 | **515 次** | MVCC +11% |
| 实际 QPS | 7.4 | **8.3** | MVCC +11% |
| 平均延迟 | 839.1 ms | **813.6 ms** | MVCC -4% |
| 最小延迟 | 146.0 ms | **105.0 ms** | MVCC -29% |
| 最大延迟 | **1284.0 ms** | 1895.0 ms | MVCC +47% |

**结论：**

* **单线程更新场景**：两者性能整体接近，高可用 MVCC 的性能波动相对更小，稳定性略优。
* **多线程并发更新场景**：普通 MVCC 的性能优于高可用 MVCC，QPS 约提升 **11%**。

## 4. 查询场景

### 4.1 场景描述

对两种表进行随机范围查询测试，测试不同数据量和不同并发数组合下的查询性能。

测试脚本如下：

```
select * from loadHaMvccTable(tableName)   -- 或 loadMvccTable
     where row_id >= startRowId and row_id <= endRowId
```

### 4.2 测试参数

| 参数 | 值 |
| --- | --- |
| 底表数据量 | **3,500,000 行** |
| 查询数据量 | 5 万 / 20 万 / 40 万行 |
| 并发数 | 10 / 13 / 15 并发 |

### 4.3 多线程查询结果对比

**小数据量 (5 万行)**

| 并发数 | 高可用 MVCC QPS | MVCC QPS | 高可用 MVCC 延迟 | MVCC 延迟 | QPS 差异 |
| --- | --- | --- | --- | --- | --- |
| 10 | **148.8** | 139.5 | **34.4 ms** | 36.1 ms | HAMVCC +7% |
| 13 | 190.7 | **198.0** | 34.1 ms | **32.7 ms** | MVCC +4% |
| 15 | 208.4 | **220.5** | 35.5 ms | **33.5 ms** | MVCC +6% |

**中数据量 (20 万行)**

| 并发数 | 高可用 MVCC QPS | MVCC QPS | 高可用 MVCC 延迟 | MVCC 延迟 | QPS 差异 |
| --- | --- | --- | --- | --- | --- |
| 10 | **44.2** | 41.1 | **130.4 ms** | 133.9 ms | HAMVCC +8% |
| 13 | 52.8 | **53.2** | **126.9 ms** | 127.2 ms | 基本持平 |
| 15 | 53.3 | **54.2** | 139.3 ms | **137.1 ms** | 基本持平 |

**大数据量 (40 万行)**

| 并发数 | 高可用 MVCC QPS | MVCC QPS | 高可用 MVCC 延迟 | MVCC 延迟 | QPS 差异 |
| --- | --- | --- | --- | --- | --- |
| 10 | **22.8** | 21.2 | **261.3 ms** | 263.3 ms | HAMVCC +8% |
| 13 | **26.5** | 26.0 | **254.2 ms** | 262.8 ms | HAMVCC +2% |
| 15 | **26.9** | 26.1 | **276.4 ms** | 284.9 ms | HAMVCC +3% |

**结论：**多线程查询场景下两者整体性能接近。在**小数据量、高并发**场景下，普通 MVCC
略占优势；在**中等及大数据量**场景下，高可用 MVCC 表现略优。

## 5. 综合对比

| 场景 | 高可用 MVCC | MVCC | **更优性能** |
| --- | --- | --- | --- |
| **单线程写入** | 228,206 行/秒 | 502,729 行/秒 | **MVCC** |
| **多线程写入** | 349,791 行/秒 | 699,301 行/秒 | **MVCC** |
| **单线程更新** | 9.97 QPS | 10.18 QPS | 持平 |
| **多线程更新** | 13.5 QPS | 8.0 QPS | **高可用 MVCC** |
| **多线程查询** | 22.8~208.4 QPS | 21.2~220.5 QPS | 持平 |

总体测试结果表明，高可用 MVCC 表（`haMvccTable`） 仅在 insert 场景下相较 MVCC
表（`mvccTable`） 存在约 2 倍的性能差距，在更新和查询等其他场景中，性能差异均不显著。

## 6. 附录

* haMvccTable 性能基准测试脚本：[haMvccTable\_test\_scripts.dos](script/mvcc_test/haMvccTable_test_scripts.dos)
* mvccTable 性能基准测试脚本：[mvccTable\_test\_scripts.dos](script/mvcc_test/mvccTable_test_scripts.dos)
