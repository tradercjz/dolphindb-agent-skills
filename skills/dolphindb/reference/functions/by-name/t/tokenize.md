# tokenize

## 语法

`tokenize(text, parser, [full=false], [lowercase=true],
[stem=false])`

## 详情

此函数可用于检查分词操作的实际效果。

根据指定的设置对输入文本进行分词操作，并返回一个 STRING 类型的向量，包含分词的结果。

## 参数

**text** STRING 类型标量，表示待分词的文本。

**parser** STRING 类型标量，指定分词器。没有默认值，必须显式指定。可选值为 'none', 'english', 'chinese',
'mixed'：

* none：不分词。
* english：英文分词器，按照空格和标点进行分词。
* chinese：中文分词器，按照中文词库、空格和标点进行分词。
* mixed：混合分词器。英文按单词分词，中文按 Bigram 分词。

**full** 设置中文分词时的分词模式，仅在 parser='chinese' 时有效：

* false：默认模式。词语之间不会重叠和包含。
* true：全分词模式。该模式会尽可能多的分析句子中包含的词语。

**lowercase** 布尔类型标量，表示是否将英文单词转换为小写（不会对原数据造成影响）。该属性在 *parser* 为 english,
chinese, mixed 时有效。默认值为 true。

**stem** 是否将英文单词作为词干匹配。该属性仅在 parser='english'，且 lowercase=true 时生效。默认值为 false。

## 返回值

STRING 类型向量。

## 例子

```
text1 = "The sun was shining brightly as I walked down the street, enjoying the warmth of the summer day."
tokenize(text=text1, parser='english', lowercase=false, stem=true)
// output:["The","sun","shine","bright","I","walk","down","street","enjoy","warmth","summer","day"]

text2 = "武汉市长江大桥"
tokenize(text=text2, parser='chinese', full=true)
// output:["武汉","武汉市","市长","长江","长江大桥","大桥"]
```
