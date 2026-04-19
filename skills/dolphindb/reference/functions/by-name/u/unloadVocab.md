# unloadVocab

首发版本：3.00.4，3.00.3.1

## 语法

`unloadVocab([vocabName])`

## 详情

从内存中删除已加载的词库。

## 参数

**vocabName** 可选参数，字符串标量，指定要删除的词库名称。若不指定，则删除所有词库。

## 返回值

无。

## 例子

```
unloadVocab("vocab1")
```

相关函数：loadVocab, tokenizeBert
