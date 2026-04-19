<!-- Auto-mirrored from upstream `documentation-main/tutorials/nginx_dolphindb.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 定义上游服务器集群
upstream dolphindb_data {
    least_conn;
    server 192.168.1.10:8902;
    server 192.168.1.11:8902;
}

upstream dolphindb_control {
    server 192.168.1.12:8902;
}

server {
    listen 80;                # 监听端口80
    server_name  _;                 # 匹配任意主机名（下划线表示默认主机）
    location / {
        proxy_pass http://dolphindb_data;   # 转发请求到上游数据节点
        proxy_http_version 1.1;                # 使用HTTP/1.1与后端通信
        proxy_set_header Host $host;           # 保留原始Host头
        proxy_set_header X-Real-IP $remote_addr;        # 传递客户端真实IP
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;  # 记录代理链IP
        # WebSocket 配置：
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        # 超时配置：
        proxy_connect_timeout 30s;
        proxy_read_timeout 7d;
        proxy_send_timeout 7d;
    }
}

server {
    listen 81;                # 监听端口81
    server_name  _;                 # 匹配任意主机名（下划线表示默认主机）
    location / {
        proxy_pass http://dolphindb_control;   # 转发请求到上游控制节点
        proxy_http_version 1.1;                # 使用HTTP/1.1与后端通信
        proxy_set_header Host $host;           # 保留原始Host头
        proxy_set_header X-Real-IP $remote_addr;        # 传递客户端真实IP
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;  # 记录代理链IP
        # WebSocket 配置：
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        # 超时配置：
        proxy_connect_timeout 30s;
        proxy_read_timeout 7d;
        proxy_send_timeout 7d;
    }
}
```

**配置说明：**

* `upstream`定义了一个上游服务器集群，名称为
  `dolphindb_cluster`。里面列出了三台后端 DolphinDB
  节点的地址和端口。默认情况下，不指定策略即为轮询（round-robin）方式，每个请求依次轮流分配到不同节点上。设定`least_conn`表示选择较少连接的服务器（least\_conn）优先。
* `server` 定义了前端代理服务的监听行为。`listen 80;` 指定在
  80 端口接受客户端请求。`server_name _;` 使用下划线 \_
  作为服务名，表示一个通配的默认主机（意味着无论请求的 Host
  为何，都由此虚拟主机处理）。在实际部署中，如果有特定域名，可在此处指定。
* `location /`
  来匹配所有以`/`开头的请求路径（即对整个站点的请求都处理）。
  + `proxy_pass`
    指定了请求转发的目标：`http://dolphindb_cluster`。这里使用了上面定义的上游集群名称。
  + `proxy_set_header`
    和相关指令用于配置当前`server`块代理转发时的HTTP请求头和连接参数，与上一步中的http全局配置含义相同。为了提高代理的健壮性，我们设置了一些超时参数：
  + `proxy_connect_timeout 30s;` 定义连接后端 DolphinDB
    的超时时间（握手超时）。如果在10秒内无法建立与任一后端的TCP连接，Nginx 将返回错误。
  + `proxy_send_timeout 7d;` 定义向后端发送请求数据的超时时间。
  + `proxy_read_timeout 7d;`
    定义从后端读取响应的**静默超时时间**。默认值为60秒，如果超过60秒后端没有任何响应数据发送，Nginx
    将关闭该连接。对于 WebSocket 长连接场景，建议将此值适当延长，否则当连接空闲超过60秒时，Nginx
    会认为后端不响应而切断连接，导致 WebSocket 意外断开（浏览器会收到 1006
    异常码）。本例将其延长至7d。总之，`proxy_read_timeout`
    要根据业务情况（如数据推送频率）进行调整，以平衡及时释放闲置连接和保持长连接不断开的需求。

#### 2.2.4 重载 Nginx 激活上述配置

当我们完成这些配置并保存到 `nginx.conf` 后，可以重载 Nginx：

