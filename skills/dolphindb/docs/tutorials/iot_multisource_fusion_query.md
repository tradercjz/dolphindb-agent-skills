<!-- Auto-mirrored from upstream `documentation-main/tutorials/iot_multisource_fusion_query.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 基于外部表的物联网多源数据融合与联合查询实践

在工业制造、化工、能源电力等物联网核心应用场景中，由于信息化建设起步早、迭代周期长，长期以来沉淀了多类型信息化系统及异构数据库架构，形成了“数据孤岛”现象——不同业务系统的数据分散存储于MySQL、SQL Server、Oracle等关系型数据库，以及 HDFS 分布式文件系统等不同载体中。

随着企业信息化建设的持续深化及数据聚合应用的扩展，多源数据的融合与实时分析已成为核心业务需求，传统的数据迁移、导入导出或第三方工具同步方式，流程繁琐、效率低下，难以满足快速、简洁、高效的融合诉求，而 DolphinDB 的外部表跨数据库联邦查询功能，凭借零迁移、免预处理、实时联邦的核心特点，为解决这一痛点提供了高效路径。

## 1. 业务挑战

在物联网核心场景中异构数据库并存形成的“数据孤岛”，以及多源数据融合需求的不断升级，使得传统数据交互方式的弊端日益凸显，难以适配业务高效发展需求，进而催生了一系列亟待解决的业务挑战。

**工具生态繁杂，技术门槛高落地性差**

当前 ETL
工具种类庞杂，且不同工具适配不同数据源特性，用户往往需要针对性掌握多款工具的操作逻辑与使用技巧，这不仅增加了技能学习的门槛，也提升了实际业务落地的复杂度。

**数据处理链路冗长，实时分析无法响应**

数据清洗与转化环节效率表现欠佳，传统模式下需先将多源异构数据汇聚并标准化为统一格式，方可开展数据分析工作，导致即席数据分析需求无法得到即时响应，极大制约了数据价值的快速挖掘。

**多源数据质量不一，分析结果准确性差**

各数据源的数据类型存在差异、质量参差不齐，在数据汇聚过程中易引发格式转换失败、精度丢失等问题，影响数据分析结果的准确性，对数据驱动决策的可靠性构成严重影响。

## 2. 解决方案

针对核心业务痛点：企业信息化建设历史悠久，多类型系统与异构数据库并存，传统数据迁移、导入导出及ETL工具同步方式，已无法满足高效数据融合需求。

解决方案：DolphinDB 3.00.4 版本推出**外部表跨数据库联邦查询**功能，构建多源数据融合技术方案，具体如下：

![](image/iot_multisource_fusion_query/1.PNG)

图 1. 图 2-1 技术架构图

## 3. 核心技术优势

物联网核心场景“数据孤岛”问题突出，传统数据交互方式存在工具繁杂、链路冗长、数据质量不均等痛点，难以支撑多源数据高效融合与实时联合查询需求。DolphinDB 的外部表的跨数据库联邦查询功能，精准对标上述痛点，其核心技术优势如下：

**1、在线抓取--多源汇聚**

DolphinDB 的 ODBC、MySQL、Parquet 等插件，可将 ODBC 数据源（Oracle、MySQL、SQL Server等）、Parquet 文件、S3 等异构数据虚拟为本地表。该方案同时支持高效写入或映射至库内，支持批处理与实时处理双模协同，无缝串联工业物联网数据采集、存储、计算、分析全流程；无需多套异构工具组合，从底层规避跨系统数据流转冗余损耗，大幅提升处理效率，精准适配企业多源数据快速融合核心诉求。

![](image/iot_multisource_fusion_query/2.PNG)

图 2. 图 3-1 数据汇聚图

**2、内存计算--高效 ETL**

依托 DolphinDB 最新外部表跨库联邦查询功能，构建跨源数据无缝交互底座。该方案能够将 SCADA、MES 关系型数据、设备时序库等异构源虚拟为内存表，并支持在线转换与清洗。通过标准 SQL 即可联合查询、多维分析，无需数据迁移或格式转换，实现分散数据集中标准化管控。

**3、批流一体--架构精简**

依托 DolphinDB 一体化存算架构，外部表跨库联邦查询功能搭配 2000 + 内置函数及多类型流计算引擎，可快速搭建物联网实时分析系统，对海量分散汇聚数据实时分析、毫秒级响应，高效支撑产线监控、设备预警等核心业务。

相较传统 Flink/Spark+Hadoop 复杂架构，DolphinDB 外部表跨库联邦查询结合流计算方案，以 Dlang 脚本几行代码替代复杂开发，兼具高效计算、简洁架构、轻量化技术栈优势，有效降硬件成本、减运维难度，适配大规模多源数据实时分析需求。

**4、数据输出--实时推送**

借助外部表跨库联邦查询实现多源异构数据快速汇聚，搭配流计算引擎将汇聚数据及分析结果高效写入 DolphinDB 内存表；数据既可留存库内支撑历史趋势分析与模型训练，更能通过原生 HTTP、TCP/IP、MQTT、ODBC 等接口，无缝推送至 Kafka、各类外部数据库，以及物联网平台、企业 ERP、可视化系统等业务终端，该方案打通数据从采集到应用的全链路，加速数据价值转化。

**5、按需部署--轻量化、可扩展**

方案无需重构现有信息化架构，可基于既有系统快速部署插件与配置外部表，降低实施成本与业务中断风险。同时 DolphinDB 支持水平扩展，能够随数据量增长、新增系统接入需求灵活扩容，持续满足信息化深化过程中对数据融合的扩展性要求。

## 4. 演示说明

以某工厂的多种信息化系统及多样化数据库存储模式为例，演示如何进行多源数据融合。具体场景如下：

* MySQL：存储设备基础信息和项目基本信息。
* DolphinDB：存储设备实时采集数据。
* HDFS（Parquet 文件）：存储设备历史采集数据。

本演示将展示如何将上述多源数据进行融合，并通过联合查询获取分析结果。

![](image/iot_multisource_fusion_query/3.PNG)

图 3. 图 4-1 演示流程图

### Step 1：数据表字段说明

* **MySQL 的设备基本信息表（device\_info）**

| 列 | 名称 | 类型 |
| --- | --- | --- |
| Device\_ID | 设备编号 | VARCHAR |
| Device\_Name\_CN | 设备名称 | VARCHAR |
| Device\_Type | 设备类型 | VARCHAR |
| Manufacturer | 厂家信息 | VARCHAR |
| Device\_Status | 设备状态 | VARCHAR |

* **MySQL 的项目基本信息表（project\_info）**

| 列 | 名称 | 类型 |
| --- | --- | --- |
| Project\_id | 项目编号 | VARCHAR |
| Device\_id | 设备编号 | VARCHAR |
| Project\_name | 项目名称 | VARCHAR |
| Project\_status | 项目状态 | VARCHAR |
| Project\_manager | 项目经理 | VARCHAR |
| Create\_time | 项目创建时间 | DATETIME |
| Expected\_completion\_time | 项目结束时间 | DATETIME |
| Project\_description | 项目详细描述 | VARCHAR |

* **DolphinDB 的设备实时采集数据表（equipment\_monitor\_data）**

| 列 | 名称 | 类型 |
| --- | --- | --- |
| No | 序号 | INT |
| Device\_ID | 设备编号 | STRING |
| Temperature | 温度 | FLOAT |
| Pressure | 压力 | FLOAT |
| Humidity | 湿度 | FLOAT |
| Voltage | 电压 | FLOAT |
| Current | 电流 | FLOAT |
| Timestamp | 上报时间 | TIMESTAMP |

* **HDFS 的离线文件 Parquet 中的设备历史采集数据表（equipment\_history\_data）**

| 列 | 名称 | 类型 |
| --- | --- | --- |
| No | 序号 | SHORT |
| Device\_ID | 设备编号 | STRING |
| Temperature(℃) | 温度 | FLOAT |
| Pressure(MPa) | 压力 | FLOAT |
| Humidity(%RH) | 湿度 | FLOAT |
| Voltage(V) | 电压 | FLOAT |
| Current(A) | 电流 | FLOAT |
| Timestamp | 上报时间 | STRING |

### Step 2：数据及环境

**device\_info：**MySQL 上的设备基础信息表

**project\_info：**MySQL 上的项目基本信息表

**equipment\_monitor\_data：**DolphinDB 的设备实时采集数据数表

**equipment\_history\_data：**Parquet 离线文件上的设备历史采集数据表

**演示环境：** 1台 MySQL 数据库服务（用于存放 **device\_info、project\_info** 数据）、2台 DolphinDB
数据库服务（1台用于 DolphinDB 脚本运行、存放 **Parquet** 离线文件 **equipment\_history\_data**
数据及 **ODBC** 插件安装，1台 DolphinDB 服务器用于存放 **equipment\_monitor\_data** 数据）。

**ODBC 信息配置：**在操作系统上需要安装相应数据库的 ODBC 插件，并根据数据库类型（MySQL）进行配置 DSN 信息（
**MysqlODBC** ）。

### Step 3：代码及结果

* **OBDC 模式下以 MySQL 为数据源的外部表跨数据库联邦查询代码实现**

通过 ODBC 插件从 MySQL 数据库中获取设备基本信息（device\_info）和项目基本信息（project\_info）。

```
//读取ODBC插件(只需加载一次)
loadPlugin("odbc")
//配置MySQL的ODBC链接信息
Mysql_cfg = {"connectionString":"Dsn=MysqlODBC"}
//创建MySQL类型device_info的ExternalTable
mysql_device_info = createExternalTable("device_info", "mysql", Mysql_cfg)
//创建MySQL类型project_info的ExternalTable
mysql_project_info = createExternalTable("project_info", "mysql", Mysql_cfg)
//从ExternalTable查询device_info表信息
mysql_devData = select * from mysql_device_info
//从ExternalTable查询project_info表信息
mysql_proData = select * from mysql_project_info
```

* **DolphinDB 模式下的外部表跨数据库联邦查询代码实现**

通过 DolphinDB 链接获取远程服务器的设备实时采集数据（equipment\_monitor\_data）。

```
//配置DolphinDB的链接信息(相关配置信息按照DolphinDB的实际情况来配置)
ddb_cfg = {"host":"IP地址","port":端口号,"userId":"用户名",
           "password":"密码","database":"dfs://externalDB"}
