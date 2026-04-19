<!-- Auto-mirrored from upstream `documentation-main/tutorials/OHLC.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 订阅DolphinDB(本机8848端口)上的OHLC流数据表
s.subscribe("127.0.0.1", 8848, handler, "OHLC","python_api_subscribe",0)
Event().wait()
```

也可通过 Grafana 等可视化系统来连接 DolphinDB，对输出表进行查询并将结果以图表方式展现。
