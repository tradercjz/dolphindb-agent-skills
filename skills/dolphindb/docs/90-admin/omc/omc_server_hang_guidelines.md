<!-- Auto-mirrored from upstream `documentation-main/omc/omc_server_hang_guidelines.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 系统卡死

集群卡住无响应通常出现在以下两种情景：

* 节点启动或节点初始化过程中；
* 运行时出现。这种情况可以先参考日常巡检章节，查看是否一些机器相关的指标异常。有一种可能是当前的集群负载比较高，导致系统响应变慢。在排除因为系统负载原因导致的响应慢的情况下，需要先采集节点进程的栈信息，反馈给
  DolphinDB 的技术支持人员进行排查。

注：

为了便于 DolphinDB 技术支持更准确地分析栈的变化，建议至少采集两次栈信息，且两次采集之间的间隔时间为3-5分钟。

## 1. 采集栈信息

### 1.1 方法一：使用 `pstack`

安装 pstack 工具后，在集群的各节点上运行如下的 shell 脚本：

```
#!/bin/bash

mkdir /root/output/

dpid=`ps -ef |grep "mode datanode" |grep -v grep | awk '{print $2}'`
cpid=`ps -ef |grep "mode controller" |grep -v grep | awk '{print $2}'`

for i in $dpid
do
    cd /ddb/software/server
    pstack $i > /root/output/pstack_dnode_${i}.log
done

for i in $cpid
do
    cd /ddb/software/server
    pstack $i > /root/output/pstack_ctrl_${i}.log
done
```

以上脚本运行后，会在/root/output的目录下生成栈信息。之后需要将这些文件发给 DolphinDB 技术支持进行进一步的分析。

### 1.2 方法二：使用`gdb`

如果环境未安装 pstack，可以通过 gdb 的命令来获取栈信息，参考如下：

```
#!/bin/bash
mkdir /root/output/

dpid=`ps -ef |grep "mode datanode" |grep -v grep | awk '{print $2}'`
cpid=`ps -ef |grep "mode controller" |grep -v grep | awk '{print $2}'`
for i in $dpid
do
    cd /home/dolphindb/server
    gdb --eval-command "set logging file /root/output/pstack_dnode_$i.log" --eval-command "set logging on" --eval-command "thread apply all bt" --batch --pid $i;
done

for i in $cpid
do
    cd /home/dolphindb/server
    gdb --eval-command "set logging file /root/output/pstack_ctl_$i.log" --eval-command "set logging on" --eval-command "thread apply all bt" --batch --pid $i;
done
```

## 2. 通过紧急通道释放资源

在部分严重卡顿场景中（如所有工作线程被阻塞且无法释放），系统可能陷入如下“死锁”：**需要释放线程 → 需要取消任务 → 需要建立连接 →
但连接失败因为线程耗尽**。

此时，可使用紧急通道登录目标 DolphinDB 进程，以无需远程连接的方式执行命令（如取消任务），从而释放关键资源，恢复系统运行。

注：紧急通道功能自 DolphinDB 2.00.16/3.00.3 起支持，且仅在 Linux 上可用。

### 2.1 原理说明

紧急通道是 DolphinDB 内部设计的特殊通道，专用于系统极端状态（如 OOM）下的故障处理。

该通道在工作时使用专门预留的内存区域（不超过最大内存的10%），即使主内存已耗尽，仍可维持连接建立和指令执行的最低可用性。通过该机制，系统可在“远程连接不可用、主线程卡死”时，仍有路径执行关键命令（如取消任务、释放资源），从而恢复正常状态。

### 2.2 使用说明

1. 登录卡顿的节点服务器。
2. 使用 DolphinDB
   服务进程的同一系统用户，在另一安装目录下执行以下命令：

   ```
   ./dolphindb -attach 1 -target-pid <目标进程 PID>
   ```

   参数说明：

   * **-attach 1**：表示当前进程用于附加连接；
   * **-target-pid**：指定目标 DolphinDB 服务进程的 PID。
3. 成功连接后，将进入一个交互式 DolphinDB 控制台（命令提示符通常为
   `>`，但部分场景下可能不显示），可执行常规脚本指令以查看状态或释放资源，例如：

   ```
   >        clearAllCache();
   ```
4. 任务完成后，输入 `quit` 退出连接。

### 2.3 注意事项

* 紧急通道仅用于异常运维场景，不建议用于日常操作。
* 若需取消任务，请预先获取作业 ID。
* 使用完毕应及时 quit 断开连接。
* 若连接失败，请检查以下项：
  + *-target-pid* 是否为有效的 DolphinDB 服务进程 PID。
  + 当前用户是否与目标进程所属用户一致。
  + DolphinDB 安装目录是否正确。
