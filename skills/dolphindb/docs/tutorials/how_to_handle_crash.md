<!-- Auto-mirrored from upstream `documentation-main/tutorials/how_to_handle_crash.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 节点宕机

在使用 DolphinDB 时，有时客户端会抛出异常信息：Connection refused。此时，Linux 操作系统上使用 `ps` 命令查看，会发现 DolphinDB 进程消失。本教程针对出现这种情况的各种原因进行定位分析，并给出相应解决方案。

## 1. 查看节点日志排查原因

DolphinDB 每个节点的运行情况会记录在相应的日志文件中。通过分析日志，能有效地掌握 Dolphindb 运行状况，从中发现和定位一些错误原因。当节点宕机时，非 DolphinDB 系统运行原因导致节点关闭的情形通常有以下三种：

* Web 集群管理界面上手动关闭节点或调用 `stopDataNode` 函数停止节点
* 操作系统 kill 命令杀死节点进程
* license 有效期到期关机

通过查看节点在退出前是否打印了日志：MainServer shutdown 进行盘查。下面假设宕机节点为 `datanode1`，操作命令示例如下：

```
less datanode1.log|grep "MainServer shutdown"
```

若命令执行结果显示如下图，推算系统退出的时间点也合理，可初步认定为系统主动退出。

![](images/handle%20shutdown/handle_shutdown3-4.png)

下面分情况讨论进一步的排查步骤。

第一种：查看控制节点日志 `controller.log`，判断是否为 Web 集群管理界面上手动关闭节点或调用 `stopDataNode` 函数停止节点，操作命令示例如下：

```
less controller.log|grep "has gone offline"
```

![](images/handle%20shutdown/handle_shutdown3-5.png)

若日志产生的信息如上图，可判断为通过 Web 界面手动关闭节点或调用 `stopDataNode` 函数停止节点。

第二种：查看对应宕机节点运行日志是否含有 Received signal 信息，判断是否为操作系统 `kill` 命令杀死节点进程。操作命令示例如下：

```
less datanode1.log|grep "Received signal"
```

![](images/handle%20shutdown/handle_shutdown3-6.png)

若相应时间点上有上图所示信息，则可判定为进程被 `kill` 命令杀掉。

第三种：查看节点运行日志是否打印了如下信息：The license has expired，判断是否为 license 到期而关机：
![](images/handle%20shutdown/handle_shutdown3-7.png)

若出现上图信息，可以判断是 license 到期退出。用户需要关注 license 有效期日期，及时更新 liense 以避免出现因 license 到期而无法使用的问题。从1.30.11，1.20.20开始，DolphinDB 支持不重启系统，在线更新 license。但是，DolphinDB 1.30.11及1.20.20之前的版本因为不支持在线更新 license，更新 license 后，需要重启数据节点、控制节点和代理节点，否则会导致数据节点退出。

注意：节点日志存放路径为：单节点模式默认在安装目录 server 下，文件名为 dolphindb.log，集群默认在 server/log 目录下。若需要修改日志文件路径，只能在命令行中通过 logFile 配置项指定。如果集群内有节点在运行，可通过如下 `ps` 命令查看每一个节点对应的 log 生成位置，其中 logFile 参数表示日志文件的路径和名称：

![](images/handle%20shutdown/handle_shutdown2-1.png)

如果未查询到上述的日志信息，需进一步查看相应操作系统日志。

## 2. 查看操作系统日志排查 OOM killer

Linux 内核提供了一种名为 OOM killer（Out Of Memory killer）的机制，用于监控占用内存过大的进程，尤其是瞬间占用大量内存的进程，以防止内存耗尽而自动把该进程杀掉。排查 OOM killer 可用 dmesg 命令，示例如下：

```
dmesg -T|grep dolphindb
```

![](images/handle%20shutdown/handle_shutdown1-3.png)

如上图，若出现了“Out of memory: Kill process”，说明 DolphinDB 使用的内存超过了操作系统所剩余的空闲内存，导致操作系统杀死了 DolphinDB 进程。解决这种问题的办法是：通过参数 *maxMemSize* （单节点模式修改 dolphindb.cfg，集群模式修改 cluster.cfg）设定节点的最大内存使用量。需要合理设置该参数，设置太小会严重限制集群的性能；设置太大可能触发操作系统杀掉进程。若机器内存为16GB，并且只部署1个节点，建议将该参数设置为12GB左右。

使用上述 `dmesg` 命令显示日志信息时，若看到如下图所示的“segfault”，就是发生了段错误，即应用程序访问的内存超出了系统所给的内存空间：

![](images/handle%20shutdown/handle_shutdown1-2.png)

可能导致段错误的原因有：

* DolphinDB 访问系统数据区，最常见的就是操作0x00地址的指针
* 内存越界（数组越界，变量类型不一致等）：访问到不属于 DolphinDB 的内存区域
* 栈溢出（Linux 一般默认栈空间大小为8192kb，可使用 `ulimit -s` 命令查看）

此时若正确开启了 core 功能，会生成相应的 core 文件，就可以使用 `gdb` 对 core 文件进行调试。

## 3. 查看 core 文件

在程序运行过程中，若发生异常导致程序终止，操作系统会自动记录程序终止时的内存状态，并将其保存至一个特定的文件中。这一过程被称为core dump，也可译为“核心转储”。尽管 core dump 常被视作一种“内存快照”，但它所包含的信息远不止内存数据。core dump 还会同时记录其他关键的程序运行状态，如寄存器信息（含程序指针、栈指针等）以及其他处理器和操作系统的状态信息。对于编程人员来说，诊断和调试程序时，core dump 是一个极其有用的工具，因为某些程序错误，例如指针异常，可能在现实环境中难以复现，但 core dump 文件能够提供程序出错时的详细上下文，从而帮助开发人员准确定位问题。core 文件默认生成位置与可执行程序位于同一目录下，文件名为 core.\*\*\*，其中\*\*\*是一串数字。

### 3.1 core 文件设置

#### 3.1.1 控制 core 文件生成

首先在终端中输入 `ulimit -c` 查看是否开启 core 文件。若结果为 0，则表示关闭了此功能，不会生成 core 文件。结果为数字或者"*unlimited*"，表示开启了 core 文件。因为 core 文件比较大，建议设置为"*unlimited*"，表示 core 文件的大小不受限制。可用下列命令设置：

```
ulimit -c unlimited
```

以上配置只对当前会话起作用，重新登录时，需要重新配置。以下两种方式可使配置永久生效：

* 在 */etc/profile* 中增加一行 `ulimit -S -c unlimited >/dev/null 2>&1` 后保存退出，重启 server；或者不重启 server，使用 `source /etc/profile` 使配置马上生效。*/etc/profile* 对所有用户有效，若想只针对某一用户有效，则修改此用户的 *~/.bashrc* 或者 *~/.bash\_profile* 文件。
* 在 */etc/security/limits.conf* 最后增加如下两行记录：为所有用户开启 core dump。

![](images/handle%20shutdown/handle_shutdown3-1.png)

注意： 由于 DolphinDB 数据节点是通过代理节点进行启动的，在不重启代理节点的情况下，无法使开启 core 功能生效。因此，开启 core 功能后需要重启代理节点，再重启数据节点。

#### 3.1.2 修改 core 文件保存路径

core 文件默认的文件名称是 *core.pid*，其中 pid 是指产生段错误程序的进程号。core 文件默认路径是该程序的当前目录。

*/proc/sys/kernel/core\_uses\_pid* 可控制产生的 core 文件名中是否添加 pid 作为扩展。1表示添加，0表示不添加。通过以下命令进行修改：

```
echo "1" > /proc/sys/kernel/core_uses_pid
```

*/proc/sys/kernel/core\_pattern* 可设置 core 文件保存的位置和文件名。但保存路径可能在机器重启后失效，若想使设置永久生效，需要在 */etc/sysctl.conf* 文件中添加 kernel.core\_pattern=/data/core/core-%e-%p-%t.core。通过以下命令将 core 文件存放到 */corefile* 目录下，产生的文件名为：core-命令名-pid-时间戳：

```
 echo /corefile/core-%e-%p-%t > /proc/sys/kernel/core_pattern
