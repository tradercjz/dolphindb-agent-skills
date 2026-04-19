# recursiveSplitText

首发版本：3.00.4，3.00.3.1

## 语法

`recursiveSplitText(text, [maxLength=300], [chunkOverlap=20], [separators],
[keepSeparator=true])`

## 详情

根据分隔符对文本进行递归分段。

## 参数

**text** LITERAL类型标量，表示需要分段处理的输入文本。

**maxLength** 正整数，表示每个分段的最大长度，默认值为 300。

**chunkOverlap** 不超过 *maxLength* 的非负整数，表示相邻分段允许重复的最大长度，默认值为 20。

**separators** STRING 类型向量，表示自定义分隔符列表。默认值为 `["\n\n", "\n", " ",
""]`。暂不支持正则表达式。

**keepSeparator** 布尔值，表示是否保留分隔符：

* true：默认值，保留分隔符，此时分隔符将保留在后半段文本开头。
* false：不保留分隔符。

## 返回值

字符串向量。

## 例子

```
text = "这是第一句文字。这是第二句，带有逗号。接着是第三句，它比前两句更长，需要被进一步分割。最后一句是结束语。"
separators = ["。","，"]

chunks = recursiveSplitText(text, maxLength=15, chunkOverlap=5, separators=separators, keepSeparator=true)
```
