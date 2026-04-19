<!-- Auto-mirrored from upstream `documentation-main/db_distr_comp/db/textdb.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 文本存储引擎

DolphinDB 在 3.00.2 版本中，推出了基于倒排索引的文本存储引擎（TextDB）。TextDB 能够为主键存储引擎（ PKEY）
中的文本数据建立倒排索引，使得用户在对有倒排索引的文本列上进行全文检索时，性能得到显著提升，满足现代应用对海量文本数据高效检索与快速响应的需求：

* 在金融领域，可提取文本中的关键信息，结合 NLP 工具实现市场情绪分析、信息过滤与处理等高效应用。
* 在物联网领域，可高效管理海量日志数据，并支持实时搜索与分析。

DolphinDB TextDB 具有以下功能和特点：

* **查询加速**：

  + 对字符串类型的全文检索进行优化，相较于传统的 `LIKE` 查询，性能显著提升。
  + 对字符串类型的等值查询进行加速。
* **多种检索方式支持**：支持关键词、短语检索，前缀、后缀匹配，并允许在短语检索时指定词距。
* **多语言支持**：适用于中文、英文及中英文混合内容的检索。
* **高效存储与索引**：深度集成于 DolphinDB 存储引擎，相较于外部维护独立的倒排索引，减少了索引的空间占用，并提升了索引的读写效率。

## 实现原理

TextDB 的实现围绕以下几个方面展开：文本数据存储、文本索引构建、文本索引存储、文本数据检索。

### 文本数据存储

DolphinDB 中现有的存储引擎都支持存储文本数据，因此 TextDB
无需单独实现文本存储功能，而是基于现有存储引擎进行文本数据的存储。当前版本中，TextDB 仅支持基于主键存储引擎（PKEY）进行文本数据存储

。关于主键存储引擎的原理介绍，请参考主键存储引擎。

### 文本索引构建

TextDB 在指定的文本列上构建文本索引（倒排索引）。构建文本索引的步骤包括：

* 通过分词器将文本划分为单词序列。可能会对生成的单词序列做一定处理，包括将英文单词转为词干、将英文单词转为小写、忽略停止词等。（不会对原数据造成影响）
* 依据分词器划分出的单词序列构建文本索引。

**分词器**

分词器是 TextDB 的内部组件，其作用是将文本划分为单词序列，这些单词序列将用于后续构建文本索引。TextDB
内部支持多种分词器，用户需要在构建索引时指定合适的分词器类型：

* 英文分词器：按照空格和标点进行分词，适合于英文为主要内容的场景。
* 中文分词器：TextDB 使用 Jieba
  分词器作为内部中文分词器，其会按照预置的中文词库、空格和标点进行分词。适合于中文较多，仅有少量英文或对英文要求不高的场景。
* 混合分词器：英文按照单词分词，中文部分按照 Bigram 分词（以两个连续字符为单位进行分词，且会重叠。如 ‘武汉市长江大桥' 会被分词为
  '武汉' '汉市' '市长' '长江' '江大' '大桥'）。适合于中英文交替，且对英文要求较高的场景。
* none
  分词器：不分词。设置为该类型分词器后，将不对输入的文本进行分词处理，而是直接将整个文本索引起来。因此设置为不分词后，无法查询和匹配单个单词，只能查询和匹配整个文本。如，输入文本句子为
  ”apple is delicious”，则搜索 ”apple”, “delicious“ 均无法搜到输入的句子，只有搜索整个句子 ”apple
  is delicious” 才能搜索到结果。

**停止词处理**

停止词是常见的无重要意义的词汇。TextDB 使用的停止词列表如下：

* 英文停止词：

  ```
  "a", "an", "and", "are", "as", "at", "be", "but", "by",
  "for", "if", "in", "into", "is", "it",
  "no", "not", "of", "on", "or", "such",
  "that", "the", "their", "then", "there", "these",
  "they", "this", "to", "was", "will", "with"
  ```
* + 中文停止词与 Jieba 分词器的停止词列表一致。

查询中如果包含停止词，TextDB 会自动忽略它们，请注意这一行为对查询结果造成的影响。比如，由于 such 是停止词，所以查询 `apple
such banana` 等效于查询 `apple banana`。

**倒排索引**

TextDB使用倒排索引作为文本索引的实现方案。倒排索引是一种文本索引技术，先通过分词器将文本切分成词语，然后建立词语到文本 ID
的映射关系，这种映射关系被称为倒排表。倒排表的结构以单词作为 key，包含该单词的文本 ID 链表作为
value。这种结构使得在查询时，可以迅速定位到相关文本，而不需要逐一遍历所有文本。

### 文本索引存储

TextDB 会以 Level File 为单位进行文本索引的构建和存储。因此每个 Level File 内部都有独立的文本索引，用于对 Level File
内部存储的文本数据进行索引。在生成新的 Level File 时，TextDB
进行文本索引的构建与存储，文本数据的写入顺序与其在文本索引中的添加顺序一致，因此文本数据在 Level File 中的行号即为其在文本索引中的文本
ID，这种设计既简化了文本数据检索的查询步骤，也节省了存储空间。

### 文本数据检索

TextDB 在接收到查询请求后，会分别对内存中的数据和 Level File 进行检索，合并结果后返回。

详细步骤如下：

1. 首先，对 Cache Engine 中的数据（如果有）进行搜索。由于 TextDB 不会对 Cache Engine
   中的数据建立文本索引，因此对于 Cache Engine 中的数据，采取先分词器分词，后遍历检索的策略。
2. 其次，对 Level File 中的数据进行检索。因为每个 Level File 都有各自的文本索引，因此需要遍历所有 Level
   File，加载出对应文本列上的文本索引，在文本索引上进行检索，得到符合条件的检索结果。
3. 合并前两步中的结果作为最终返回结果。

与 `LIKE` 在查询时进行全表遍历不同，TextDB
通过索引进行查询。因此当数据总量越大且满足查询条件的数据越少时，TextDB 的查询性能相较于 `LIKE`
提升更加显著。

## 文本索引分析器

TextDB 提供丰富的配置选项，支持设置分词器、大小写敏感、中文分词模式以及英文词干匹配。可在创建文本索引时，设置 *indexes* 参数，例如：

```
indexes=textindex(parser=english, full=false, lowercase=true, stem=true)
```

**分词器**

*parser* 参数用于指定分词器。此参数没有默认值，必须显式指定。可选值包括：none、english、chinese 和 mixed：

* none：不分词。
* english：英文分词器，按空格和标点符号进行分词，适合英文为主的场景。
* chinese：中文分词器。基于中文词库、空格和标点进行分词。适用于中文内容为主，且英文较少或对英文要求不高的场景。
* mixed：混合分词器。英文按单词分词，中文按 Bigram 分词（以两个连续字符为单位进行分词，且会重叠。如 '武汉市长江大桥' 会被分词为 '武汉'
  '汉市' '市长' '长江' '江大' '大桥'）。适合于中英文交替，且对英文要求较高的场景。

**大小写敏感**

*lowercase* 参数用于设置是否忽略大小写。此参数在 *parser* 为 english、chinese 或 mixed 时有效：

* true：默认值，适用于需要忽略英文大小写的场景。
* false：适用于需要大小写敏感的场景。

**中文分词模式**

*full* 参数用于设置中文分词的模式。该属性仅在 *parser*=chinese 时有效：

* false：默认模式。词语之间不会重叠和包含。比如 '武汉市长江大桥' 会分成 '武汉市' 和 '长江大桥'。
* true：全分词模式。该模式会尽可能多的分析句子中包含的词语。比如 '武汉市长江大桥' 会分成 '武汉', '武汉市', '市长', '长江',
  '长江大桥', '大桥'。

**英文词干匹配**

*stem* 参数指定是否将英文单词作为词干匹配。该属性仅在 parser=english 且 lowercase=true 时生效。

* true：将英文单词作为词干。此时可能会匹配到相应的派生词，例如查询单词'dark'，可能会搜到含 'darkness' 的结果。
* false：默认值，只能精确查询结果。

## 文本索引查询函数

TextDB 提供以下查询函数用于文本索引查询。请注意，这些函数仅适用于已创建文本索引的列，且只能在查询语句的 `where`
子句中使用，无法单独调用。

下列函数的用法示例，请参见 [简单示例](#textdb_example)。

| **函数** | **功能** |
| --- | --- |
| matchAny | 查询包含任意给定词语的行 |
| matchAll | 查询包含所有给定词语的行 |
| matchPhrase | 查询包含指定短语的行 |
| matchPrefix | 查询包含指定词语前缀的行 |
| matchSuffix | 查询包含指定词语后缀的行 |
| matchPrefixSuffix | 查询同时包含指定前缀和后缀的词语所在的行 |
| matchPhrasePrefix | 查询包含指定短语前缀的行 |
| matchPhraseSuffix | 查询包含指定短语后缀的行 |
| matchPhraseInfix | 查询包含指定短语中缀的行 |
| matchSpan | 给定一个短语和词距 *slop*，查询包含该短语的行，允许目标短语中单词的词距小于等于 *slop* |
| matchUnorderedSpan | 给定一个短语和词距 *slop*，查询包含该短语的行，允许目标短语中单词的词距小于等于 *slop*，允许目标短语中单词的顺序与给定短语不同 |

## 等值查询加速

若不使用文本索引查询函数，而是直接在文本索引列上使用 `=` 或 `in`
查询，将自动使用文本索引，从而加速查询。触发查询加速需同时满足以下条件：

* 建立文本索引时设置分词器为 none 分词器。
* `=` 或 `in` 查询的另一侧为常量。

```
select textCol from pt where textCol = "apple";
select textCol from pt where textCol in ("apple","banana");
```

## 使用限制

**建库建表**

* 只能创建 PKEY 引擎下的数据库，因此在使用 `database` 函数创建数据库时，必须设置
  *engine*="PKEY"。
* 只能在 STRING 或 BLOB 类型的列上面建立文本索引。
* 支持单个表上创建多个索引，但不支持多列组合索引。

**数据写入**

* TextDB 支持在 STRING 列上建立文本索引，而 STRING 有 65535 字节的长度限制，因此超出长度限制的文本会被截断。
* 只支持 UTF-8 编码的字符串。遇到非法 UTF-8 字符（乱码）时，字符串会截断至乱码处。

**查询**

* TextDB 只支持在建立了文本索引的列上进行查询加速。
* 查询需直接作用于带索引的表，不能在表连接等操作后再使用 TextDB 的查询加速函数。
* 查询加速函数必须位于 where 子句中，不能位于 select、group by、order by 等其它子句。
* 查询加速函数必须位于 where 子句的顶层，不能嵌套于其他复合条件中。
* 只能使用 and 连接查询加速函数和其它普通查询条件，不能用 or。

## 简单示例

**例1**

**建库建表**

目前 TextDB 只支持基于 PKEY 引擎使用，因此建库时需要指定 engine="PKEY"。

```
// 创建 PKEY 引擎中的数据库
dbName = "dfs://test"
if (existsDatabase(dbName)){
        dropDatabase(dbName)
}

