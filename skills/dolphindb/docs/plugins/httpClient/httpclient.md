<!-- Auto-mirrored from upstream `documentation-main/plugins/httpClient/httpclient.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# HttpClient

通过 DolphinDB 的 httpClient 插件，用户可以发送 HTTP 请求以及发送邮件。该插件使用第三方库 CURL 来进行 HTTP 相关的操作。

本插件使用 SMTP 邮件传输协议，所以邮件服务器必须支持 SMTP 协议和开启 SMTP 端口，如果邮件服务商默认没有开启 SMTP 端口，则需要开启该账号的 SMTP 服务。

## 安装插件

### 版本要求

支持 DolphinDB Server 2.00.10 及更高版本。

支持 Shark；支持 Linux x64，Linux ARM ，Linux ABI，Windows x64。

### 安装步骤

1. 在 DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   注意：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可[自行编译](https://gitee.com/dolphindb/DolphinDBPlugin)（请自行选择对应分支下的插件）或在 [DolphinDB 用户社区](https://ask.dolphindb.cn/)进行反馈。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   ```
   installPlugin("httpClient")
   ```
3. 使用 `loadPlugin` 命令加载插件。

   ```
   loadPlugin("httpClient")
   ```

## 接口说明

### httpGet

发送HTTP GET请求。

**语法**

```
httpClient::httpGet(url, [params], [timeout], [headers], [config])
```

**详情**

发送 HTTP GET 请求。返回一个字典，包括以下键：

* responseCode：请求返回的响应码。
* headers：请求返回的头部。
* text：请求返回的内容文本。
* elapsed：请求经过的时间。

**参数**

**url** 请求的URL字符串。

**params** STRING 类型标量，或键和值都是 STRING 类型的字典，表示 http 请求的参数。指定后，*params* 将会放在 url 的后面。

假如url为 www.dolphindb.cn，

* 如果 params 为一个字符串（例如，"example"），则发出的完整 http 报文的请求头中的 url 为 "http://www.dolphindb.cn?example "。
* 如果 params 为一个字典（例如，两个键值对 "name"->"jack" 和"id"->"111"），则发出的完整http报文的请求头中的url为 "http://www.dolphindb.cn?id=111&name=jack "。

**timeout** 整型标量，表示超时时间，单位为毫秒。

**headers** STRING 类型标量，或键和值都是 STRING 类型的字典，表示 http 请求的头部。

* 如果 headers 为一个字典（例如 "groupName"->"dolphindb" 和 "groupId"->"11"），则发出的完整 http 报文添加请求头是 "groupId: 11" 和 "groupName: dolphindb"。
* 如果 headers 为一个字符串，则必须是 "xx: xx" 格式，会直接把该字符串添加到请求头中。

**config** 一个 key 类型为 STRING 的字典，表示一些配置项。

| **配置项(key)** | **值类型** | **说明** |
| --- | --- | --- |
| proxy | STRING | 可选参数，设置代理地址 |

**例子**

```
loadPlugin('/home/zmx/worker/DolphinDBPlugin/httpClient/PluginHttpClient.txt');
param=dict(string,string);
header=dict(string,string);
param['name']='zmx';
param['id']='111';
header['groupName']='dolphindb';
header['groupId']='11';
//Please set up your own httpServer ex.(python -m SimpleHTTPServer 8900)
url = "localhost:8900";
res = httpClient::httpGet(url,param,1000,header);
```

### httpPost

发送 HTTP POST 请求。返回值同 `httpGet` 的返回值。

**语法**

```
httpClient::httpPost(url, [params], [timeout], [headers], [config])
```

**参数**

`httpPost` 大部分参数和 `httpGet` 参数相同，这里仅说明不同的参数。

**params** STRING 类型标量，或键和值都是 STRING 类型的字典，表示 http 请求的参数。指定后，*params* 将会出现在HTTP报文主体(body)部分。

**例子**

```
loadPlugin('/home/zmx/worker/DolphinDBPlugin/httpClient/PluginHttpClient.txt');
param=dict(string,string);
header=dict(string,string);
param['name']='zmx';
param['id']='111';
header['groupName']='dolphindb';
header['groupId']='11';
//Please set up your own httpServer ex.(python -m SimpleHTTPServer 8900)
url = "localhost:8900";
res = httpClient::httpPost(url,toStdJson(param),1000,header);
```

### httpPut

**语法**

```
httpClient::httpPut(url, [params], [timeout], [headers], [config])
```

**详情**

发送 HTTP PUT 请求。返回值同 `httpGet` 的返回值。

**参数**

同 `httpGet` 的参数。

### httpDelete

**语法**

```
httpClient::httpDelete(url, [params], [timeout], [headers], [config])
```

**详情**

发送 HTTP DELETE 请求。返回值同 `httpGet` 的返回值。

**参数**

同 `httpGet` 的参数。

### emailSmtpConfig

**语法**

```
httpClient::emailSmtpConfig(domain,host,[port=25])
```

**详情**

配置邮件服务器。

**参数**

**domain** STRING 类型标量，表示邮箱名称，格式为邮箱'@'字符后的字符串。如果是 qq 邮箱，则是 "qq.com "。如果是 yeah 邮箱，则是 "yeah.net "。

**host** STRING 类型标量，表示邮箱 SMTP 服务器的地址。

**port** INT 类型标量，表示邮箱服务器端口，默认为25。

**例子**

```
emailName="qq.com";
host="smtp.qq.com";
port=25;
httpClient::emailSmtpConfig(emailName,host,port);
```

### sendEmail

**语法**

```
httpClient::sendEmail(userId, pwd, recipient, [subject], [body], [msg])
```

**详情**

发送邮件。返回一个字典，包括以下键：

* userId：STRING 类型标量，发送者邮箱账号。
* recipient：STRING 类型向量，接收者邮箱的集合的字符串。
* responseCode：INT 类型标量，请求返回的响应码。
* headers：STRING 类型标量，请求返回的头部。
* text：STRING 类型标量，请求返回的内容文本。
* elapsed：STRING 类型标量，请求经过的时间。

请注意，可通过两种方式生成 SMTP 的消息内容，任选其一即可：

* 同时填写 subject 和 body 参数，插件将根据这两个参数的内容按照 SMTP 标准拼接成完整的 SMTP 消息。
* 只填写 msg 参数。

**参数**

**userId** STRING 类型标量，表示发送者邮箱账号。

**pwd** STRING 类型标量，表示发送者邮箱密码。某些邮件服务商提供邮箱授权码的功能，在这种情况下，参数 *pwd* 为邮箱授权码而非邮箱密码。

**recipient** STRING 类型标量或向量，表示目标邮箱账号的一个字符串或一个字符串集合。

**subject** STRING 类型标量，表示邮件主题。

**body** STRING 类型标量，表示邮件正文。

**msg** STRING 类型标量，表示 SMTP 的消息内容。消息内容必须由如下 5 个字段和邮件正文构成，否则发送邮件会失败：

* MIME-Version：SMTP 正文格式的版本。
* Content-Type, Charset：表示文件内容格式，表示文本编码方式。
* To：接收者邮箱。
* From：发送者邮箱。
* Subject：邮件主题。

每个字段之间必须使用 ”\r\n“ 分隔，且在这 5 个字段后必须加上 “\r\n\r\n”。

可参考例子中通过 createSMTPMsg 函数来构造 SMTP 的消息内容。

注意：发送者邮箱 *userId*、接收者邮箱 *recipient*，必须和邮件正文中的 "From:"、"To: " 字段保持一致，否则会导致邮件发送失败。具体来说，示例中的 `createSMTPMsg` 函数和 `httpClient::sendSMTPEmail` 函数的 *userId*、*recipients* 参数必须保持一致。

**例子**

例1. 发送一个邮件到一个邮箱里。

```
res=httpClient::sendEmail('MailFrom@xxx.com','xxxxx','Maildestination@xxx.com','This is a subject','It is a text');
```

例2. 发送一个邮件到多个邮箱里。

```
recipient='Maildestination@xxx.com''Maildestination2@xxx.com''Maildestination3@xxx.com';
res=httpClient::sendEmail('MailFrom@xxx.com','xxxxx',recipient,'This is a subject','It is a text');
```

例3. 发送自定义的 SMTP 正文的邮件到指定邮箱中。

```
// 构造 SMTP 格式的邮件正文
def createSMTPMsg(userId, recipient, subject, content){
	MimeVersion = "MIME-Version: 1.0"
    ContentType = "Content-Type: text/html; Charset=\"UTF-8\""
    Recipients = "To: " + concat(recipient, ",")
    Sender = "From: " + userId
    Subject = "Subject: " + subject
    msg = [MimeVersion, ContentType, Recipients, Sender, Subject]
    msg = concat(msg, "\r\n")
	msg += "\r\n\r\n"
	msg += content
	return msg
}
userId = "httpClient1@dolphindb.com"
pwd = "password"
recipient = ["httpClient2@dolphindb.com", "httpClient3@dolphindb.com"]
subject = "Test"
content = "This is a test."
smtpMsg = createSMTPMsg(userId, recipient, subject, content)
// 发送邮件
httpClient::sendEmail(userId, pwd, recipient, , , smtpMsg)
```
