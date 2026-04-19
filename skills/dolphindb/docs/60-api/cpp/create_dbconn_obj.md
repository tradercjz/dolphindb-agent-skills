<!-- Auto-mirrored from upstream `documentation-main/api/cpp/create_dbconn_obj.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 创建 DBConnection 类对象

以下为 DBConnection 类的构造函数声明：

```
DBConnection(bool enableSSL = false, bool asyncTask = false, int keepAliveTime = 7200, bool compress = false, bool python = false, bool isReverseStreaming = false);
```

以下为参数介绍：

## 加密参数

`enableSSL`：表示是否启用加密通讯，默认值为 false。

注：

1. 必须在编译API动态库的时候指定-DUSE\_OPENSSL选项，否则该参数无效果。
2. DolphinDB 自 1.10.17 与 1.20.6 版本起支持加密通讯参数 *enableSSL*。
3. DolphinDB 须同时设置配置项 `enableHTTPS=true` 方可启动 SSL 通讯。详情可参考 enableHTTPS。

## 异步参数

`asyncTask`：表示是否开启异步通讯，默认值为 false。

开启异步通讯后，在采用 `DBConnection::run()` 方法与 DolphinDB 端进行通讯时，API
不再等待任务执行完毕，而是直接返回，用户无法获知执行结果。

注：

DolphinDB 自 1.10.17 与 1.20.6 版本起支持异步通讯。

## 保活参数

`keepAliveTime`：表示在 TCP 连接空闲状态下，两次保活包之间的间隔时间，默认参数为 7200，单位秒（s）。

注：

1. 该参数在 Linux、Windows、MacOS 平台均可生效。
2. 在连接时同样也可以设置该参数。

## 压缩参数

`compress`：表示是否开启压缩，默认参数为 false。

该模式适用于大数据量的写入或查询。压缩数据后再进行传输，这可以节省网络带宽，但也会增加 DolphinDB 和 API 端的计算量。

## 其他参数

* `python`：内部保留参数，用户无需设置。
* `isReverseStreaming`：内部保留参数，用户无需设置。

## 用法示例

```
DBConnection conn(true, false, 30, true);   //创建一个连接对象，启用加密通信和压缩选项，不开启异步通信，保活时间间隔为30s
```
