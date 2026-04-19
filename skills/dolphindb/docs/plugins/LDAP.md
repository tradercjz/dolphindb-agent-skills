<!-- Auto-mirrored from upstream `documentation-main/plugins/LDAP.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# LDAP

The Lightweight Directory Access Protocol（LDAP）是一种软件协议 ，使任何人都可以在公共互联网或公司内网上查找网络中的组织、个人和其他资源的数据。LDAP 常用来为身份验证服务提供存储用户名和密码的功能。DolphinDB 提供 LDAP 插件，用于搜索 LDAP 服务器内的条目信息，进而实现在 DolphinDB 中进行 LDAP 第三方验证登录功能。

## 安装插件

### 版本要求

DolphinDB Server 2.00.10 及更高版本，支持 Linux x86-64。

### 安装步骤

1. 在 DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   注意：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可[自行编译](https://gitee.com/dolphindb/DolphinDBPlugin)（请选择对应分支下的插件）或在 [DolphinDB 用户社区](https://ask.dolphindb.cn/)进行反馈。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   ```
   installPlugin("LDAP")
   ```
3. 使用 `loadPlugin` 命令加载插件。

   ```
   loadPlugin("LDAP")
   ```

## 接口说明

### search

**语法**

```
LDAP::search(host, dn, password, searchBase, filter, [attrs], [option], [searchScope], [saslMechanism])
```

**详情**

搜索 ldap 服务器内相关条目信息。返回一个 key 类型为 STRING、value 类型为 ANY 的 Dictionary，key 内容为对应条目的 *dn*，value 内容为一个 key、value 类型均为 STRING 的 Dictionary，其对应 *dn* 的属性值。

**参数**

**host** STRING 类型标量，ldap 服务器地址，需要以 ldap:// 开头。

**dn** STRING 类型标量，绑定的账户。如果不需要验证用户名与密码，则填空字符串即可。

**password** STRING 类型标量，绑定账户的密码，如果不需要验证用户名与密码，则填空字符串即可。

**searchBase** STRING 类型标量，查询的 base。

**filter** STRING 类型标量，查询的过滤器，指定为空时为查询 searchBase 下所有条目。

**attrs** STRING 类型向量，可选，表示需要查询的参数字段名。如果不为空，则只查询该向量内指定的参数，返回的 dict 中各个条目只会包含 *attrs* 中出现的参数字段。存在一些特殊用法：

* 传入 `+` 会输出所有 operational attribute 操作属性。
* 传入 `*` 会输出所有 user attribute 用户属性。
* 如果输入的是一个 `@{objectClass 名称}`，则会以该类包含的参数字段来过滤输出的参数字段。

具体可以参考 The ldapsearch Command-Line Tool 中 *attrs* 相关描述。

**option** 字典类型，用于设置 LDAP 连接的配置项。key 的类型为 STRING，支持以下配置：

* LDAP\_OPT\_PROTOCOL\_VERSION：value 为整型标量，用于指定 LDAP 传输协议版本。可选 1、2、3，默认为 3。
* LDAP\_OPT\_REFERRALS：value 为 STRING 类型标量，用于指定是否自动遵循 LDAP 服务器返回的引用。可选值为 LDAP\_OPT\_ON， LDAP\_OPT\_OFF，默认为 LDAP\_OPT\_OFF。

**searchScope** STRING 类型标量，查询的搜索范围，默认为 `LDAP_SCOPE_SUBTREE` 。可以取值为：

* `LDAP_SCOPE_BASE`：搜索指定 DN 的对象本身，不搜索子对象。
* `LDAP_SCOPE_ONELEVEL`：搜索指定 DN 下的一级子对象，不包括子对象的子对象。
* `LDAP_SCOPE_SUBTREE`：搜索指定 DN 下的所有子孙对象，包括子对象的子对象。
* `LDAP_SCOPE_SUBORDINATE`：搜索指定 DN 下的直接子对象，不包括指定 DN 自身和指定 DN 的孙子对象。

**saslMechanism** STRING 类型标量，绑定 LDAP 服务器时所使用的 Simple Authentication and Security Layer (SASL) 加密方式，默认为 `NULL` 。目前只支持取值为 `NULL`。

**示例**

下例是在 `ldap://localhost` ldap 服务器地址中，通过 `cn=admin,dc=sample,dc=com` 账号登录，基于 `dc=sample,dc=com` 查询符合 `(cn=admin)` 过滤的条目。