```
/usr/local/webserver/nginx/sbin/nginx -s reload
```

此时，Nginx 会在 80 端口等待请求，并按照配置将请求反向代理到 DolphinDB 集群的各节点上。

#### 2.2.5 访问方式

在浏览器中输入:

```
http://nginx地址IP:配置中的监听端口
```

或在 VSCode DolphinDB 插件中Connection的配置中添加:

```
"dolphindb.connections": [
    {
        "name": "nginx",
        "url": "ws://nginx地址IP:配置中的监听端口",
        "autologin": true,
        "username": "admin",
        "password": "123456"
    }
]
```

### 2.3 TCP 协议下通过 Nginx 反向代理 DolphinDB

该方法适用于Python API或其他API中连接DolphinDB。

![](images/nginx_dolphindb/2-1.png)

图 2. TCP 协议下反向代理架构

#### 2.3.1 编辑 nginx.conf 文件

与 `http {}` 同级下方，添加 stream {} 块，用82和83端口反向代理数据和控制节点：

```
stream {
    upstream dolphindb_data {
        server 192.168.1.10:8902;
        server 192.168.1.11:8902;
    }
    server {
        listen 82;
        proxy_pass dolphindb_data;
    }

    upstream dolphindb_control {
        server 192.168.1.12:8902;
    }
    server {
        listen 83;
        proxy_pass dolphindb_control;
    }
}
```

注：

**stream块和http块中配置的端口（80，81）不能一样，**否则会因为 Nginx
不能自动识别TCP/HTTP协议转发而报错。

#### 2.3.2 重载 Nginx

```
/usr/local/webserver/nginx/sbin/nginx -s reload
```

#### 2.3.3 在 Python 中连接

```
import dolphindb as ddb
s = ddb.session()
s.connect("192.168.1.20", 82)  # 或 83
```

### 2.4 使用 SSL 加密 WebSocket 和 TCP 代理

在实际部署过程中，若需对Nginx 反向代理 DolphinDB 的 HTTP 接口（浏览器，客户端，VScode）与 TCP通信接口（如用于
Jupyter、Python api等）进行SSL/TLS加密，此处以上文中的控制节点为例，有以下步骤：

#### 2.4.1 确保 Nginx 下载时已启用此配置

```
--with-http_ssl_module --with-stream_ssl_module
```

#### 2.4.2 修改 Nginx 配置文件的 http 部分

```
http{
    upstream dolphindb_control {
        server 192.168.1.12:8902;
    }

    server {
        listen 81 ssl;
        ssl_protocols       TLSv1 TLSv1.1 TLSv1.2;
        ssl_ciphers         AES128-SHA:AES256-SHA:RC4-SHA:DES-CBC3-SHA:RC4-MD5;
        ssl_certificate     /path/to/server.crt;
        ssl_certificate_key /path/to/server.key;

        location / {
            proxy_pass http://dolphindb_control;
            proxy_http_version  1.1;

            proxy_set_header    Host            $host;
            proxy_set_header    X-Real-IP       $remote_addr;
            proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;

            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection $connection_upgrade;

            proxy_connect_timeout 30s;
            proxy_read_timeout 7d;
            proxy_send_timeout 7d;
        }
    }
}
```

和无SSL加密时的主要配置区别：

* `listen 81` 后增加了 `ssl`
* 指定了 SSL 协议和加密方法
* 指定了必要的 SSL
  证书与头信息的地址，可以无需CA，使用openssl以下指令自颁发生成自签名证书和私钥:

  ```
  openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout server.key -out server.crt
  ```

#### 2.4.3 修改 Nginx 配置文件的 stream 部分

