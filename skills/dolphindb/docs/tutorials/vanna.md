<!-- Auto-mirrored from upstream `documentation-main/tutorials/vanna.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 或
vn.train(ddl='''
  create database "dfs://test"
  partitioned by VALUE(1..10), HASH([SYMBOL, 40])
  engine='TSDB'
''')
```

### 4.3 文档关键词匹配

DolphinDB 提供了多种文本索引查询函数来查询已建立文本索引的列。本教程使用 matchAny 函数来进行关键词匹配，即查询包含任意给定词语的文档文本。例如在 get\_related\_ddl
接口中，查询匹配关键字的 DDL 语句使用了如下 SQL：

```
select id, question, content, embedding from loadTable("{self.db_name}", "{self.tb_name}")
where type == "ddl" and matchAny(content, keywords)
```

注：

注意文本存储引擎存在一些使用限制，若自定义或修改接口，请确定查询能正常触发文本索引加速。

### 4.4 向量相似度检索

DolphinDB 提供了 rowEuclidean
函数来查询已建立向量索引的列，即计算输入向量与指定向量列的欧式距离。例如在 get\_related\_ddl 接口中，查询距离关键字 embedding 最近的
DDL 语句使用了如下 SQL：

```
select id, question, content, embedding from loadTable("{self.db_name}", "{self.tb_name}")
where type == "ddl"
order by rowEuclidean(embedding, embedding_) asc
limit {self.top_n}
```

注：

注意向量存储引擎存在一些使用限制，若自定义修改接口，请使用 HINT\_EXPLAIN 确定查询能正常触发向量索引加速。

## 5. 依赖

执行如下命令安装依赖：

```
pip install dolphindb
pip install vanna
```

离线安装 dolphindb 包可参考《离线安装 Python API》。

## 6. 使用案例

注：

LLM 的幻觉问题目前依然无法完全避免，请注意甄别回答的正确性。

在首次使用前，需要连接配置的 DolphinDB 数据节点，修改附件的 import.dos 内的相关配置项并全选执行，创建 Vanna 的后端库表并导入
DolphinDB 文档和 DDL 定义。

Vanna 官方提供了开箱即用的 [web 应用](https://vanna.ai/docs/web-app/)，可以在 jupyter notebook 里启动或独立启动。启动前需要参照《配置项》一节填写附件
demo.py 内的配置项，然后可以使用如下命令启动 web 应用：

```
python demo.py
```

命令行会输出 Vanna web 应用的默认地址为 http://localhost:8084，使用浏览器前往该地址，可见页面如下：

![](images/vanna/6-1.png)

输入查询问题后，Vanna 会自动生成对应的 SQL，执行查询并返回结果。

![](images/vanna/6-2.png)

接着 Vanna 会尝试对结果进行绘图，并用文本总结结果：

![](images/vanna/6-3.png)

然后 Vanna 会询问该回答是否正确，可见除了绘图以外均正确，可以点击 Yes, train as Question-SQL pair
按钮将本次回答存储为训练数据（绘图结果不参与训练）：

![](images/vanna/6-4.png)

最后 Vanna 会给出一些 followup 问题，可以直接点击询问：

![](images/vanna/6-5.png)

下面展示回答错误的情况，询问一个比较困难的问题：

![](images/vanna/6-6.png)

可以点击 Auto Fix 来让 Vanna 根据错误信息自动纠错，但依然回答错误：

![](images/vanna/6-7.png)

由于缺少正确的问题-SQL对示例，加上 asof join 是 DolphinDB 独特的语法，Vanna 很难给出正确答案。此时我们可以点击 Manually Fix
按钮手动给出答案：

![](images/vanna/6-8.png)

可见查出了正确的结果，可以点击 Yes, train as Question-SQL pair 按钮将其存储为训练数据，这样下次提出类似问题时，Vanna
更有可能给出正确的答案。

![](images/vanna/6-9.png)

新建一个会话，然后再次询问同样的问题，可见 Vanna 能够根据上次的回答给出正确的答案：

![](images/vanna/6-10.png)

另外查看启动程序的终端，可以看到打印了相关日志，可用于调试程序：

![](images/vanna/6-11.png)

## 7. 总结

DolphinDB 凭借其高性能的文本存储引擎（TextDB）和向量存储引擎（VectorDB），为 Vanna 这一融合 RAG 与交互式数据库查询的 AI
框架提供了理想的底层支持。借助 DolphinDB，Vanna
能够高效处理海量文本与向量数据、利用丰富计算函数优化提示工程，并实现一站式数据存储、检索与分析，充分展现了 DolphinDB 在 AI
增强数据库场景下的卓越性能与扩展优势。

## 8. 附件

[docs.zip](https://cdn.dolphindb.cn/zh/tutorials/script/vanna/docs.zip)

[demo.py](https://cdn.dolphindb.cn/zh/tutorials/script/vanna/demo.py)

[import.dos](https://cdn.dolphindb.cn/zh/tutorials/script/vanna/import.dos)
