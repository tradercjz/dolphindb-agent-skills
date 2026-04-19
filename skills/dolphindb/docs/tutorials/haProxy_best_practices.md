<!-- Auto-mirrored from upstream `documentation-main/tutorials/haProxy_best_practices.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 使用 HAProxy 实现负载均衡

HAProxy 是一款基于 C 语言开发的开源软件，用于提供高可用性、负载均衡和基于 TCP（第四层）和 HTTP（第七层）应用的代理服务，是一种免费、快速、可靠的解决方案，因其优异的性能在如今各大主流网页上得到了广泛的应用。

DolphinDB 作为一款可用于搭建高可用数据集群的时序数据引擎，其在实际生产环境的应用中对高并发、大流量的处理对实际应用性能具有更高的要求。本次教程为此类生产环境中的实践需求提供了一个解决方案，将 HAProxy 引入到 DolphinDB 的高可用集群中，通过使用 HAProxy 所提供的特定功能来实现 DolphinDB 数据节点的负载均衡。

## 概述

* **软件简介**

  HAProxy 是一款由 Linux 内核贡献者在2000年基于 C 语言开发的一款开源软件，用于为基于 TCP （第四层）和 HTTP（第七层）协议的应用程序提供高可用性、负载均衡和代理服务等。它具有高可用性、负载均衡、健康检查、会话保持、SSL、监控统计等多种核心功能。其良好的可扩展性、对高并发大流量的支持以及对 CPU、内存资源等的高效利用，使得其在当今诸如诸如 GitHub, Bitbucket, Stack Overflow, Reddit, Tumblr, Twitter 和 Tuenti 等的主流网站上得到了广泛应用。

  HAProxy 作为一款类似于软件应用中间件的工具，其主要包含两个部分：前端，定义用于接收从客户端发来的请求的端口；后端，用于将从前端接收过来的请求交付于后端的应用服务处理，一般来说一个前端的代理服务端口可以对应多个后端应用服务。HAProxy 主要起到了代理服务以及负载均衡的中间件作用，实现将高并发、大流量的请求平均分配到后端多个服务上。

  ![](images/haProxy_best_practices/1_1.png)
* **官方教程、下载、安装**

  HAProxy 由 Linux 内核的核心贡献者 Willy Tarreau 于 2000 年编写，他现在仍然负责该项目的维护，并在开源社区免费提供版本迭代。本文示例使用 HAProxy [2.6](https://www.haproxy.com/blog/announcing-haproxy-2-6/)。推荐使用最新稳定版的 HAProxy，详情见[已发布的 HAProxy 版本](http://www.haproxy.org/)。

**HAProxy 部分核心功能介绍**

* 高可用性：HAProxy 提供优雅关闭服务和无缝切换的高可用功能；
* 负载均衡：L4 (TCP) 和 L7 (HTTP) 两种负载均衡模式，至少 9 类均衡算法，比如 roundrobin, leastconn, random 等；
* 健康检查：对 HAProxy 配置的 HTTP 或者 TCP 模式状态进行检查；
* 会话保持：在应用程序没有提供会话保持功能的情况下，HAProxy 可以提供该项功能；
* SSL：支持 HTTPS 通信和解析；
* 监控与统计：通过 web 页面可以实时监控服务状态以及具体的流量信息。

利用这些核心功能，可以实现为 DolphinDB 实现负载均衡、健康检查等功能，下文将以四个数据节点的集群为例，为大家逐步介绍安装部署、启动服务的过程。

## 环境部署

* **硬件环境：**

  | 硬件名称 | 配置信息 |
  | --- | --- |
  | 主机名 | HostName |
  | 外网 IP | xxx.xxx.xxx.122 |
  | 操作系统 | Linux（内核版本3.10以上） |
  | 内存 | 64 GB |
  | CPU | x86\_64（12核心） |
* **软件环境：**

  | 软件名称 | 版本信息 |
  | --- | --- |
  | DolphinDB | V2.00.8 |
  | HAProxy | 2.6.2 |
  | Docker | 3.0及以上 |

**注意**：本教程包含了如何在 docker 环境下安装、部署 HAProxy 的内容，需要提前安装 docker。具体安装方法可以参考 [docker 官方教程](https://docs.docker.com/get-docker/)。

## HAProxy 安装、部署、应用流程

**注意**：在流程开始前建议预先构建具有多数据节点 DolphinDB 高可用集群。具体安装方法可以参考 DolphinDB 高可用集群部署教程。也可以参考基于 Docker-Compose 的 DolphinDB 多容器集群部署。

### 安装

* **主机环境**

  首先，在安装 HAProxy 之前要确保主机上安装了 `epel-release` 、`gcc` 、`systemd-devel` 三个依赖包。执行如下命令安装：

  ```
  yum -y install epel-release gcc systemd-devel
  ```

  下载 HAProxy 2.6.2 的源码包并解压：

  ```
  wget https://www.haproxy.org/download/2.6/src/haproxy-2.6.2.tar.gz && tar zxf haproxy-2.6.2.tar.gz
  ```

  执行如下命令编译源码：

  ```
  cd haproxy-2.6.2
  make clean
  make -j 8 TARGET=linux-glibc USE_THREAD=1
  make PREFIX=${/haproxy} SBINDIR=${/haproxy/bin} install  # 根据实际情况将 `${/haproxy}` 和 `${/haproxy/bin}` 替换为实际路径
  ```

  重新配置 *profile* 文件，其中 `/path/haproxy/bin` 需替换为实际目录：

  ```
  echo 'export PATH=/path/haproxy/bin:$PATH' >> /etc/profile
  . /etc/profile
  ```

  执行如下命令查看是否安装成功：

  ```
  which haproxy
  ```
* **docker 环境**

  执行如下命令拉取 HAProxy 的 docker 镜像，这里我们选择 *haproxytech/haproxy-alpine:2.6.2*.

  ```
  docker pull haproxy:2.6.2-alpine
  ```

### 创建 HAProxy 用户

在启动 HAproxy 前须确保配置文件中用户和用户组已正确配置。例如对于下文配置文件中的用户 haproxy 和 用户组 haproxy，可使用如下命令配置：

```
sudo groupadd haproxy
sudo useradd -g haproxy haproxy
```

### 配置 DolphinDB 集群端口监控

**HTTP 模式**

在主机上创建 *haproxy.cfg* 文件，并配置如下配置项：

```
global                           #定义全局配置
    log         127.0.0.1 local2 #定义全局的 syslog 服务器，最多可以定义两个。
    maxconn     4000
    user haproxy
    group haproxy

