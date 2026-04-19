<!-- Auto-mirrored from upstream `documentation-main/stream/event_stream_deserializer.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 事件流反序列化器

事件流反序列化器（Stream Event Deserializer）将序列化的流事件数据转换回原始事件对象。CEP 引擎内部实现了
StreamEventDeserializer，因此无需额外定义反序列化器，引擎便会自动反序列化从订阅的异构流表中获取到的数据。
