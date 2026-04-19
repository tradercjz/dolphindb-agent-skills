# initIMOLTPCheckpointEncryption

首发版本：3.00.3

## 语法

`initIMOLTPCheckpointEncryption(mode)`

## 详情

该函数用于初始化 IMOLTP 库表的数据静态加密，仅支持全局加密（即对 checkpoint 中的所有库表统一应用加密）。

注意：仅 Linux 系统支持该功能。一旦完成初始化，加密方式无法修改或关闭，请谨慎操作。

## 参数

**mode** 字符串标量，指定表的加密方式，默认为不加密（明文模式）。目前支持以下可选值（大小写不区分）：plaintext, aes\_128\_ctr,
aes\_128\_cbc, aes\_128\_ecb, aes\_192\_ctr, aes\_192\_cbc, aes\_192\_ecb, aes\_256\_ctr,
aes\_256\_cbc, aes\_256\_ecb, sm4\_128\_cbc, sm4\_128\_ecb

## 返回值

无。

## 例子

```
initIMOLTPCheckpointEncryption(`aes_128_ctr)
```
