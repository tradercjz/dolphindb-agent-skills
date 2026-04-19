<!-- Auto-mirrored from upstream `documentation-main/tutorials/prep_linux_for_deploy.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# systemctl disable firewalld.service
```

### Swap

Swap 即交换分区，在物理内存不够用时，操作系统会从物理内存中把部分暂时不被使用的数据转移到交换分区，从而为当前运行的程序留出足够的物理内存空间，保证程序的正常运行，但会造成系统性能下降。如果系统物理内存充足，且用户比较重视性能，建议关闭 Swap，步骤如下：

1. 检查 Swap 是否已关闭

   ```
   # free -h
                 total        used        free      shared  buff/cache   available
   Mem:           7.6G        378M        7.1G        8.5M        136M        7.1G
   Swap:          7.9G          0B        7.9G
   ```

   可见 Swap 的 total 值为 7.9G，未关闭。
2. 临时关闭 Swap

   ```
   # swapoff -a
   ```
3. 再次检查 Swap 是否已关闭

   ```
   # free -h
                 total        used        free      shared  buff/cache   available
   Mem:           7.6G        378M        7.1G        8.5M        136M        7.1G
   Swap:            0B          0B          0B
   ```

   可见 Swap 的 total 值为 0B，已关闭。
4. 永久关闭 Swap，注释掉第 2 列值为 swap 的行

   ```
   # vi /etc/fstab
   ...
   # /dev/mapper/centos-swap swap                    swap    defaults        0 0
   ...
   ```

## 部署 DolphinDB

系统配置好后，即可根据业务需求选择合适的部署方式部署 DolphinDB。

### 单节点、单机集群、多机集群的选择

本节介绍不同部署方式之间的比较重要的差异，不同部署方式的功能和应用场景的完整列表见《DolphinDB 安装使用指南》。

* 相同单机资源，部署单节点和单机集群的差异

  单节点指在单机上部署一个 DolphinDB 单机节点，单机集群指在单机上部署多个 DolphinDB 分布式节点。

  单机集群通常适合密集型计算场景，将计算任务分发到不同的节点（进程）上，可以有效的隔离内存资源竞争，提高计算效率。

  集群与单节点的另外两个差异，一是集群支持横向扩展，即支持在线加入新的数据节点，提高整个集群的最大负载；二是集群支持高可用，容错率更高。

  综上，单机部署时，建议部署集群模式。
* 相同节点的情况下，部署单机集群和多机集群的差异

  多机集群部署指将 DolphinDB 分布式节点分别部署到多台机器上。

  多机可以充分利用各个节点（机器）的计算资源和存储资源。但是节点间通信引入了网络开销，故建议部署在内网并配置万兆网络以降低网络开销。

  另外，假设每台机器故障概率相同，多机比单机更容易出现故障，但由于节点分布在多机上，通过开启高可用支持，多机集群容错率更高。
* 单机多硬盘与多机部署的差异

  对于大吞吐量、低计算的任务来说，单机多硬盘集群模式因网络开销小而具有更好的性能。对于小吞吐量、重计算的场景，多机集群的分布式计算优势更明显。

  元数据和redo log的存储，相关配置项包括：

  + `chunkMetaDir`: 元数据目录
  + `dfsMetaDir`: 该目录保存控制器节点上的分布式文件系统的元数据
  + `redoLogDir`: OLAP 存储引擎重做日志（redo log）的目录
  + `TSDBRedoLogDir`: TSDB 存储引擎重做日志（redo log）的目录

  这些配置项建议指定到 SSD 以提高读写性能。

  数据实体的存储，相关配置项包括：

  + `volumes`: 数据文件目录。多个目录用 ',' 隔开，例如： /hdd/hdd1/volumes,/hdd/hdd2/volumes,/hdd/hdd3/volumes
  + `diskIOConcurrencyLevel`: 读写磁盘数据的线程数，默认为1，若 volumes 全部配置为 HDD 硬盘，建议 diskIOConcurrencyLevel 设置为同 HDD 硬盘个数相同的值

### Docker 和非 Docker 环境运行的选择

Docker 只是轻量化的资源隔离，DolphinDB 部署在 Docker 环境和非 Docker 环境下的运行性能差异不明显，可根据业务需求选择合适的运行环境。

### 生产环境配置参数实践

以搭建元数据和流数据高可用集群为例介绍如何配置集群各节点。设集群机器硬件配置相同，集群机器信息如下：

| 名称 | IP | 备注 |
| --- | --- | --- |
| centos-1 | 175.178.100.3 | 1控制节点，1代理节点，1数据节点 |
| centos-2 | 119.91.229.229 | 1控制节点，1代理节点，1数据节点 |
| centos-3 | 175.178.100.213 | 1控制节点，1代理节点，1数据节点 |

