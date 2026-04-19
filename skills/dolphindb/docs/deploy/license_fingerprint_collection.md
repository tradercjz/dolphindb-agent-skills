<!-- Auto-mirrored from upstream `documentation-main/deploy/license_fingerprint_collection.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 如何采集服务器指纹生成 DolphinDB License

## 1. license文件说明

注：

请勿随意更改机器的软硬件配置，否则可能导致指纹信息变更，从而使 license 失效，进而导致 DolphinDB 无法启动。

DolphinDB 的付费 license 均需绑定用户对应的机器指纹（机器唯一标识）进行制作，license
文件授权用户所能够使用的软硬件资源，包括CPU、内存、节点数及有效日期等。在启动及运行过程中，DolphinDB 进程会校验 license 文件的有效性。

## 2. 指纹文件采集

### 2.1 主机环境

这里的主机环境指的是非容器化的环境，比如一个虚拟或物理的操作系统。

（1）在服务器下载社区版解压，以交互方式启动 DolphinDB。

```
./dolphindb
```

（2）在 DolphinDB 命令行交互界面，执行 `generateMachineFingerprint` 函数。

```
login("admin", "123456");
//指纹文件的输出目录，请替换为合适的路径
generateMachineFingerprint('/yourPath/fingerprint-S100');
```

注：

* 请确保 DolphinDB 进程具备该目录的读写权限。
* 每行命令一定要以 ; 结束。

（3）社区版建议将输出指纹文件以“MachineFingerprint”命名，方便制作及替换 license
文件时进行区分。商业部建议采用更具区分度的命名方式，格式为： fp\_<机器名>\_<mem>\_<cores>\_<nodes>，
其中包含机器名、内存、核心数和节点数等信息。

```
tar -zcvf fp_S100_512_32_6.tar.gz /yourPath/fingerprint-S100
```

（4）将压缩文件提交给 DolphinDB 官方。

### 2.2 Docker 容器指纹采集

#### 2.2.1 宿主机为 Linux 系统

（1）license 需要验证 hostname，CPU 等信息。采集指纹时需要挂载宿主机的 /etc 目录。将 license
文件保存路径映射到宿主机；容器启动时指定容器的 hostname。

```
docker run -itd --hostname cnserver10  -v /etc:/dolphindb/etc  -v /root/dolphindb.lic:/data/ddb/server/dolphindb.lic -p 18800:8848  dolphindb/dolphindb:v1.30.16 bash
```

* `--hostname`：容器的主机名称，需指定，下次启动不能修改。
* `-v`：主机路径与容器路径的映射关系：
  + 将宿主机保存 license 文件的目录映射到容器内部对应路径。
  + 将宿主机的 /etc 目录映射到容器内部，因为 DolphinDB 在生成或验证 license 时需读取主机的
    CPU、网卡等硬件信息，而这些信息可能依赖 /etc 中的配置文件。
* `-p`：容器端口与主机端口的映射关系，本例将宿主机的 18800 端口映射到 dolphindb 进程的
  8848 端口。

（2）连接 dolphindb

```
//自行修改输出文件路径
generateMachineFingerprint('/yourPath/fingerprint-S100');
```

(3) 在每个容器上执行上述步骤获取指纹文件。社区版建议将输出指纹文件以“MachineFingerprint”命名，方便制作及替换 license
文件时进行区分。商业部建议采用更具区分度的命名方式，格式为： fp\_<机器名>\_<mem>\_<cores>\_<nodes>，
其中包含机器名、内存、核心数和节点数等信息。产生的指纹为容器内部的路径，执行下面命令将指纹文件拷贝出来，进行制作。

```
docker cp  96f7f14e99ab:/yourPath/fingerprint-S100 /tmp/
```

以上命令将容器 96f7f14e99ab 的 /yourPath/fingerprint-S100 目录拷贝到主机的 /tmp 目录。

#### 2.2.2 宿主机为 Windows 系统

（1）在 windows 上安装 WSL 子系统。

```
docker run -itd --hostname cnserver10  -v /etc:/dolphindb/etc  -v /home/dolphindb/dolphindb.lic:/data/ddb/server/dolphindb.lic -p 18804:8848  ubuntu:20.04 bash
```

进入容器安装 tzdata 以及三个网络组件。

```
apt-get update
apt-get upgrade
apt-get install -y tzdata
apt install net-tools
apt-get install inetutils-ping
apt-get install openssh-server
```

（2）进入容器采集指纹

参考 2.2.1 所述采集指纹。

## 3. license 更新

商业版的 license 支持在线更新，无需停止现有集群。将获取的 license 文件覆盖原 license 文件（server 目录下的 dolphindb.lic）
。替换完成后， 连接任意一节点， 执行如下的 Dlang 脚本。

```
use ops
updateAllLicenses()
```