// 通过函数创建数据库
db = database(dbName, HASH, [INT, 3], engine=`PKEY)

// 通过SQL语句创建数据库
create database "dfs://test"
partitioned by HASH([INT, 3]),engine="PKEY"

// 通过函数创建表，并通过indexes参数指定文本索引，其中textCol列为索引列
schematb = table(5:5, `col0`col1`textCol, [INT,INT,STRING])
pt = createPartitionedTable(dbHandle=db,table=schematb,tableName=`pt, partitionColumns=`col0, primaryKey=`col0`col1, indexes={"textCol":"textindex(parser=english,full=false,lowercase=true,stem=false)"})

// 通过SQL语句创建表，并通过indexes参数指定文本索引，其中textCol列为索引列
CREATE TABLE "dfs://test"."pt"(
    col0 INT,
    col1 INT,
    textCol STRING [indexes="textIndex(parser=english,full=true,lowercase=true,stem=false)"]
)
PARTITIONED BY col0,
primaryKey=`col0`col1
```

**索引查询**

本节展示如何通过 TextDB 提供的文本索引查询函数进行查询。

首先基于上一节建立的库表，插入一些数据用于后续查询：

```
textData = [
        "The sun was shining brightly as I walked down the street, enjoying the warmth of the summer day.",
        "I enjoy a refreshing smoothie made with apple every morning.",
        "The sound of the waves crashing against the shore was a soothing melody that helped me relax after a long day.",
        "The city skyline looked stunning from the top of the mountain, with the lights twinkling like stars in the night sky.",
        "The picnic basket was filled with juicy apple slices and ripe banana for a healthy snack."
    ]
