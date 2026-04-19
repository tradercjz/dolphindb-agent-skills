<!-- Auto-mirrored from upstream `documentation-main/sys_man/secure_conn.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 安全通信

DolphinDB 支持 Web 上 HTTPS 安全通信。

## Web访问权限

DolphinDB 可以设置 Web 集群管理器的访问权限。DolphinDB 第一次启动时，系统会自动创建用户名称为
"admin"，密码为 "123456" 的管理员账号。

有关用户权限设置，请参考 用户权限管理。

## 启用 HTTPS

有两种方式启用 HTTPS：

* 在集群控制节点的配置文件（controller.cfg）中添加如下配置："enableHTTPS=true"，和
  publicName（必须为域名）。
* 使用命令行启动集群控制节点时，加上"-enableHTTPS true" 和 "-publicName
  xxxx"。

  ```
  ./dolphindb -enableHTTPS true -home master -publicName www.psui.com -mode controller -localSite 192.168.1.30:8500:rh8500 -logFile ./log/master.log
  ```

注：

若数据节点或代理节点需启用 HTTPS，则应在代理节点配置文件中设置上述两个参数。

## HTTPS 证书

我们需要在DolphinDB的每台服务器上安装服务器身份验证证书来进行安全连接。控制节点和每个代理节点都需要安装证书。数据节点/计算节点使用同一台服务器上的代理节点的证书。

*使用证书颁发机构的身份验证证书：*

从证书颁发机构获取证书，把它重命名为server.crt，然后复制到控制节点主目录下的"keys"目录（如目录不存在需手动创建）。同时，将服务器的独立私钥文件
serverPrivate.key 一并放置在该目录下，否则系统在生成密钥时会覆盖原有文件。由证书颁发机构获取的证书无需额外安装。

*按照以下步骤安装自签名证书：*

1. 把publicName设置为计算机的域名。

   在集群控制节点的配置文件(controller.cfg)中加上"publicName=www.ABCD.com"，或者在命令行窗口启动控制节点时加上"-publicName
   www.ABCD.com"。
2. 检查证书是否生成。

   启动控制节点，并且检查证书文件server.crt和服务器的独立密钥serverPrivate.key是否存在主目录的“keys”目录下。
3. 把自签名证书安装到浏览器的证书颁发机构。

   在Google Chrome，选择 设置 -> 高级 -> 管理证书 -> 颁发机构 ->
   导入，把server.crt导入。

   在浏览器地址栏中输入 *https://www.ABCD.com:8500/*
   连接到DolphinDB集群管理器，其中8500是控制节点的端口

## SSO（单点登录）

DolphinDB 提供了两个用于 SSO 的函数：

* `getAuthenticatedUserTicket()`：发行当前用户的加密
  ticket。
* `authenticateByTicket(ticket)`：使用
  `getAuthenticatedUserTicket` 生成的 ticket 登录系统。
