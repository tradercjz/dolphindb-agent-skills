# updatePKEYDeleteBitmap

## 语法

`updatePKEYDeleteBitmap(chunkId)`

## 详情

更新 PKEY 引擎的 delete bitmap，完成后清空主键的暂存缓冲区。

## 参数

**chunkId** STRING 类型标量或向量，表示 chunk 对应的 ID。

## 返回值

无。

## 例子

```
updatePKEYDeleteBitmap(chunkId="1486f935-6f87-479c-b341-34c6a303d4f9")
```