```
ret = LDAP::search("ldap://localhost","cn=admin,dc=sample,dc=com", "password", "dc=sample,dc=com", "(cn=admin)")
```

## 配置说明

### 1. 上传插件并配置启动加载

上传附件插件压缩包到所有节点所在服务器，解压到 *<DolphinDB 安装目录>/plugins*。

在 Web 管理界面的 Controller Config 和 Nodes Config 中配置 *preloadModules* 值为 `plugins::LDAP`。如果之前已经配置过 *preloadModules*，则需要用逗号隔开之前的值。

### 2. 重启集群，定义登录函数视图

要求入参为：

**username** STRING 类型，登录输入的用户名。

**password** STRING 类型，登录输入的密码。

返回值为：

ANY VECTOR 类型，第一个元素为 DolphinDB 账户用户名，第二个为 DolphinDB 账户密码。

需要使用 `LDAP::search` 方法连接 LDAP Server 获取 DolphinDB 账户用户名和密码，以实现登录逻辑。

```
// 加载 LDAP 插件
try { loadPlugin("plugins/LDAP/PluginLDAP.txt") } catch(err) { print(err) }
go

// 定义一个与 login 函数前两个入参相同的函数
def ldap_login(username, password) {

    // 排除超级管理员账户
    if (username == "admin") {
        return [username, password]$ANY
    }

    // 根据入参查询 entry
    ret = LDAP::search("ldap://192.168.100.43","cn=ldapadm,dc=sample,dc=com", password, "dc=sample,dc=com", "(cn=" + username + ")")

    // 找同名的 entry
    dn = "cn=" + username + ",dc=sample,dc=com"

    // 注意返回的一定要是 ANY 类型的 vector
    // 这里是给账户的 facsimileTelephoneNumber 属性设置为 admin
    // telephoneNumber 属性设置为 123456, 进行模拟
    return [ret[dn]["facsimileTelephoneNumber"], ret[dn]["telephoneNumber"]]$ANY
}

// 加入函数视图
addFunctionView(ldap_login)
```

注意事项：

1. 该视图须配置为仅 admin 管理员账户可见。
2. 需要在视图内判断排除不需要通过 LDAP 鉴权的用户（例如超级管理员 admin），直接返回输入的用户名和密码，或者返回空也可以。
3. `LDAP::search` 方法的 *dn* 参数应该基于 *username* 入参进行拼接。
4. `LDAP::search` 方法的 *password* 参数应该基于 *password* 入参进行拼接。
5. `LDAP::search` 方法的 *filter* 参数应该在 *searchBase* 下通过 *username* 入参拼接筛选出集群的特定用户。
6. 实际使用的是 LDAP 中存储的用户的密码，DolphinDB 中存储的密码对于集群用户无实际意义，所以 DolphinDB 密码用 LDAP 返回的信息中任何一个对于该用户固定的值做密码即可。
7. 如果需要在登录时创建不存在的用户，则可以先在视图内登录超级用户 admin（内部机制见事项 2），然后新建用户，最后使用新建的用户登录。

### 3. 关闭集群，修改所有控制节点的 *controller.cfg* 配置 *thirdPartyAuthenticator* 值为函数视图 ldap\_login

*thirdPartyAuthenticator* 配置项参考：功能配置—登录。

```
preloadModules=plugins::LDAP
thirdPartyAuthenticator=ldap_login
```

### 4. 重启集群，使用 LDAP 账户登录节点

```
login("ldapadm", "DolphinDB123@3");
```
