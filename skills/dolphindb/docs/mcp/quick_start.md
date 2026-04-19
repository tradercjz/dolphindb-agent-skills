<!-- Auto-mirrored from upstream `documentation-main/mcp/quick_start.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 快速开始

本章节介绍如何快速接入 Stock MCP 服务，包括如何申请访问凭证（API Key）、配置鉴权信息、接入 MCP 平台以及使用不同权限组调用工具。

## MCP API Key（Token）

**免费申请 Token**

API Key 是访问 MCP 服务的凭证，必须先申请才能使用 MCP 工具。当前面向机构用户免费发放 Token 试用，获取方法：

* 联系 DolphinDB 团队申请 MCP Token。

**配置鉴权信息**

在客户端或系统接入 MCP 时，需要在 HTTP 请求 Header 中添加鉴权信息：

```
Authorization: Bearer {YOUR_MCP_TOKEN}
```

注：

请将 `{YOUR_MCP_TOKEN}` 替换为实际获取的 Token。Token
是访问凭证，请妥善保存，不要在前端或公开环境中暴露。

**Stock MCP Server 地址**

在各个 MCP Client 上，需要填写连接 MCP Server 的地址，当前的地址为：

```
mcpstockstrategy.dolphindb.com:8654/mcp
```

## MCP 平台接入

支持多种接入方式，无论是在客户端、系统工具还是你熟悉的投研平台，都可以快速配置 API Key 并调用 MCP 服务，立即开始使用 Stock MCP
的数据和分析能力。

## VScode Github Copilot 接入指引

打开 Copilot 聊天框，点击右下角 “**工具**”图示。

![](images/stock_mcp/quick_start01.png)

点击右上方 “**Add MCP Server**”，选择 “**HTTP**”模式。

![](images/stock_mcp/quick_start02.png)

输入 MCP Server 地址：`"http://ip:port/mcp"`。注意：需要将 ip 和 port
替换为实际使用的服务器地址和端口。

![](images/stock_mcp/quick_start03.png)

输入自定义 MCP Server 名称，如 “DDB MCP Server”。

![](images/stock_mcp/quick_start04.png)

在 mcp.json 文件中增加 “**headers**”字段，并保存文件。

```
{
                  "servers": {
                      "DDB MCP
              Server": {             "url":
              "http://ip:port/mcp",             "type":
              "http",
              "headers": {
              "Authorization": "Bearer token"             }
                      }     },     "inputs": []
              }
```

注意：

* 请将文件中的 ip、port 和 token 替换为实际使用的服务器地址、端口和 MCP Token。
* MCP Token 是由服务端颁发的访问凭证，具有效期。若 Token 失效，需要联系 DolphinDB 团队获取 Token，方可继续访问 MCP
  服务。

![](images/stock_mcp/quick_start05.png)

保存 mcp.json 后，打开 Copilot 聊天框右下角的工具图示，选 Agent模式。

如果成功连接，可以看到刚才添加的 MCP Server。勾选所需工具，即可开始使用 MCP 功能。

![](images/stock_mcp/quick_start06.png)

## Cherry Studio 接入指引

Cherry Studio下载地址：[Cherry Studio - 全能的 AI 助手](https://cherry-ai.com/)

下载并安装 Cherry Studio 后，点击界面右上角的 “**设置**”按钮进行配置。

![](images/stock_mcp/quick_start07.png)

进入设置界面后在左边侧栏选择 “**MCP**”，点击右上角的 “**添加**”，选择 “**快速创建**”，进入 MCP 添加界面。

![](images/stock_mcp/quick_start08.png)

在配置界面填入 MCP 服务器信息，类型选择可流式传输的 HTTP（streamableHttp），在 URL 中填入
`http://ip:port/mcp`，在请求头中填入 `Authorization=Bearer
YOUR_TOKEN_HERE`，并将 YOUR\_TOKEN\_HERE 替换为申请到的 MCP Token。

![](images/stock_mcp/quick_start09.png)

填写完成后，点击右上角的 “**保存**”，弹出 “服务器更新成功！” 提示即表示配置完成。

![](images/stock_mcp/quick_start10.png)

返回 MCP 设置界面，即可看到添加的 MCP 服务器，并启动该服务。

![](images/stock_mcp/quick_start11.png)

点击 MCP 服务进入详细界面，可查看和管理 MCP 工具。

![](images/stock_mcp/quick_start12.png)

配置服务器完成后，在 “**话题**” 界面下新建话题，在上方选择模型，在下方侧栏中选择 DolphinDB 的 MCP 服务，即可开始使用 MCP 功能。

![](images/stock_mcp/quick_start13.png)

##

操作步骤：

1. 下载 Cursor: [Cursor](https://www.cursor.com/cn)

   注意：仅 **Pro trial** 或 **Pro** 版本的 Cursor 账户支持接入 MCP
   Server，普通账户无法完成以下操作。
2. 打开 Cursor 平台，点击右上角设置按键，点击左侧边栏 **“Tools & MCP”**，点击 **“New MCP
   Server”**，添加新的 MCP Server。
   ![](images/stock_mcp/quick_start14.png)
   ![](images/stock_mcp/quick_start15.png)
3. 根据 MCP Server 的 URL 和 Token，在 JSON 文件中填写相应信息并保存。**DolphinDB MCP Server 的 URL
   示例为：**`http://ip:port/mcp`

   ![](images/stock_mcp/quick_start16.png)
   确认 MCP Server 已启用，并在界面上显示绿灯，表示可正常使用。
   ![](images/stock_mcp/quick_start17.png)