data = table(1..5 as col1, 1..5 as col2, textData)

//分区表中写入数据后，强制将数据写入磁盘
pt.append!(data)
```

执行查询：

```
//查询数据
// 查询含"apple"或"banana"的行
select textCol from pt where matchAny(textCol, "apple banana");

// 查询同时包含"apple"和"banana"的行
select textCol from pt where matchAll(textCol, "apple banana");

// 查询所有包含短语"juicy apple"的行
select textCol from pt where matchPhrase(textCol, "juicy apple");

// 查询所有包含以"ap"为前缀的单词的行
select textCol from pt where matchPrefix(textCol, "ap");

// 查询所有包含以"ana"为后缀的单词的行
select textCol from pt where matchSuffix(textCol, "ana");

// 查询所有包含以"a"为前缀，且以"le"为后缀的单词的行
select textCol from pt where matchPrefixSuffix(textCol, "ap", "le");

// 查询包含以"filled with juicy ap" 为前缀的短语所在的行
select textCol from pt where matchPhrasePrefix(textCol, "filled with juicy", "ap");

// 查询包含以"th of the summer day"为后缀的短语所在的行
select textCol from pt where matchPhraseSuffix(textCol, "th", "of the summer day");

// 查询包含以"hts twinkling like sta"为中缀的短语所在的行
select textCol from pt where matchPhraseInfix(textCol, "hts", "twinkling like", "sta");