```
stream {
    upstream dolphindb_control {
        server 192.168.1.12:8902;
    }

    server {
        listen 83 ssl;
        ssl_protocols       TLSv1 TLSv1.1 TLSv1.2;
        ssl_ciphers         AES128-SHA:AES256-SHA:RC4-SHA:DES-CBC3-SHA:RC4-MD5;
        ssl_certificate     /path/to/server.crt;
        ssl_certificate_key /path/to/server.key;
        proxy_pass dolphindb_control;
    }
}
```

#### 2.4.4 重载 Nginx

```
/usr/local/webserver/nginx/sbin/nginx -s reload
```

#### 2.4.5 访问方法

端口 81：用于 Web HTTPS访问控制节点，`https://192.168.1.20:81/`。

端口 83：用于 API 访问控制节点，TCP over SSL 的代理转发，此时的ddb连接配置需加一项
`enableSSL=True`。

```
import dolphindb as ddb
s = ddb.session(enableSSL=True)
s.connect("192.168.1.20", 83)
```

## 3. 常见问题解答（FAQ）

### 3.1 WebSocket 握手失败（错误码 1006）

如果在通过 Nginx 访问 DolphinDB 的 WebSocket 服务时，前端报错 `code: 1006, reason:
"abnormal closure"` 或 `Connection header must include
'Upgrade`*'*，通常是由于握手协议头未正确转发导致的。解决办法是确保在 Nginx 配置中包含
`proxy_http_version 1.1;` 以及 `Upgrade` 和
`Connection` 头设置。

`proxy_set_header Upgrade $http_upgrade;` 将客户端请求中的 “Upgrade”
头的值传递给后端（一般为 “websocket”），而 `proxy_set_header Connection
"upgrade";` 则明确告诉后端希望升级连接。这两个指令是实现 WebSocket 握手的关键，缺少它们会导致后端无法识别为
WebSocket 请求，从而握手失败。例如，后端可能报出 *“Connection header must include 'Upgrade'”*
之类的错误。配置了以上头信息后，Nginx 收到 WebSocket 请求会将协议升级所需的头信息正确地传递给 DolphinDB 后端，使 WebSocket
可以建立长连接。

此处简单地将 Connection 固定设为 "upgrade" 来配合 Upgrade 头。如果还需要同时兼顾普通 HTTP 请求长连接，可以使用 Nginx
内置变量更优雅地处理。例如利用 `map` 指令，根据 `$http_upgrade` 是否为空设置
`$connection_upgrade` 变量为 "upgrade" 或 "close"，然后
`proxy_set_header Connection $connection_upgrade;`。这样既满足
WebSocket 升级，也不会在非 WebSocket请求时误设 Connection。但对 DolphinDB API 的场景而言，大部分请求可能涉及
WebSocket（如 Web 前端交互或流数据订阅），所以本文直接使用固定值简化配置。

### 3.2 多节点下启用了 keepalive 导致连接失败

在单节点情况下，`upstream` 配置中启用 `keepalive`
时，可以提升性能（避免每次重建TCP连接），但在多节点情况下，对于 WebSocket 这类**长寿命连接**而言，可能出现某些副作用。Nginx
无法感知连接是否还被 WebSocket 占用，容易误用被挂起的连接。因此在多节点状况下，请确保无类似 `keepalive
16;` 的配置。

### 3.3 每次登录到的节点不一样

在默认轮询策略或者本文配置的负载均衡策略（`least_conn`）下，每个请求可能落到不同的后端节点。如果应用场景对“会话粘性”有要求（例如某一用户登录后的所有请求应由同一节点处理），可在
`upstream` 配置中将 `least_conn` 改为
`ip_hash;`，这会根据客户端 IP 将请求固定转发到同一个后端节点。

### 3.4 VS Code 访问成功，浏览器访问不成功

清除浏览器缓存重试。

## 4. 附录

WebSocket 和TCP 示例完整配置文件：[nginx.conf](script/nginx_dolphindb/nginx.zip)。

SSL加密的WebSocket 和TCP 示例完整配置文件：[nginx\_ssl.conf](script/nginx_dolphindb/nginx_ssl.zip)。
