# isClientAuth

## 语法

`isClientAuth()`

## 详情

获取配置项 *enableClientAuth* 的值。

当*enableClientAuth* 设置为 true 时，访客用户必须登录才能执行脚本，可通过 API
调用少数运维函数，包括：`isClientAuth`, `getNodeType`,
`getNodeAlias`, `login`,
`authenticateByTicket`, `getControllerAlias`,
`version`, `license`,
`getActiveMaster`, `getClusterPerf`,
`loadClusterNodesConfigs`, `getConfig`,
`oauthLogin`, `getCurrentSessionAndUser`,
`getDynamicPublicKey`。

## 返回值

一个布尔值。
