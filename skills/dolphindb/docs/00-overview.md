# DolphinDB overview

DolphinDB is a **columnar, in-memory-first, distributed time-series database**
with a **built-in vectorized programming language**. One server process
handles storage, SQL, scripting, and stream computing; clients talk to it
over a binary protocol or language-specific APIs.

## What is it good at

- Storing and querying **trillions of rows of time-series data** (tick, bar,
  IoT, logs) with sub-second latency.
- Running **vectorized analytics** (moving windows, cross-section, TA-lib) as
  first-class SQL operators (`context by`, `pivot by`, `m*` / `tm*` / `cum*`
  windows, `rowXxx` row-wise aggregates).
- **Real-time stream computing**: stream tables, subscriptions, reactive
  state engine, time-series / asof / window / session engines, CEP.
- **Quant / IoT / OMC** workloads that need to mix historical + real-time in
  one process without shipping data through Kafka/Flink.

## What it is NOT

- Not a general-purpose OLTP database. Use `PKEY` / `IMOLTP` engines when you
  need row-level update/delete; avoid row-by-row inserts with `TSDB`/`OLAP`.
- Not a drop-in for PostgreSQL/MySQL. Its SQL dialect is **close but
  non-standard** (see `docs/20-sql/context-by.md` and friends).

## Node types

| Node type | Role |
|-----------|------|
| **Controller** | Metadata + cluster coordination (Raft-replicated). Never store user data here. |
| **Data node** | Stores DFS chunks; executes queries + stream tasks. |
| **Compute node** | Stateless query worker; pairs with remote data nodes (storage–compute separation). |
| **Agent** | Starts/stops other node processes on the same host. |

Single-node deployments run everything as one process (good for dev). Use
`getClusterPerf()` / `getClusterChunksStatus()` to inspect a cluster.

## Storage engines

Choose the engine at database-creation time; you cannot change it later.

| Engine | Use when | Key traits |
|--------|----------|------------|
| **TSDB** | Tick / high-frequency time-series | Sorted-by-time LSM; supports `sortColumns`, `keepDuplicates`. Default for new projects. |
| **OLAP** | Large analytic tables, append-heavy, no updates | Columnar; fastest on wide scans. |
| **PKEY** | Need `upsert` / point update / delete by primary key | LSM with primary-key index; supports `upsert!`. |
| **IMOLTP** | Pure in-memory OLTP | ACID, row-level update; small datasets. |
| **VectorDB** | Vector similarity search (embeddings) | HNSW index. |
| **TextDB** | Full-text search | Inverted index. |
| **IOTDB** | Metric / tag storage for industrial IoT | Point-tag model. |

→ See `docs/30-database/` for per-engine detail, and
`docs/about/ddb_intro.md` for the official marketing-style overview.

## File formats & files you will encounter

- `.dos` — DolphinDB script file.
- `.dolphindb` — configuration file (e.g. `dolphindb.cfg`, `cluster.cfg`).
- `dfs://<db>` — distributed database URL.
- `loadTable("dfs://trades", \`trade)` — open a distributed table handle.

## Quick orientation

- **Run a script**: `dolphindb -run script.dos` (server CLI), or via an API.
- **Web UI**: DolphinDB ships with a web notebook at `http://<host>:8848`.
- **Clients**: VSCode extension, DataGrip, DBeaver, Grafana, Power BI,
  Superset, Jupyter — see `reference/plugins-catalog.md` and
  `docs/60-api/tools/`.