4. 点击右上角 **“AI Pane”** 按键，打开对话框。Agent 模式选择 **“Agent”**（只有该模式才能调用 MCP
   工具），选择所需模型，如 deepseek-v3.1。

   注意：不能选择推理模型，否则无法调用 MCP 工具。

   ![](images/stock_mcp/quick_start18.png)

配置完成后，即可使用 DolphinDB MCP Server 提供的工具和实时数据。

## Trae 接入指引

操作步骤：

1. 下载 Trae：[TRAE -
   The Real AI Engineer | TRAE - The Real AI Engineer](https://www.trae.cn/)
2. 登录 Trae 后，打开 AI 侧栏，点击右上角的 “**AI功能管理**”。
   ![](images/stock_mcp/quick_start19.png)
3. 选择 “**MCP**”，点击右上角 “**添加**”，选择 “**手动添加**”。

   ![](images/stock_mcp/quick_start20.png)
4. 在打开的手动配置界面输入以下内容：

   ```
   {
                   "mcpServers": {
                     "DolphinDB数据库助手": {
                       "type": "http",
                       "url":
                 "http://ip:port/mcp",       "headers": {
                         "Authorization":
                 "Bearer YOUR_TOKEN_HERE"       }     }   } }
   ```

   **配置说明**：

   * 将 `ip:port` 替换为 DolphinDB 服务器的实际地址，必须以 /mcp 结尾。
   * 将 `YOUR_TOKEN_HERE` 替换为获取的访问令牌 Token。
   ![](images/stock_mcp/quick_start21.png)
5. 点击确认后，即可看到已添加的 MCP 服务。服务默认已启动，如未启动，可手动启动。

   ![](images/stock_mcp/quick_start22.png)

完成后点击返回对话界面，点击下方的 “**@**” 选择智能体，选择 Builder with MCP，即可开始使用 MCP 服务。

![](images/stock_mcp/quick_start23.png)

## 腾讯 CodeBuddy 接入指引

操作步骤：

1. 下载 CodeBuddy：[腾讯云代码助手 CodeBuddy - AI 时代的智能编程伙伴](https://copilot.tencent.com/ide/)
2. 登录 CodeBuddy 后，打开 AI 侧栏，点击右上角的 “**CodeBuddy 设置**”。
   ![](images/stock_mcp/quick_start24.png)
3. 选择 “**MCP**”，点击右上角 “**添加MCP**”，进入配置界面。在左侧打开的手动配置界面输入以下内容：

   ```
   {
                   "mcpServers": {
                     "DolphinDB数据库助手": {
                       "type": "http",
                       "url":
                 "http://ip:port/mcp",       "headers": {
                         "Authorization":
                 "Bearer YOUR_TOKEN_HERE"       }     }   } }
   ```

   **配置说明**：

   * 将 `ip:port` 替换为 DolphinDB 服务器的实际地址，必须以 /mcp 结尾。
   * 将 `YOUR_TOKEN_HERE` 替换为获取的访问令牌 Token。
   ![](images/stock_mcp/quick_start25.png)
4. 按下 **Ctrl+S** 保存后，即可看到 MCP 服务默认已开启；如果未自动开启，需要手动打开。点击展开可以查看 MCP
   服务提供的函数工具。

   ![](images/stock_mcp/quick_start26.png)
5. 关闭设置界面，打开新的对话，即可直接使用 MCP 服务进行对话。

   ![](images/stock_mcp/quick_start27.png)

## Dify 接入指引

点开工具页面，点击 MCP——添加 MCP 服务（HTTP）。将会显示如下界面，分别填入 URL 和请求头。

![](images/stock_mcp/quick_start28.png)

进入工作室，填写 system prompt，选择 MCP Server 连接，然后选择 LLM 进行调试。

![](images/stock_mcp/quick_start29.png)
