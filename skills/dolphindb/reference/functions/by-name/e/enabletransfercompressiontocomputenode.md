# enableTransferCompressionToComputeNode

首发版本：3.00.5

## 语法

`enableTransferCompressionToComputeNode(enable)`

## 详情

用于控制数据节点在向计算节点传输数据前是否进行压缩。

## 参数

**enable** 布尔值，指定是否压缩将被传输的数据。true 表示压缩，false 表示不压缩。

## 返回值

无

## 例子

```
enableTransferCompressionToComputeNode(true)
```

**相关函数：**isTransferCompressionToComputeNodeEnabled
