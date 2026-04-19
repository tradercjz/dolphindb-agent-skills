<!-- Auto-mirrored from upstream `documentation-main/mcp/mcp_use_guide.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# MCP 使用指南

## 部署 MCP Server

1. 下载 [DolphinDB](https://dolphindb.cn/product#downloads-top) 最新版本 3.00.4。
2. 登录并验证 MCP Server
   生效。

   ```
   login(`user,password)
   // 获取当前账号的 MCP Server的 ticket
   getAuthenticatedUserTicket()
   // 查看当前服务器发布的 MCP 工具
   listMCPTools()
   ```

### 集群部署

DolphinDB MCP Server 支持集群部署。工具在调用时，会在对应的数据节点和计算节点执行，返回结果给客户端。假如集群包含 ip:port1
控制节点， ip:port2 计算节点 和 ip:port3 数据节点，用户可以在任意节点定义工具，调用时，工具会在调用的节点执行。例如：调用
ip:port2/mcp，工具将在 ip:port2 执行。

### 权限控制

MCP Server 支持基于角色的权限管理，兼容 DolphinDB 现有的用户/用户组体系。权限采用 **显式授权（grant）+
拒绝优先（deny）** 机制，确保灵活管控。

**支持的权限类型**

| 权限标识 | 作用范围 | 权限说明 |
| --- | --- | --- |
| MCP\_MANAGE | 全局 | MCP 资源管理员：可 **发布/停止发布** tools，resources 与 prompts，适用于运维角色。 |
| MCP\_DEVELOP | 全局 | MCP 工具开发者：可 **新增/修改/删除/查看** tools，resources 与 prompts，适用于开发者。 |
| MCP\_EXEC | 资源级 | MCP 执行者：可调用 `tools/*`、`prompts/*`、`resources/*` 等接口，适用于 AI 模型或前端客户端。 |

**授权命令**

通过 `grant` 命令进行授权，通过 `deny` 命令取消授权。示例如下：

```
// 赋予用户 userA 发布工具的权限
grant(`userA, MCP_MANAGE)
// 赋予用户 userA 工具开发权限
grant(`userA, MCP_DEVELOP)
// 允许 userA 执行名为 fun1 的工具
grant(`userA, MCP_EXEC, "tools/fun1")
// 允许 userA 执行所有 tools（包含 future tools/*）
grant(`userA, MCP_EXEC, "tools/*")
// 同时授权所有 + 显式禁止某个工具（deny 优先生效）
grant(`userA, MCP_EXEC, "tools/*")
deny(`userA, MCP_EXEC, "tools/fun1")
```

Agent 在实际执行工具时会进行两层权限检查：

1. 检查 userA 是否具有 MCP 工具的执行权限，如果不具有权限，则无法执行工具；
2. userA 执行工具函数时，如果涉及用户本身权限不允许的操作（如删除库表），则无法执行。

## 查看现有工具集

注：

在加载工具之前，请确保：

* 已完成第一部分的环境搭建和基础配置。
* 至少已成功注册一个工具集。

```
// 查看已注册的工具
print("已注册工具：")
print(listMCPTools())
```

![](images/use_guide/fig_1-1.png)

## 开发自定义工具

参考MCP 工具开发指南。

## 在客户端配置 MCP 服务器、工具集和 System Prompt

### 在 VS Code Copilot 配置 MCP

#### 创建 MCP 配置

1. 打开 Copilot 聊天框，点击右下角 “**工具**”图示。

   ![](images/use_guide/fig_1-2.png)
2. 点击右上方 “**Add MCP Server**”，选择 “**HTTP**”模式。

   ![](images/use_guide/fig_1-3.png)
3. 输入 MCP Server 地址：`"http://ip:port/mcp"`。注意：需要将 IP 和
   port 替换为实际使用的服务器地址和端口。如使用 HTTPS 协议，需在配置文件（单节点的 dolphindb.cfg 或集群的
   cluster.cfg ）中，指定配置项 `enableHTTPS=true`。

   ![](images/use_guide/fig_1-4.png)
4. 输入自定义 MCP Server 名称，如 “DDB MCP Server”。

   ![](images/use_guide/fig_1-5.png)
5. 在 mcp.json 文件中增加 “**headers**”字段，并保存文件。

   ```
   {
     "servers": {
       "DDB Agent": {
         "type": "http",
         "url": "http://ip:port/mcp",
         "headers": {
           "Authorization": "Bearer token"
         }
       }
     }
   }
   ```

保存配置文件后，客户端会自动检测到配置已更新，并在界面上方显示 “**Start**” 按钮。点击 “**Start**”
后，客户端将根据配置内容自动连接 MCP Server 并加载服务器已发布的 MCP 工具集，使配置正式生效。

**注意：**

* 请将文件中的 ip、port 和 token 替换为实际使用的服务器地址、端口和 MCP Token。
* MCP Token 是由服务端颁发的访问凭证，具有效期。若 Token 失效，需要在服务端登录并调用
  `getAuthenticatedUserTicket()` 获取新的 Token，方可继续访问 MCP
  服务。

#### 启动 VS Code Github Copilot，添加 MCP 工具

* 打开 VS Code，点击 Copilot 的聊天界面，选 Agent 模式，点击右下角工具按钮；
* 如果连接成功，可以看到刚才添加的 MCP Server。
* 在 MCP Server 下方会显示服务器发布的工具列表，例如下图的 7 个工具。勾选这些工具，使 Copilot
  能在对话中调用它们。

![](images/use_guide/fig_1-6.png)

完成以上步骤后，就可以开始在 Copilot 对话中使用 MCP 功能了。大模型会根据上下文自动调用这些工具执行任务。

### 在 Cherry studio 配置 MCP

**使用前提：**要在 Cherry Studio 配置 MCP，需要先获得 API Key。

#### 创建 MCP 配置

1. 打开 Cherry Studio，点击界面右上角的 “**设置”** 按钮进行配置。

   ![](images/use_guide/fig_1-7.png)
2. 进入设置界面后在左边侧栏选择 “**MCP**”，点击右上角的 “**添加**”，选择 “**快速创建**”，进入
   MCP 添加界面。

   ![](images/use_guide/fig_1-8.png)
3. 在配置界面填入 MCP 服务器信息，类型选择可流式传输的 HTTP（streamableHttp），在 URL 中填入
   `http://your-server-ip:port/mcp`，在请求头中填入
   Authorization=Bearer YOUR\_TOKEN\_HERE，并将 YOUR\_TOKEN\_HERE 替换为申请到的 MCP
   Token。

   ![](images/use_guide/fig_1-9.png)
4. 填写完成后，点击右上角的 “**保存**”，弹出 “服务器更新成功！” 提示即表示配置完成。

   ![](images/use_guide/fig_1-10.png)
5. 返回 MCP 设置界面，即可看到添加的 MCP 服务器，并启动该服务。

   ![](images/use_guide/fig_1-11.png)
6. 点击 MCP 服务进入详细界面，可查看和管理 MCP 工具。

   ![](images/use_guide/fig_1-12.png)
7. 配置服务器完成后，在 “**话题**” 界面下新建话题，在上方选择模型，在下方侧栏中选择 DolphinDB 的 MCP
   服务，即可开始使用 MCP 功能。

   ![](images/use_guide/fig_1-13.png)

#### 模型配置

在所使用的模型服务中，填写对应模型的 API Key，以确保客户端能够正常访问模型。

同时请在 **常规设置** 中关闭代理（Proxy），避免因代理干扰导致 MCP Server 无法连接。

![](images/use_guide/fig_1-14.png)

### 其他客户端配置 MCP

除以上两种客户端外，Claude Desktop Pro 等符合 MCP 协议的客户端也都可以连接 MCP Server。

不同客户端的具体配置方式，可参考MCP
平台接入。

## 工具使用和测试

### 使用示例

完成配置并勾选所需的 MCP 工具后，在 VS Code Copilot 的聊天框中选择 **Agent 模式**，输入自然语言问题，即可触发 MCP
工具调用。

AI 会根据你的提问自动选择并调用适合的工具，也可能在一次对话中连续调用多个工具以完成任务。

![](images/use_guide/fig_1-15.png)

### 单工具测试

若某个工具的描述中明确说明了典型使用场景（如 `monitor_memory_usage`
用于监控内存使用情况），即可在客户端直接输入相关的自然语言语句进行单工具测试，例如："内存使用率高吗？需要优化吗？"

**Agent 预期行为**：

1. 调用 `monitor_memory_usage` 获取内存数据。
2. 分析工具返回的数据，并给出优化建议。

### 联合工具测试

当工具数量较多、功能协同复杂时，建议为特定 Agent 配置相应的 **System Prompt**，以指导其如何调度多个工具完成任务。

例如，在“选股 Agent”中查询某个衍生因子并进行单因子评价时，Agent 会触发多步工具调用：

* 先调用查询因子的工具
* 再调用因子评价工具
* 可能还会涉及数据存储或临时表管理

每次 Agent 调用工具时，计算在 DolphinDB MCP 服务端完成。客户端只负责保存输入参数和计算结果的上下文，无需参与实际计算。

![](images/use_guide/fig_1-16.png)
![](images/use_guide/fig_1-17.png)
![](images/use_guide/fig_1-18.png)

### 使用 Inspector 调试工具

在完成工具开发后，可以通过两种方式进行验证：

* 在客户端直接使用自然语言进行测试
* 使用 MCP 官方调试工具 Inspector 对单个工具进行精确调试

以下介绍如何使用 MCP Inspector 进行工具级调试。关于 Inspector 的更多介绍，参考[MCP Inspector - Model Context
Protocol](https://modelcontextprotocol.io/legacy/tools/inspector#inspector)。

#### 安装与启动 Inspector

Inspector 是 MCP 官方提供的可视化调试工具，无需单独安装，使用 Node.js 的 npx 即可运行。

1. 前往 [Node.js 官网](https://nodejs.org/zh-cn) 下载 Node.js。
2. 安装完成后，在 PowerShell
   执行：

   ```
   npx @modelcontextprotocol/inspector
   ```

   运行后会自动打开浏览器进入
   Inspector 页面。

#### 配置 Inspector

进入 Inspector 后，需要完成以下配置。

1. 将 Session token 复制到页面中的 Proxy Session Token。

   ![](images/use_guide/fig_1-19.png)![](images/use_guide/fig_1-20.png)
2. 在 DolphinDB 服务端运行 `getAuthenticatedUserTicket()`，将返回的
   Ticket 填入Bearer Token。注意：MCP 工具权限是基于用户的 Ticket 进行检查的。建议使用 admin 用户获取
   Ticket。
3. URL 填写当前 MCP Server 的地址：ip:port/mcp。
4. Transport Type 选择 SSE/Streamable。

   ![](images/use_guide/fig_1-21.png)

#### 连接和调试 Tools

1. 点击 Connect 连接 MCP Server。
2. 点击 List Tools 显示服务器发布的所有 MCP 工具。
3. 选择某个工具，可在右侧填入参数进行测试。

   输入格式说明：STRING 类型无需加引号，对于 STRING[] 类型，可以点击 “**Switch to JSON**” 以标准
   JSON 格式输入。
4. 点击执行即可在右侧查看工具输出，验证是否符合预期。

   ![](images/use_guide/fig_1-22.png)