defaults
    mode                    http               #工作模式为 http
    log                     global             #日志继承全局配置的设置
    option                  httplog            #日志类别,采用 httplog
    option                  dontlognull        #空连接不记录在日志中
    option http-server-close
    option forwardfor       except 127.0.0.0/8 #实现 IP 穿透
    option                  redispatch         #服务不可用后重定向到其他健康服务器。
    retries                 3                  #上游服务器尝试连接的最大次数，此处为3
    timeout http-request    10s
    timeout queue           1m                 #在请求队列中排队的最大时长
    timeout connect         10s                #haproxy和服务端建立连接的最大时长
    timeout client          1h                 #和客户端保持空闲连接的最大时长
    timeout server          1h                 #和服务端保持空闲连接的最大时长
    timeout http-keep-alive 10s                #开启与客户端的会话保持时间，为10s
    timeout check           10s
    maxconn                 3000               #定义客户端与服务器端的最大连接数为3000

frontend    ddb_fronted
    bind        *:8080 #前端用于接收请求的端口
    mode        http
    log         global
    default_backend ddb_backend

backend ddb_backend
    balance roundrobin #这里使用了动态加权轮询算法，支持权重的运行时调整及慢启动机制，是一种最公平、最平衡的算法
    # 检测服务器端口端口，频率为每 5 秒一次。如果 2 次检测成功，则认为服务器可用；如果 3 次检测失败，则认为服务器不可用。
    server node1 xxx.xxx.xxx.1:9302 check inter 5s rise 2 fall 3
    server node2 xxx.xxx.xxx.2:9302 check inter 5s rise 2 fall 3
    server node3 xxx.xxx.xxx.3:9302 check inter 5s rise 2 fall 3
    server node4 xxx.xxx.xxx.4:9302 check inter 5s rise 2 fall 3

listen stats
    mode    http
    bind    0.0.0.0:1080    #监控页面的访问端口
    stats   enable
    stats   hide-version
    stats uri /haproxyamdin #监控页面的 uri
    stats realm Haproxy     #监控页面的提示信息
    stats auth admin:admin  #监控页面的访问用户名加密码，此处均为 admin
    stats admin if TRUE
```

**TCP 模式**

```
global                           #定义全局配置
    log         127.0.0.1 local2 #定义全局的 syslog 服务器，最多可以定义两个。
    maxconn     4000
    user haproxy
    group haproxy