3 台机器上 cluster.nodes 与 cluster.cfg 配置文件内容均相同，而 controller.cfg 和 agent.cfg 需要根据机器 IP 和端口号做相应配置。注意下面只列出部分重要配置。

* [cluster.nodes](script/deploy_dolphindb_on_new_server/cluster.nodes)
* [cluster.cfg](script/deploy_dolphindb_on_new_server/cluster.cfg)

```
diskIOConcurrencyLevel=0
node1.volumes=/ssd1/dolphindb/volumes/node1,/ssd2/dolphindb/volumes/node1
node1.redoLogDir=/ssd1/dolphindb/redoLog/node1
node1.chunkMetaDir=/ssd1/dolphindb/metaDir/chunkMeta/node1
node1.TSDBRedoLogDir=/ssd1/dolphindb/tsdb/node1/redoLog
chunkCacheEngineMemSize=2
TSDBCacheEngineSize=2
...
```

* [controller.cfg](script/deploy_dolphindb_on_new_server/controller.cfg)

```
localSite=175.178.100.3:8990:controller1
dfsMetaDir=/ssd1/dolphindb/metaDir/dfsMeta/controller1
dfsMetaDir=/ssd1/dolphindb/metaDir/dfsMeta/controller1
dataSync=1
...
```

* [agent.cfg](script/deploy_dolphindb_on_new_server/agent.cfg)

```
localSite=175.178.100.3:8960:agent1
sites=175.178.100.3:8960:agent1:agent,175.178.100.3:8990:controller1:controller,119.91.229.229:8990:controller2:controller,175.178.100.213:8990:controller3:controller
...
```

关于如何配置部分重要配置参数，见下表：

| 文件 | 配置参数 | 说明 |
| --- | --- | --- |
| cluster.cfg | node1.volumes=/ssd1/dolphindb/volumes/node1,/ssd2/dolphindb/volumes/node1 | 配置多个 SSD 硬盘达到并发读写，以提高读写性能。 |
| cluster.cfg | diskIOConcurrencyLevel=0 | 合理设置该参数，可以优化读写性能。建议配置如下：若 volumes 配置了 SSD 硬盘，建议设置 diskIOConcurrencyLevel = 0；若 volumes 全部配置为 HDD 硬盘，建议 diskIOConcurrencyLevel 设置为同 HDD 硬盘个数相同的值。 |
| cluster.cfg | chunkCacheEngineMemSize=2 TSDBCacheEngineSize=2 | DolphinDB 目前要求 cache engine 和 redo log 必须搭配使用。若在 cluster.cfg 配置了chunkCacheEngineMemSize 和 TSDBCacheEngineSize（即启动 cache engine）则必须在 controller.cfg 里配置 dataSync=1。 |
| controller.cfg | dataSync=1 |

### 部署流程

DolphinDB为各种部署方式提供了详细的教程，在决定部署方式和配置后，根据教程部署即可，本文涉及的部署方式教程链接如下：

* 单节点部署
* 单节点部署（嵌入式ARM版本）
* 单服务器集群部署
* 多服务器集群部署
* 高可用集群部署教程
* 如何扩展集群节点和存储
* 基于 Docker单机部署方案
* 基于Docker-Compose的DolphinDB多容器集群部署

**注意**：在 windows 系统下部署时，部署路径不能包含中文。

### 启动流程

以启动前文配置的高可用集群为例，将配置文件相应放在 centos-1、centos-2、centos-3 机器的 DolphinDB 安装目录 */clusterDemo/config* 目录下。

**注意**：启动脚本使用了相对路径，故需要到脚本所在目录执行。

#### 启动控制节点

分别在 centos-1、centos-2、centos-3 机器上执行如下命令：

```
$ cd DolphinDB/clusterDemo/
$ ./startController.sh
```

#### 启动代理节点

分别在 centos-1、centos-2、centos-3 机器上执行如下命令：

```
$ cd DolphinDB/clusterDemo/
$ ./startAgent.sh
```

#### 启动数据节点

进入任意一个控制节点的 Web 集群管理界面，如 [http://175.178.100.3:8990](http://175.178.100.3:8990)，会自动跳转到 leader 节点的集群管理界面。在节点列表选中所有数据节点，点击启动按钮启动即可。Web 集群管理界面具体介绍见 DolphinDB Web 集群管理界面。

## 附件

* [cluster.nodes](script/deploy_dolphindb_on_new_server/cluster.nodes)
* [cluster.cfg](script/deploy_dolphindb_on_new_server/cluster.cfg)
* [controller.cfg](script/deploy_dolphindb_on_new_server/controller.cfg)
* [agent.cfg](script/deploy_dolphindb_on_new_server/agent.cfg)
