<!-- Auto-mirrored from upstream `documentation-main/plugins/tcpsocket.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# TCPSocket

通过 DolphinDB 的 TCPSocket 插件，用户可以通过 TCP 连接到指定的 IP 和端口，然后遵循自定义格式的传输报文进行数据的接收和发送。

## 安装插件

### 版本要求

DolphinDB Server 2.00.10 及更高版本，支持 Linux x64, Linux ARM, Linux JIT。

### 安装步骤

1. 在 DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   注意：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可[自行编译](https://gitee.com/dolphindb/DolphinDBPlugin)（请选择对应分支下的插件）或在 [DolphinDB 用户社区](https://ask.dolphindb.cn/)进行反馈。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   ```
   installPlugin("TCPSocket")
   ```
3. 使用 `loadPlugin` 命令加载插件。

   ```
   loadPlugin("TCPSocket")
   ```

## 接口说明

### createSubJob

**语法**

```
TCPSocket::createSubJob(host, port, handler, [config])
```

**详情**

创建一个 TCP 连接，连接指定的 host 和 port，并创建一个后台任务，接收 TCP 的数据。返回一个 STRING 的标量，可用于后续 `TCPSocket::cancelSubJob` 使用。

注意： `TCPSocket::createSubJob` 创建的 job 不会随着 session 关闭自动退出，必须手动调用 `TCPSocket::cancelSubJob` 结束。

**参数**

**host** STRING 类型标量，表示需要连接的服务端的 IP 地址。

**port** INT 类型的标量，表示需要连接的服务端的端口。

**handler** 一个一元函数对象，用于解析从 TCP 的连接里接收到的数据。handler 需要的函数签名为：

```
def handler(data){
}
```

其中输入的 data 是一个表，包含如下列：

* bytes：列类型为 BLOB，接收到的 TCP 数据。最大长度为 10240 字节。
* isHead：列类型为 BOOL，表示该行所接的 TCP 数据是否和上一行是连续的，每次 TCP 连接后，第一行数据的 *isHead* 为 true。

**config** 一个字典，类型为 (STRING, ANY)，用于配置特定的参数。目前仅支持 “maxRows\*”\*。

* maxRows：INT 类型的标量，表示每次执行 parser 时的最多的数据行数。默认为 128；最小值为1。

### getSubJobStat

**语法**

```
TCPSocket::getSubJobStat()
```

**详情**

获取所有的 TCP 后台任务信息，包含已经通过 `TCPSocket::cancelSubJob` 取消的任务。

返回一个表，包含如下列：

* tag：列类型为 STRING，表示 TCP 的订阅任务标识。
* startTime：列类型为 NANOTIMESTAMP，表示任务创建时间。
* endTime：列类型为 NANOTIMESTAMP，表示任务取消时间。
* firstMsgTime：列类型为 NANOTIMESTAMP，表示第一条数据的接收时间。
* lastMsgTime：列类型为 NANOTIMESTAMP， 表示上一条消息的接收时间。
* processedMsgCount：列类型为 LONG，表示成功处理的消息行数。
* failedMsgCount：列类型为 LONG ，表示处理失败的消息行数。
* lastErrMsg：列类型为 STRING，表示上一次处理失败（TCP 连接失败、TCP 连接断开、读取 TCP 数据失败等情况）的错误信息。
* lastFailedTimestamp：列类型为 NANOTIMESTAMP ，表示上一次处理失败（同上）的时间。

### cancelSubJob

**语法**

```
TCPSocket::cancelSubJob(tag)
```

**详情**

取消一个 TCP 的后台任务。

**参数**

**tag** 类型为 STRING 标量，表示TCP 任务标识。可以通过 `TCPSocket::getSubJobStat ()` 查询获得或者 `TCPSocket::createSubJob` 函数返回获得。

### connect

**语法**

```
TCPSocket::connect(host, port)
```

**详情**

创建一个阻塞模式的 TCP 连接。`TCPSocket::connect` 创建的连接。返回一个 TCP 的 socket 资源，可用于后续在 `TCPSocket::read` 和 `TCPSocket::close` 中使用。

注意：在当前 session 关闭时，插件会自动调用 `TCPSocket::close` 以关闭连接。

**参数**

**host** STRING 类型的标量，表示连接 TCP socket 服务端的 IP 地址。

**port** INT 类型的标量，表示连接 TCP socket 服务端的端口。

### read

**语法**

```
TCPSocket::read(socket, [maxBytes])
```

**详情**

读取 TCP 的 socket 里的数据。返回一个 BLOB 类型的标量。

**参数**

**socket** 通过 `TCPSocket::connect` 创建的 socket 连接。

**maxBytes** 类型为 INT 的标量，表示读取的最大字节数。默认是 10240 字节数；必须大于0。

### write

**语法**

```
TCPSocket::write(socket, data)
```

**详情**

向 TCP 的 socket 写数据。如果写入成功，会返回 true。如果写入失败，会抛出异常。

**参数**

**socket** 通过 `TCPSocket::connect` 创建的 socket 连接。

**data** BLOB 或 STRING 类型的标量，需要往 socket 写的数据。

### close

**语法**

```
TCPSocket::close(socket)
```

**详情**

关闭一个 TCP 的 socket 连接。返回 true。

**参数**

**socket** 通过 `TCPSocket::connect` 创建的 socket 连接。

## 使用示例

```
def handler(mutable table1, data){
	table1.append!(data)
}
share table(1:0, `bytes`isHead, [BLOB, BOOL]) as t
config = dict(STRING, ANY)
config[`maxRows] = 8192

TCPSocket::createSubJob("192.168.1.38", 20002, handler{t}, config)
```

## 附录

### IO\_ERROR 错误码以及出错原因

如果在执行插件接口后返回或者在 log 里有如下异常信息：[PLUGIN::TCPSocket]: failed to XXX with IO error type $。建议查看下表以排查具体原因。

| IO\_ERROR 值 | 原因 |
| --- | --- |
| 1 | Socket is disconnected/closed or file is closed. |
| 3 | Out of memory, no disk space, or no buffer. |
| 7 | Reach the end of a file or a buffer. |
| 8 | File is readable but not writable. |
| 9 | File is writable but not readable. |
| 10 | A file doesn't exist or the socket destination is not reachable. |
| 13 | Unknown IO error. |