defaults
    mode                    tcp               #工作模式为 tcp
    log                     global             #日志继承全局配置的设置
    option                  tcplog            #日志类别,采用 tcplog
    option                  dontlognull        #空连接不记录在日志中
    option http-server-close
    option                  redispatch         #服务不可用后重定向到其他健康服务器。
    retries                 3                  #上游服务器尝试连接的最大次数，此处为3
    timeout http-request    10s
    timeout queue           1m                 #在请求队列中排队的最大时长
    timeout connect         10s                #haproxy和服务端建立连接的最大时长
    timeout client          1h                 #和客户端保持空闲连接的最大时长
    timeout server          1h                 #和服务端保持空闲连接的最大时长
    timeout http-keep-alive 10s                #开启与客户端的会话保持时间，为10s
    timeout check           10s
    maxconn                 3000               #定义客户端与服务器端的最大连接数为3000

frontend    ddb_fronted
    bind        *:8080 #前端用于接收请求的端口
    mode        tcp
    log         global
    default_backend ddb_backend

backend ddb_backend
    balance roundrobin #这里使用了动态加权轮询算法，支持权重的运行时调整及慢启动机制，是一种最公平、最平衡的算法
    # 检测服务器端口端口，频率为每 5 秒一次。如果 2 次检测成功，则认为服务器可用；如果 3 次检测失败，则认为服务器不可用。
    server node1 10.0.0.80:8802 check inter 5s rise 2 fall 3 send-proxy
    server node2 10.0.0.81:8802 check inter 5s rise 2 fall 3 send-proxy
    server node3 10.0.0.82:8802 check inter 5s rise 2 fall 3 send-proxy

listen stats
    mode    http
    bind    0.0.0.0:1080    #监控页面的访问端口
    stats   enable
    stats   hide-version
    stats uri /haproxyamdin #监控页面的 uri
    stats realm Haproxy     #监控页面的提示信息
    stats auth admin:admin  #监控页面的访问用户名加密码，此处均为 admin
    stats admin if TRUE
