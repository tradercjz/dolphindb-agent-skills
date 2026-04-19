# base64Decode

## 语法

`base64Decode(X)`

## 详情

将 Base64 编码的数据解码为二进制数据。

## 参数

**X** 字符串标量或向量。

## 返回值

BLOB 类型标量或向量。

## 例子

```
base64Decode(base64Encode(`hello))
// output
hello

base64Decode(base64Encode(`hello`world))
// output
["hello","world"]
```

相关函数：base64Encode