```

**上述命令参数列表如下:**

* %p - insert pid into filename 添加pid
* %u - insert current uid into filename 添加当前uid
* %g - insert current gid into filename 添加当前gid
* %s - insert signal that caused the coredump into the filename 添加导致产生core的信号
* %t - insert UNIX time that the coredump occurred into filename 添加core文件生成时的unix时间
* %h - insert hostname where the coredump happened into filename 添加主机名
* %e - insert coredumping executable name into filename 添加命令名

一般情况下，无需修改参数，按照默认的方式即可。可根据实际环境修改 core 文件路径及名称。

注意：

* 设置 core 文件保存路径时首先要创建这个保存路径，并确保运行进程的用户对此目录有读写权限，否则 core 文件无法生成，建议将此目录的权限设置为 777。

  ```
  chmod 777 /path2/corefile
  ```
* 要注意所在磁盘的剩余空间大小，不要影响 DolphinDB 元数据、分区数据的存储。

#### 3.1.3 测试core文件是否能够生成

使用下列命令对某进程（用 `ps` 查到进程号为24758）使用 SIGSEGV 信号，可以 kill 掉这个进程：

```
kill -s SIGSEGV 24758
```

若在 core 文件夹下生成了 core 文件，表示设置有效。

### 3.2 gdb 调试 core 文件

若 gdb 没有安装，需要先安装。以 Centos 系统为例，安装 gdb 用命令如下：

```
yum install gdb
```

gdb 调试命令格式：`gdb [exec file] [core file]`，然后执行 bt 看堆栈信息：

![](images/handle%20shutdown/handle_shutdown3-2.png)

### 3.3 core 文件不生成的情况

Linux中信号是一种异步事件处理的机制，每种信号对应有默认的操作，可以在 **这里** 查看 Linux 系统提供的信号以及默认处理。默认操作主要包括忽略该信号（Ingore）、暂停进程（Stop）、终止进程（Terminate）、终止并发生 core dump 等。如果信号均是采用默认操作，那么，以下几种信号发生时会产生 core dump:

| Signal | Action | Comment |
| --- | --- | --- |
| SIGQUIT | core | Quit from keyboard |
| SIGILL | core | Illegal Instruction |
| SIGABRT | core | Abort signal from abort |
| SIGSEGV | core | Invalid memory reference |
| SIGTRAP | core | Trace/breakpoint trap |

当然，Linux 提供的信号不仅限于上面的几种。还有一些信号是无法产生 core dump 的，比如：

(1) 使用 `Ctrl+z` 来挂起一个进程或者 `Ctrl+C` 结束一个进程均不会产生 core dump，因为前者会向进程发出 **SIGTSTP** 信号，该信号的默认操作为暂停进程(Stop Process)；后者会向进程发出 **SIGINT** 信号，该信号默认操作为终止进程(Terminate Process)。

(2) `kill -9` 命令会发出 **SIGKILL** 命令，该命令默认为终止进程，同样不会产生 core 文件。

(3) 查看 DolphinDB 对应日志，假设日志信息出现“Received signal 15”，如下图，即用 **SIGTERM** （kill命令默认信号）杀死 DolphinDB 进程，不会生成 core 文件。

![](images/handle%20shutdown/handle_shutdown3-6.png)

以下情况也不会产生 core 文件：

(a) 进程是设置-用户-ID，而且当前用户并非程序文件的所有者；

(b) 进程是设置-组-ID，而且当前用户并非该程序文件的组所有者；

(c) 用户没有写当前工作目录的许可权；

(d) core 文件太大。

## 4. 避免节点宕机

在企业生产环境下，DolphinDB 往往作为流数据中心以及历史数据仓库，为业务人员提供数据查询和计算。当用户较多时，不当的使用容易造成 server 端宕机。遵循以下建议，可尽量避免不当使用。

### 4.1 避免无限递归

用户在自定义递归函数时，如果不设置终止条件，就会导致无限递归。每次递归调用都会消耗堆栈空间，当堆栈空间耗尽时，就会引发堆栈溢出错误，最终导致进程终止。

例如调用以下递归函数会导致节点宕机，应避免类似定义。

```
def danger(x){
  return danger(x)+1
}

