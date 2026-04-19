# oauthLogin

## 语法

`oauthLogin(oauthType, params)`

## 详情

目前 DolphinDB 已支持三种 OAuth 鉴权方式：Authentication Code（授权码模式，支持 Web）、Implicit（隐式授权模式，支持
Web）、Client Credentials（客户端凭证模式，支持 API）。该函数将根据传入的鉴权方式和鉴权参数向指定的授权服务器发送登录请求，最后返回字符串类型的
token 和用户信息。

## 参数

**oauthType** 字符串标量，用来指定 OAuth 的鉴权方式。可选值如下：

* 'authentication code'
* 'implicit'
* 'client credentials'

**params** 一个字典，用来指定鉴权参数。

* 若 *oauthType* 为 authentication code，则 *params* 传入{ code: string
  }。
* 若 *oauthType* 为 implicit，则 *params* 传入{ token\_type: string,
  access\_token: string, expires\_in?: string }。
* 若 *oauthType* 为 client credentials，则 *params* 传入{ … }。

## 返回值

字符串类型的 token 和用户信息。

## 例子

指定鉴权方式为 authentication code，同时指定对应参数，最后实现单点登录。

```
oauthLogin("authorization
              code",{"code":"9d823075cb151201925a"})
```

相关信息：单点登录
