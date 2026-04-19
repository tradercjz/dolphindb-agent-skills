# Plugins — navigation index

## Contents
- How to install & load
- File formats (parquet, hdf5, Arrow, feather, orc, mat, mseed, zip)
- Databases & file stores (MongoDB, MySQL, ODBC, HBase, HDFS, kdb, Redis, AWS S3)
- Messaging (Kafka, Pulsar, RabbitMQ, RocketMQ, MQTT, ZeroMQ)
- Network (httpClient, websocket, tcpsocket)
- Market-data feeds (AMD, INSIGHT, EFH, MDL, Wind, NSQ, SSE, CTP, XTP)
- Trading / execution (ASTTrader, CSM, QuickFIX, Backtest, MES, OME)
- Industrial IoT (OPC UA / OPC DA/HDA)
- Math / optimization (QuantLib, Gurobi, signal)
- Machine learning (LibTorch, XGBoost, LightGBM, svm, gp)
- Embedded runtimes (Python, Excel), auth, utilities
- Plugin development

70+ plugin pages mirrored from upstream `documentation-main/plugins/`. For
a one-line blurb on each, see `../../reference/plugins-catalog.md`. This
index groups full manuals by functional category.

## How to install & load

```dolphindb
login("admin", "123456")
listRemotePlugins()                       // see what's available
installPlugin("<name>")                    // one-time
loadPlugin("<name>")                       // per session
// functions become available under <name>:: namespace
```

See `plg_intro.md`, `plg_howtos.md` for installation caveats, and
`plg_mkt_inst.md` for the plugin marketplace flow.

---

## File formats

| Format | File / dir | Notes |
|--------|-----------|-------|
| Parquet  | `parquet/` (dir) | read/write; row-group level. |
| HDF5     | `hdf5/` | named datasets, attributes. |
| Arrow    | `Arrow/` | Apache Arrow IPC stream/file. |
| Feather  | `feather/` | Feather v2. |
| ORC      | `orc.md` | Apache ORC. |
| mat      | `mat/` | MATLAB .mat files. |
| mseed    | `mseed/` | MiniSEED seismic. |
| zip / 7z / zlib | `zip/`, `sevenzip.md`, `zlib/` | archive / compression. |

## Databases & file stores

| Target | File / dir |
|--------|-----------|
| MongoDB | `mongodb/` |
| MySQL | `mysql/` |
| ODBC (generic JDBC/ODBC) | `odbc/` |
| HBase | `hbase/` |
| HDFS | `hdfs/` |
| kdb+ | `kdb/` |
| Redis | `redis.md` |
| AWS (S3) | `aws/` |

## Messaging / streaming transport

| Bus | File |
|-----|------|
| Kafka | `kafka/` |
| Apache Pulsar | `pulsar.md` |
| RabbitMQ | `rabbitMQ.md` |
| RocketMQ | `rocketMQ.md` |
| MQTT | `mqtt/` |
| ZeroMQ | `zmq/` |

## Network / transport

| File | Purpose |
|------|---------|
| `httpClient/` | HTTP(S) client for REST/webhooks. |
| `websocket.md` | WebSocket client. |
| `tcpsocket.md` | Raw TCP client. |

## Market-data connectors (financial)

| Vendor / source | File |
|-----------------|------|
| AMD L1/L2 live | `amdquote/` |
| AMD historical | `amdquote/amdhistory.md` |
| HuaXin INSIGHT | `insight/` |
| Exegy EFH | `efh.md` |
| MDL unified feed | `MDL.md` |
| Wind TDF | `windtdf.md`, `windtdf_tutorial.md` |
| 中信 NSQ L2 | `nsq/` |
| SSE 行情文件 | `SSEQuotationFile.md` |
| Generic data feed | `datafeed.md` |

## Trading / execution

| Plugin | File | Role |
|--------|------|------|
| CTP futures | `ctp.md`, `ctp_2.md`, `ctp_best_practice.md` | CTP counter |
| XTP | `xtp.md` | XTP counter |
| AST | `ASTTrader.md` | AST counter |
| CSM | `CSM.md` | CSM counter |
| QuickFIX | `quick_fix.md` | FIX client |
| **Backtest** | `backtest.md` + `backtest/` dir | Event-driven strategy backtest. See also `../backtest/`. |
| Matching Engine Simulator | `matchingEngineSimulator/` | L2-accurate fill simulator. |
| Matching Engine | `MatchingEngine/` | Internal order matching. |
| Simulated Exchange Engine | `simulatedexchangeengine.md` | Full virtual exchange. |
| Order Management Engine | `order_management_engine.md` | Live/paper order lifecycle. |

## Industrial IoT

| Plugin | File |
|--------|------|
| OPC UA | `opcua/` |
| OPC DA/HDA | `opc/` |

## Math / optimization

| Plugin | File |
|--------|------|
| QuantLib | `quantlib/` |
| Gurobi | `gurobi.md` |
| Signal processing (FFT, filters, complex) | `signal/` |

## Machine learning

| Plugin | File |
|--------|------|
| LibTorch (PyTorch) | `libtorch/` |
| LightGBM | `lgbm.md` |
| XGBoost | `xgboost/` |
| libsvm | `svm/` |
| Symbolic regression / GP | `gp/` |

## Embedded runtimes

| Plugin | File |
|--------|------|
| Python (3.9+) | `py/` |
| Excel add-in | `excel_add_in.md` |

## Auth / security

| Plugin | File |
|--------|------|
| LDAP | `LDAP.md` |

## Misc utilities

| Plugin | File |
|--------|------|
| UniqueID (snowflake-style IDs) | `uniqueid.md` |
| Input (stdin / interactive) | `input.md` |
| Encoder / decoder (FIX, protobuf, …) | `EncoderDecoder.md` |
| DataX writer (for DataX ingest) | `dataxwriter/` |
| Schemaless writer | `slwriter.md` |

## Plugin development

| Topic | File |
|-------|------|
| Intro | `plg_intro.md` |
| How-tos | `plg_howtos.md` |
| Development tutorial | `plg_dev_tutorial.md` |
| Advanced development | `plg_dev_adv.md` |
| Marketplace | `plg_mkt_inst.md` |
| Performance comparison | `performance_comparison.md` |

---

## Cross-references

- Quick one-liners: `../../reference/plugins-catalog.md`.
- Backtest plugin hub: `../backtest/README.md`.
- Ingest via Kafka/MQTT: `../50-ingestion/kafka-mqtt.md`.
- File format ingest: `../50-ingestion/hdf5-parquet.md`.
- Client APIs (not plugins): `../60-api/`.
