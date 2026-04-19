# encryptModule

首发版本：3.00.5，3.00.4.3

## 语法

`encryptModule(name, [moduleDir], [overwrite=false])`

## 详情

对模块（dos 文件）进行加密，用于生成可分发的加密模块（dom 文件）。该函数必须要用户登录后才能执行。

注：

* `saveModule` 也可用于生成 dom 文件，但无法进行加密。
* `encryptModule` 包含函数序列化协议，所以会有兼容性考虑。
  + 在 3.00.0 版本 server 中加密的模块无法在任何 2.00.0 版本 server 上运行。
  + 在 2.00.0 版本 server 中加密的模块可以在同级别的 3.00.0 版本 server 中运行。比如 2.00.17 和
    3.00.4 是同级别的，所以 2.00.17 中生成的加密模块可以在 3.00.4 中运行。但不保证在 3.00.4 之前的
    3.00.0 版本 server 中能够运行。

## 参数

**name** 是一个字符串，用于指定模块文件的名称。

**moduleDir** 是一个字符串，用于指定模块文件所在的目录，默认为节点的 [home]/modules 目录。可通过 getHomeDir 查询 home 目录。

**overwrite** 是一个布尔值，用于指定是否覆盖已存在的同名 dom 文件。默认值为 false，即不覆盖。

## 返回值

无。

## 例子

假设节点 home 目录下的 modules 目录包含了 ta.dos 模块文件，将其序列化为加密的二进制文件。

```
encryptModule("ta")
```

函数执行成功后 modules 目录中会出现 ta.dom 文件。

![](../../images/encrypt_module.png)

**相关函数**

saveModule

loadModule