```

**注意**：

* 两种模式的配置文件中后端服务器的 ip 和端口要根据实际情况进行修改。
* TCP 模式中 listen stats mode 须配置为 http。
* `check inter 5s rise 2 fall 3` 配置了节点检测与切换频率。其中，`inter 5s` 表示每 5 秒检查一次节点状态；`rise 2` 表示连续成功检测 2 次后，该节点将被标记为可用；`fall 3` 表示连续失败检测 3 次后，该节点将被标记为不可用，并触发节点切换。如果希望缩短检测并切换失效节点的时间，可以通过减少单次检测的间隔时间和判定所需的检测次数来实现。例如，将配置修改为 `check inter 2s rise 2 fall 2`，检测节点失效的时间将从约 15 秒缩短至约 4 秒。

### 服务启动

在主机环境下，执行如下命令启动 HAProxy，其中 -f 后接配置文件所在地址，默认为 */etc/haproxy/haproxy.cfg*，此处为 */haproxy/haproxy.cfg* 。

```
haproxy -f /haproxy/haproxy.cfg
```

在 docker 环境下，执行如下命令创建容器，注意要将监控端口和前端端口映射到主机上，同时将在主机上配置好的 *haproxy.cfg* 文件映射到容器内：

```
docker run -itd --name ddb_haproxy -p 8080:8080 -p 1080:1080 -v /haproxy/haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg --privileged=true haproxy:2.6.2-alpine
```

启动成功后，用户就可以使用 DolphinDB 的 VScode 插件和 DolphinDB GUI 连接 HAProxy 用于接收请求的前端端口8080来访问 DolphinDB 的集群服务。假如访问8080端口，出现如下为访问 DolphinDB 数据节点端口的浏览器页面时，证明 HAProxy 部署成功。

![](images/haProxy_best_practices/3_1.png)

**注意**：使用 DolphinDB 客户端工具连接监听的代理端口时，HAProxy 的负载均衡功能会根据相应的算法规则等自动分配连接到后端部署的其中之一节点。

### 高可用

Keepalived 是一款轻量级的高可用解决方案，通过实现 VRRP 协议动态管理虚拟 IP 地址（VIP），可在主备节点之间实现自动切换。在本次部署中，当 Haproxy 主节点发生故障时，Keepalived 能够检测到服务异常并将 VIP 自动切换至备用节点，从而确保 Haproxy 服务的连续性与稳定性。

HAProxy 分别在主备机器上部署好以后，按照以下步骤在主备机器上依次部署 Keepalived。

**部署 Keepalived**

1. 安装依赖包

   运行以下命令安装必要的依赖包：

   ```
   yum -y install gcc openssl-devel pcre2-devel systemd-devel openssl-devel
   ```
2. 下载并安装 Keepalived

   从 Keepalived 官网下载 2.3.0 版本的安装包并进行编译安装：

   ```
   tar zxf keepalived-2.3.0.tar.gz
   cd keepalived-2.3.0

   ./configure
   make
   make install
   ```
3. 配置 Master/Backup（主/备节点）服务

   ```
   vim /etc/keepalived/keepalived.conf
   ```

   根据主节点和备用节点分别设置：

   ```
   # 配置文件内容如下：
   ! Configuration File for keepalived

   global_defs {
     router_id ha_1                   # backup 改为 ha_2
     vrrp_iptables
     vrrp_garp_interval 0
     vrrp_gna_interval 0
   }

   vrrp_script chk_haproxy {
      script "/usr/sbin/pidof haproxy"    # 检查 haproxy 进程是否存在
      interval 2                      # 每 2 秒检查一次
      weight -30                      # 如果检查失败，减少 30 优先级
   }

   vrrp_instance VI_1 {
      state MASTER                    # backup 改为 BACKUP
      interface eth1                  # 替换为机器的真实网卡名
      virtual_router_id 51
      priority 100                    # backup 配置为 80
      advert_int 1
      authentication {
          auth_type PASS
          auth_pass 1111
      }
      virtual_ipaddress {
          10.0.0.100                # 修改为真实环境中的 VIP
      }
      track_script {
          chk_haproxy
      }
   }
   ```

   其中:

   * MASTER/BACKUP：state 的值分别设为 MASTER 和 BACKUP，分别表示主节点和备用节点。
   * 网卡配置：interface 配置为 HAProxy 使用的网卡。
   * VIP 配置：应在与主备节点一致的子网下。

   例如，通过以下命令查看本节点 IP：

   ```
   ip a
   ```

   ![](images/haProxy_best_practices/3_2.png)

   本文示例通过 10.0.0.81:8080 访问 HAProxy，则 interface 配置为 eth1；主节点为 10.0.0.80，备用节点为 10.0.0.81，则 VIP 可写为 10.0.0.xxx ，此处设定为 10.0.0.100。
4. 启动 Keepalived

   ```
   systemctl restart keepalived.service  # 重启
   systemctl enable keepalived.service  # 随系统自启动
   systemctl status keepalived.service   # 查看状态
   ```

   Keepalive 启动后，主节点的服务会绑定到 VIP，用户可以通过 VIP 访问 Haproxy 服务，例如：10.0.0.100:8080。如果主节点下的 Haproxy 服务不可用，Keepalived 会将备用节点提升为新主节点，并将该节点的服务绑定到 VIP，从而确保 VIP 的持续可用。可以使用查看状态的命令来确认当前节点是否为主节点，或者通过指令检查当前节点的网卡是否绑定了 VIP，绑定 VIP 的节点即为主节点。

   ```
   ip addr show eth1
   ```

   ![](images/haProxy_best_practices/3_3.png)

### 运维

* **监控页面查看**

  在可以访问到 HAProxy 部署主机的任一机器上的浏览器中输入部署主机 ip: 监听端口以及配置的 URI，此处为 `xxx.xxx.xxx.122:1080/haproxyamdin`，访问监控页面。

  ![](images/haProxy_best_practices/3_4.png)
* **HAProxy服务重启、终止**

  在 HAProxy 服务的实际使用过程中，需要通过终止或重启服务来实现配置文件修改生效等操作。

  在主机环境下，首先执行如下命令找到正在运行的 HAProxy 进程 PID：

  ```
  ps -ef | grep haproxy
  ```

  其次，使用 `kill` 命令终止正在运行的 HAProxy 进程：

  ```
  kill -9 ${haproxy_pid} #${haproxy_pid}为实际进程数
  ```

  如需要重启则再次执行 `haproxy -f` 命令。

  而在 docker 环境下，可以通过如下命令重启服务

  ```
  docker restart ddb_haproxy
  ```

  如需终止且彻底删除容器，则可以执行如下命令：

  ```
  docker stop ddb_haproxy && docker rm ddb_haproxy
  ```
