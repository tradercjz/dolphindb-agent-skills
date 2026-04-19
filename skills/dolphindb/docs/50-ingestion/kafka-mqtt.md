# Kafka / MQTT / MQ ingestion

Real-time ingest usually lands data in a **stream table**, then a
subscription persists to DFS.

## Kafka

```dolphindb
loadPlugin("kafka")

conf = dict(STRING, STRING)
conf["metadata.broker.list"] = "kafka1:9092,kafka2:9092"
conf["group.id"] = "ddb-demo"

// create consumer
consumer = kafka::consumer(conf)

// subscribe
kafka::subscribe(consumer, ["ticks"])

// poll loop — decode JSON → append to stream table
share streamTable(1000000:0, `ts`sym`px, [TIMESTAMP, SYMBOL, DOUBLE]) as ticks

def onBatch(consumer, sink, timeoutMs = 100) {
    msgs = kafka::pollBatch(consumer, 1000, timeoutMs)
    if(size(msgs) > 0) {
        t = select
            nanotimestamp(value.ts)      as ts,
            symbol(value.sym)            as sym,
            double(value.px)             as px
        from msgs
        sink.append!(t)
    }
}

submitJob("kafkaPoller", "poll kafka", loop, onBatch{consumer, ticks}, 1000)
```

Downstream: `subscribeTable` on `ticks` → DFS appender engine.

## MQTT

```dolphindb
loadPlugin("mqtt")

share streamTable(1000000:0, `ts`device`v, [TIMESTAMP, SYMBOL, DOUBLE]) as iot

def onMsg(msg) {
    t = parseJsonMsg(msg)   // user-defined
    iot.append!(t)
}

handle = mqtt::connect("tcp://broker:1883", "ddb-demo")
mqtt::subscribe(handle, "sensors/#", 1, onMsg)
```

## Plugins relevant to ingest

- `kafka` — Apache Kafka.
- `mqtt` — MQTT pub/sub.
- `pulsar` — Apache Pulsar.
- `rocketMQ` / `rabbitMQ` / `zmq` / `redis`.
- `nsq` — NSQ Level-2 quotes.
- `insight` — HuaXin INSIGHT quotes.
- `amdquote`, `amdhistory` — AMD market data.
- `opcua`, `opc` — industrial IoT.

See `reference/plugins-catalog.md` for the complete list.

## Traps

- **Plugin polling runs in a server job** — remember to `submitJob` /
  `scheduledJob` so it stays alive across sessions.
- **Back-pressure**: if the stream table's subscribers can't keep up,
  memory grows. Persist the stream table and cap `cacheSize`.
- **Deserialization cost** (JSON/FIX/protobuf) is often the bottleneck —
  consider plugin-side decoders (`encoderDecoder` plugin) or pre-normalize
  upstream.

## See also

- `docs/40-streaming/stream-table.md`, `docs/40-streaming/subscribe.md`.
- Upstream: `mq_import.md` (if present).