danger(1)
```

### 4.2 监控内存使用，避免内存高位运行

内存高位运行容易发生OOM，如何监控和高效使用内存详见 **内存管理** 中为分布式数据库提供写入缓存小节与流数据消息缓存队列小节

### 4.3 避免多线程并发访问某些内存表

DolphinDB内置编程语言，在操作访问表时有一些规则，如内存表详解并发性小节就说明了有些内存表不能并发写入。若不遵守规则，容易出现 server 崩溃。下例创建了一个以 id 字段进行 RANGE 分区的常规内存表：

```
t=table(1:0,`id`val,[INT,INT])
db=database("",RANGE,1 101 201 301)
pt=db.createPartitionedTable(t,`pt,`id)
```

下面的代码启动了两个写入任务，并且写入的分区相同，运行后即导致 server 系统崩溃。

```
def writeData(mutable t,id,batchSize,n){
	for(i in 1..n){
		idv=take(id,batchSize)
		valv=rand(100,batchSize)
		tmp=table(idv,valv)
		t.append!(tmp)
	}
}

job1=submitJob("write1","",writeData,pt,1..300,1000,1000)
job2=submitJob("write2","",writeData,pt,1..300,1000,1000)
```

产生的 core 文件如下图：

![](images/handle%20shutdown/handle_shutdown3-2.png)

### 4.4 自定义开发插件俘获异常

DolphinDB 支持用户自定义开发插件以扩展系统功能。插件与 DolphinDB server 在同一个进程中运行。若插件崩溃，整个系统（server）就会崩溃。因此，在开发插件时要注意完善错误检测机制。除了插件函数所在线程可以抛出异常（server 在调用插件函数时俘获了异常），其他线程都必须自己俘获异常，不得抛出异常。详情请参阅 [DolphinDB Plugin](https://gitee.com/dolphindb/DolphinDBPlugin/tree/release200#dolphindb-plugin)。

## 5. 总结

分布式数据库 DolphinDB 的设计十分复杂，发生宕机的情况各有不同。若发生节点宕机，请按本文所述一步步排查：

1. 排查是否为系统主动退出，如是否通过 Web 集群管理界面手动关闭节点或调用 stopDataNode 函数停止节点，是否用 kill 命令杀死节点进程，是否为 license 有效期到期退出等。当这些原因导致数据库宕机时，系统运行日志会记录相关的信息，请检查对应时间点是否有相应的操作；
2. 排查是否因为内存耗尽而被操作系统杀掉。排查 OOM killer 可查看操作系统日志；
3. 检查是否有使用不当的脚本，如多线程并发访问了没有共享的分区表、插件没有俘获一些异常等；
4. 请查看 core 文件，用 gdb 调试获取堆栈信息。若确定系统有问题，请保存节点日志、操作系统日志和 core 文件，并及时与 DolphinDB 工程师联系。
