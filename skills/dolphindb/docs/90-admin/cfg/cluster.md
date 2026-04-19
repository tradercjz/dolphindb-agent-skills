<!-- Auto-mirrored from upstream `documentation-main/db_distr_comp/cfg/cluster.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 集群模式

从部署机器区分，集群分为单机集群和多机集群；从是否启用高可用区分，集群分为普通集群和高可用集群。

DolphinDB 集群包括 4
种类型节点：数据节点（datanode），计算节点（computenode），代理节点（agent）和控制节点（controller）。
其配置文件存放在config目录中，主要包含以下配置文件：

* controller.cfg：控制节点的配置文件
* agent.cfg：代理节点的配置文件
* cluster.cfg：数据节点的配置文件。单节点参数配置一节中的所有配置参数适用于集群中的数据节点，必须在
  cluster.cfg 中配置。
* cluster.nodes：集群成员信息文件

重要：

以上所有配置文件的第一行不可为空行。

## 普通集群

有关普通集群部署的方法，参考教程： 单机集群部署教程 , 多机集群部署教程

注：

多服务器环境下，控制节点所在服务器必须包含controller.cfg, cluster.cfg,
cluster.nodes 3种配置文件。代理节点必须包含 agent.cfg 文件。

在 cluster.cfg 中，可以使用以下4种方式指定配置参数的值：

1. 使用节点的别名。节点的别名在 cluster.nodes 中定义。

   ```
   nodeA.volumes = /DFSRoot/nodeA
   nodeB.volumes = /DFSRoot/nodeB
   ```
2. 使用别名和通配符("%" 和 "?")。"?" 表示单个字符，"%" 表示0，1或多个字符。

   ```
   %8821.volumes = /DFSRoot/data8821
   %8822.volumes = /DFSRoot/data8822
   DFSnode?.maxMemSize=16
   ```
3. 使用宏变量 <ALIAS>。<ALIAS>
   会自动替换对应节点的节点别名。例如：对于具有两个数据节点 *nodeA* 和 *nodeB* 的集群：

   ```
   volumes = /DFSRoot/<ALIAS>
   ```

   相当于：

   ```
   nodeA.volumes = /DFSRoot/nodeA
   nodeB.volumes = /DFSRoot/nodeB
   ```
4. 集群中的所有节点使用相同的参数值：

   ```
   // for Windows
   maxConnections=64
   // for Linux
   maxConnections=512
   maxMemSize=12
   ```

需要注意：

* 前 3 种适用于相同的参数在不同节点中具有不同的配置值的情况；
* 第 4 种适用于所有节点配置相同的参数值；
* 以第 1 种方式配置指定路径时，不能使用宏变量，否则控制节点无法启动。例如，不能配置为
  *nodeA.volumes = /DFSRoot/<ALIAS>*。

DolphinDB 提供了默认的 clusterDemo 文件夹存储对应的集群文件、默认的启动脚本：

| 脚本类型 | Windows | Linux |
| --- | --- | --- |
| 控制节点启动脚本 | startController.bat | startController.sh |
| 代理节点启动脚本 | startAgent.bat | startAgent.sh |
| 关机脚本 | stopAll.bat | stopAll.sh |

这些脚本仅对默认配置生效，用户可参考这些启动脚本中的命令，根据场景进行调整。

注：

集群环境下，关机脚本将关闭整个集群，参考 shutdown。对单个节点的重启操作，建议在 Web
集群管理器进行操作，具体操作可参考 基于 web 的集群管理 。

## 高可用集群

集群的高可用主要体现在数据高可用（多副本机制）、元数据高可用（控制节点高可用）、客户端高可用（API 指定多个数据节点 site，支持断连切换）。

对于高可用集群，配置文件 cluster.cfg 和 cluster.node 由 raft 组统一管理，它们仅作为集群第一次启动时的配置来源。集群启动后，修改
cluster.cfg 和 cluster.node 里的配置项将不会生效。必须通过 web 或 API 接口修改配置项，web 或 API
端会自动将修改同步到集群中的所有配置文件。

**相关信息**

* [高可用集群部署教程](../../tutorials/ha_cluster_deployment.html "高可用集群部署教程")
