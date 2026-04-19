<!-- Auto-mirrored from upstream `documentation-main/db_distr_comp/cfg/init.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 初始化

## 下载 server 并安装

下载 server 安装包并解压，可以发现一系列相关的文件夹。其中配置文件、许可证文件、日志文件和其他相关的依赖文件所在的目录为 DolphinDB 的主目录。

| 配置参数 | 解释 |
| --- | --- |
| home=/home/DolphinDB/server | DolphinDB 的主目录。该参数只能在命令行中指定。本章节中的 <HomeDir> 表示该参数的值。单节点模式下，通过 getHomeDir 函数可以获取 <HomeDir> 。集群模式下，home 在启动控制节点或代理节点时指定。数据节点/计算节点的 home 目录默认为代理节点 <HomeDir>下的 <nodeAlias> 目录。 |

初始状态下，解压后的 DolphinDB
主目录下包含几个依赖的文件夹：modules（依赖模块及用户自定义模块）、plugins（插件）、tzdb（时区数据库）、web（web
集群管理器依赖项）。分别对应以下配置项：

| 配置参数 | 解释 |
| --- | --- |
| moduleDir=modules | 节点的模块目录，可以是绝对路径或者是相对目录（默认为 modules）。系统搜寻相对目录 modules 的顺序如下：先到节点的 home 目录寻找，再到节点的工作目录寻找，最后到可执行文件所在目录寻找。 |
| pluginDir=plugins | 节点的插件目录，可以是绝对路径或者是相对目录（默认为 plugins）。系统搜寻相对目录 plugins 的顺序如下：先到节点的 home 目录寻找，再到节点的工作目录寻找，最后到可执行文件所在目录寻找。 |
| tzdb=<HomeDir>/tzdb | 时区数据库的目录。默认值是<HomeDir>/server/tzdb。 注： 仅 Windows 版本的 DolphinDB 有此目录。 |
| webRoot=web | web 服务器的目录，可以是绝对路径或者是相对目录（默认为 web）。系统搜寻相对目录 web 的顺序如下：先到节点的 home 目录寻找，再到节点的工作目录寻找，最后到可执行文件所在目录寻找。 |

## 启动 server

单机环境下，DolphinDB 支持以单节点模式（single mode）或者集群模式（cluster
mode）启动。绝大部分参数启动后不支持在线修改，因此必须在启动前，根据使用的生产场景，对配置项进行调整。

单节点模式下，server 依赖的配置项文件默认为 dolphindb.cfg； 集群模式下，配置项文件 cluster.cfg 默认存储在集群工作目录的
“config” 文件夹下。除必须在启动时通过命令行指定的配置参数外，该章节涉及到的所有配置参数均需在 config 或 clusterConfig
指定的文件中进行配置。

| 配置参数 | 解释 |
| --- | --- |
| config=dolphindb.cfg | 节点的配置文件。默认值为 dolphindb.cfg。该参数只能在命令行中指定。集群模式下，启动控制节点和代理节点时，需指定为对应节点的配置文件路径。默认条件下，控制节点的配置文件路径为 config/controller.cfg，代理节点为 config/agent.cfg。 |
| clusterConfig=cluster.cfg | 集群的配置文件，存储在控制节点的服务器上。默认值是 cluster.cfg。该参数只能在命令行中指定。 |

注：

集群环境下，除特殊说明的需要在 config
配置文件里进行配置的参数（主要为高可用、节点通信、节点恢复等功能涉及的参数）外，其余参数均在 clusterConfig 文件中配置。

集群模式，除了上述提到的必要配置文件，还有一个 cluster.nodes
文件。该文件配置在控制节点上，用于存放集群代理节点、数据节点和计算节点的网络信息。对应的配置参数为：

| 配置参数 | 解释 |
| --- | --- |
| nodesFile=cluster.nodes | 存储了集群代理节点和数据/计算节点的信息，存储在 controller 服务器上。默认值为 cluster.nodes。该参数只能在命令行中指定。 |

**相关信息**

* [单机集群配置集群成员参数文件](../../tutorials/single_machine_cluster_deploy.html "单机集群配置集群成员参数文件")
* [多机集群配置集群成员参数文件](../../tutorials/multi_machine_cluster_deployment.html "多机集群配置集群成员参数文件")
