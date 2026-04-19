# DolphinDB plugin catalog

One-line summary of every bundled plugin. Load any plugin from the marketplace with `installPlugin("<name>"); loadPlugin("<name>")`, then call its functions under the `<name>::` namespace.

Full manuals for every plugin are mirrored into `docs/plugins/`. This catalog is meant for quick discovery only — follow the link column to read the details.

| Plugin | One-line summary | In-skill path |
|--------|------------------|---------------|
| `amdquote` | AMD low-latency quote feed connector (Level-1/Level-2). | `docs/plugins/amdquote/` |
| `Arrow` | Read/write Apache Arrow IPC streams and files. | `docs/plugins/Arrow/` |
| `ASTTrader` | AST counter trading API connector. | `docs/plugins/ASTTrader.md` |
| `aws` | AWS S3 object storage read/write. | `docs/plugins/aws/` |
| `backtest` | Event-driven backtest engine with order-matching. | `docs/plugins/backtest/` |
| `CSM` | CSM counter trading API. | `docs/plugins/CSM.md` |
| `ctp` | CTP futures trading/market-data connector (SimNow / live). | `docs/plugins/ctp.md` |
| `ctp_2` | CTP futures trading/market-data connector (v2 API). | `docs/plugins/ctp_2.md` |
| `ctp_best_practice` |  | `docs/plugins/ctp_best_practice.md` |
| `datafeed` | Generic data-feed adapter (file/socket). | `docs/plugins/datafeed.md` |
| `dataxwriter` |  | `docs/plugins/dataxwriter/` |
| `efh` |  | `docs/plugins/efh.md` |
| `EncoderDecoder` | Binary encode/decode helpers (FIX, protobuf, custom). | `docs/plugins/EncoderDecoder.md` |
| `excel_add_in` |  | `docs/plugins/excel_add_in.md` |
| `feather` |  | `docs/plugins/feather/` |
| `gp` |  | `docs/plugins/gp/` |
| `gurobi` | Gurobi optimizer bindings. | `docs/plugins/gurobi.md` |
| `hbase` |  | `docs/plugins/hbase/` |
| `hdf5` |  | `docs/plugins/hdf5/` |
| `hdfs` |  | `docs/plugins/hdfs/` |
| `httpClient` |  | `docs/plugins/httpClient/` |
| `input` | Interactive prompt / stdin capture inside scripts. | `docs/plugins/input.md` |
| `insight` |  | `docs/plugins/insight/` |
| `kafka` |  | `docs/plugins/kafka/` |
| `kdb` |  | `docs/plugins/kdb/` |
| `LDAP` | LDAP authentication backend. | `docs/plugins/LDAP.md` |
| `lgbm` | LightGBM training / prediction bindings. | `docs/plugins/lgbm.md` |
| `libtorch` |  | `docs/plugins/libtorch/` |
| `mat` | MATLAB .mat file reader. | `docs/plugins/mat/` |
| `MatchingEngine` | Internal order matching / backtesting engine. | `docs/plugins/MatchingEngine/` |
| `matchingEngineSimulator` | Exchange matching engine simulator. | `docs/plugins/matchingEngineSimulator/` |
| `MDL` | Market Data Layer — unified high-frequency feed. | `docs/plugins/MDL.md` |
| `mongodb` |  | `docs/plugins/mongodb/` |
| `mqtt` | MQTT pub/sub client. | `docs/plugins/mqtt/` |
| `mseed` | MiniSEED seismic file reader. | `docs/plugins/mseed/` |
| `mysql` |  | `docs/plugins/mysql/` |
| `nsq` |  | `docs/plugins/nsq/` |
| `odbc` |  | `docs/plugins/odbc/` |
| `opc` |  | `docs/plugins/opc/` |
| `opcua` |  | `docs/plugins/opcua/` |
| `orc` |  | `docs/plugins/orc.md` |
| `order_management_engine` | Order-management engine for live/simulated trading. | `docs/plugins/order_management_engine.md` |
| `parquet` |  | `docs/plugins/parquet/` |
| `pulsar` | Apache Pulsar pub/sub. | `docs/plugins/pulsar.md` |
| `py` |  | `docs/plugins/py/` |
| `quantlib` |  | `docs/plugins/quantlib/` |
| `quick_fix` |  | `docs/plugins/quick_fix.md` |
| `rabbitMQ` |  | `docs/plugins/rabbitMQ.md` |
| `redis` |  | `docs/plugins/redis.md` |
| `rocketMQ` |  | `docs/plugins/rocketMQ.md` |
| `sevenzip` |  | `docs/plugins/sevenzip.md` |
| `signal` | DSP primitives (FFT, filter, complex math). | `docs/plugins/signal/` |
| `simulatedexchangeengine` | Simulated exchange engine (same as SimulatedExchangeEngine). | `docs/plugins/simulatedexchangeengine.md` |
| `slwriter` |  | `docs/plugins/slwriter.md` |
| `SSEQuotationFile` | SSE 交易所行情文件解析器. | `docs/plugins/SSEQuotationFile.md` |
| `svm` |  | `docs/plugins/svm/` |
| `tcpsocket` |  | `docs/plugins/tcpsocket.md` |
| `uniqueid` |  | `docs/plugins/uniqueid.md` |
| `websocket` |  | `docs/plugins/websocket.md` |
| `windtdf` |  | `docs/plugins/windtdf.md` |
| `windtdf_tutorial` |  | `docs/plugins/windtdf_tutorial.md` |
| `xgboost` | XGBoost train/predict bindings. | `docs/plugins/xgboost/` |
| `xtp` |  | `docs/plugins/xtp.md` |
| `zip` | ZIP archive read/write. | `docs/plugins/zip/` |
| `zlib` |  | `docs/plugins/zlib/` |
| `zmq` | ZeroMQ pub/sub/req/rep. | `docs/plugins/zmq/` |

## Common usage

```dolphindb
// one-time install (download from the plugin marketplace)
listRemotePlugins()
installPlugin("parquet")

// per-session load
loadPlugin("parquet")

// call a plugin function under its namespace
t = parquet::loadParquet("/data/foo.parquet")
```