//创建DolphinDB类型equipment_monitor_data的ExternalTable
ddb_monitor_data = createExternalTable("equipment_monitor_data", "dolphindb", ddb_cfg)
//从ExternalTable查询equipment_monitor_data表信息
ddb_equData = select * from ddb_monitor_data
```

* **Parquet 模式以 parquet 离线文件为数据源的外部表跨数据库联邦查询代码实现**

通过 Parquet 模式获取设备历史采集数据（equipment\_history\_data）。

```
//读取parquet插件(只需加载一次)
loadPlugin("parquet")
//配置parquet的文件路径
parquet_pro_cfg = {"fileName":"/home/jkzhong/equipment_history_data.parquet"}
//创建parquet类型equipment_history_data的ExternalTable
parquet_history_data = createExternalTable("equipment_history_data",
                                           "parquet", parquet_pro_cfg)
//从ExternalTable查询equipment_history_data表信息
parquet_equData = select * from parquet_history_data
```

* **三种数据源汇聚的联表数据查询（inner join）**

```
//MySQL和DolphinDB进行联表查询(设备、项目、最新实时采集数据)
select * from mysql_device_info inner join mysql_project_info on
mysql_device_info.Device_ID = mysql_project_info.Device_ID inner join
ddb_monitor_data on mysql_device_info.Device_ID = ddb_monitor_data.Device_ID
//MySQL和Parquet进行联表查询(设备、项目、历史采集数据)
select * from mysql_device_info inner join mysql_project_info on
mysql_device_info.Device_ID = mysql_project_info.Device_ID inner join
parquet_history_data on mysql_device_info.Device_ID = parquet_history_data.Device_ID
```

* **联合查询结果**

设备实时采集数据联合查询结果：

![](image/iot_multisource_fusion_query/4.PNG)

设备历史采集数据联合查询结果：

![](image/iot_multisource_fusion_query/5.PNG)

## 5. 总结

在物联网多数据接入的业务场景中，数据汇聚曾是长期困扰开发与运维人员的核心痛点：传统方案不仅需要依赖各类第三方工具完成繁琐的数据导入导出或数据同步操作，还需编写大量复杂的业务逻辑代码，技术实现链路长、成本高，且对技术栈的掌握程度要求严苛。

而 DolphinDB 的外部表跨数据库联邦查询功能，彻底重构了这一流程 —— 仅需寥寥数行 Dlang 脚本，即可轻松实现多源数据的高效汇聚，并可进一步结合
DolphinDB
的流计算引擎能快速的对数据进行分析。这一特性不仅大幅简化了技术实现路径，更显著降低了技术栈的学习成本与项目落地周期，让物联网场景下的跨库数据整合从复杂的
“工程化难题”，转变为简单、高效的 “轻量化操作”，为业务快速迭代与数据价值挖掘提供了核心支撑。

## 功能演示视频

[](image/iot_multisource_fusion_query/demo.mp4)