/**
  查询包含了 "enjoying the summer day"的短语的行，且如果短语内部有小于等于2个无关词汇，也可以被匹配到
  如 "enjoying the summer day", "enjoying xxx the yyy summer day"都会被匹配，其中xxx,yyy为无关词汇
  注：如果查询字段或目标字符串中包含停止词，停止词会被预先过滤掉，因此均不计入"无关词汇个数"
*/
select textCol from pt where matchSpan(textCol, "enjoying the summer day", 2)

/**
  查询包含了 "day summer the enjoying"的短语的行，且如果短语内部有小于等于2个无关词汇，也可以被匹配到。
  且忽略目标文本中 day summer the enjoying之间的相对顺序
  如 "enjoying the xxx summer day", "day xxx summer the yyy enjoying"都会被匹配，其中xxx,yyy为无关词汇
*/
select textCol from pt where matchUnorderedSpan(textCol, "day summer the enjoying", 2)
```

**例2**

```
// 创建 PKEY 引擎中的数据库
dbName = "dfs://test"
if (existsDatabase(dbName)){
        dropDatabase(dbName)
}
create database "dfs://test"
partitioned by HASH([INT, 3]),engine="PKEY"

// 通过SQL语句创建表，并通过indexes参数指定文本索引，其中textCol列为索引列
CREATE TABLE "dfs://test"."pt"(
    col0 INT,
    col1 INT,
    textCol STRING [indexes="textIndex(parser=chinese,full=true,lowercase=true)"]
)
PARTITIONED BY col0,
primaryKey=`col0`col1

// 模拟数据并写入
textData = [
    "金融市场的波动性对投资者的心理预期产生重要影响。",
    "投资者需要关注通货膨胀率的变化，通胀预期往往影响股市和债市的表现。",
    "关税提高通过增加进口商品价格和生产成本，从而推动物价上涨，进而加剧通货膨胀。",
    "提高关税可能导致进口商品价格上涨，从而影响国内消费水平。",
    "经济学家警告，持续的高通货膨胀可能引发恶性通货膨胀，而关税可能是其中的一个因素。"
]
data = table(1..5 as col1, 1..5 as col2, textData)
loadTable("dfs://test","pt").append!(data)

// 查询包含 "关税" 的行
select * from loadTable("dfs://test","pt") where matchAll(textCol,"关税")

// 查询包含 "关税" 或 "通货膨胀" 的行
select * from loadTable("dfs://test","pt") where matchAny(textCol,"关税通货膨胀")

// 查询包含 "关税" 和 "通货膨胀" 的行
select * from loadTable("dfs://test","pt") where matchAll(textCol,"关税通货膨胀")
```
