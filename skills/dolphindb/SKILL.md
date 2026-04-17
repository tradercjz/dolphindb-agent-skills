---
name: dolphindb
description: "Use when working with DolphinDB: writing DolphinDB scripts, SQL queries, time-series data analysis, stream computing (subscribeTable, DStream), distributed tables (DFS), Python/Java/C++ API usage, data ingestion, and DolphinDB database administration. Covers syntax reference, built-in function catalog, best practices, and common patterns."
license: Apache-2.0
---

# DolphinDB Knowledge Base

DolphinDB is a high-performance distributed time-series database with a built-in programming language. This skill provides offline reference documentation so you can help answer questions and write code without needing internet access.

## How to Use This Skill

When the user asks about DolphinDB, **first check the documentation index below** to find the most relevant file, then read it.  
For quick questions, the [High-Frequency Patterns](#high-frequency-patterns) section below may already contain the answer.

---

## Documentation Index

| # | Area | File | What's covered |
|---|------|------|----------------|
| 1 | Overview & Concepts | [docs/00.overview.md](docs/00.overview.md) | Architecture, node types, storage engines |
| 2 | Quick Start | [docs/01.quick-start.md](docs/01.quick-start.md) | Install, connect, first script |
| 3 | Data Types | [docs/02.data-types.md](docs/02.data-types.md) | Scalar, vector, matrix, table, dict, all type keywords |
| 4 | DolphinDB Script Language | [docs/03.scripting.md](docs/03.scripting.md) | Variables, control flow, functions, modules, error handling |
| 5 | SQL | [docs/04.sql.md](docs/04.sql.md) | SELECT, UPDATE, INSERT, JOIN, GROUP BY, window functions, context by |
| 6 | Distributed Tables (DFS) | [docs/05.distributed-tables.md](docs/05.distributed-tables.md) | Database/table creation, partitioning schemes, loadTable |
| 7 | In-Memory Tables | [docs/06.in-memory-tables.md](docs/06.in-memory-tables.md) | table(), keyedTable, indexedTable, streamTable |
| 8 | Stream Computing | [docs/07.streaming.md](docs/07.streaming.md) | subscribeTable, DStream, reactive state engine, snapshot |
| 9 | Built-in Functions | [docs/08.functions.md](docs/08.functions.md) | Math, string, time, financial, aggregation function reference |
| 10 | Python API (dolphindb) | [docs/09.python-api.md](docs/09.python-api.md) | connect, run, upload, table operations, type mapping |
| 11 | Java API | [docs/10.java-api.md](docs/10.java-api.md) | DBConnection, BasicTable, type mapping |
| 12 | C++ API | [docs/11.cpp-api.md](docs/11.cpp-api.md) | DBConnection, ConstantSP, data types |
| 13 | Data Import | [docs/12.data-import.md](docs/12.data-import.md) | loadText, ploadText, CSV/HDF5/Parquet ingestion |
| 14 | Performance & Tuning | [docs/13.performance.md](docs/13.performance.md) | Partitioning strategy, query optimization, parallel computing |
| 15 | Security & Admin | [docs/14.admin.md](docs/14.admin.md) | User management, ACL, backup, cluster config |

---

## High-Frequency Patterns

The following snippets cover the most commonly asked questions. Use them directly if they match.

### Connect via Python API

```python
import dolphindb as ddb

s = ddb.session()
s.connect("localhost", 8848, "admin", "123456")

# Run a DolphinDB script and get result as DataFrame
df = s.run("select * from loadTable('dfs://trades', `trade) limit 100")
```

### Create a partitioned DFS database and table

```dolphindb
// Create database (RANGE partition by date)
db = database("dfs://trades", RANGE, 2020.01.01..2030.01.01)

// Define schema
schema = table(
    1:0,
    `sym`date`price`volume,
    [SYMBOL, DATE, DOUBLE, INT]
)

// Create partitioned table
db.createPartitionedTable(schema, `trade, `date)
```

### Append data to a DFS table

```dolphindb
t = table(
    take(`AAPL`MSFT, 10) as sym,
    take(2024.01.01..2024.01.10, 10) as date,
    rand(100.0, 10) as price,
    rand(1000, 10) as volume
)
loadTable("dfs://trades", `trade).append!(t)
```

### Stream table + subscription

```dolphindb
// Create stream table
share streamTable(1000:0, `time`sym`price, [TIMESTAMP, SYMBOL, DOUBLE]) as trades

// Define handler
def myHandler(msg) {
    print(msg)
}

// Subscribe
subscribeTable(tableName=`trades, actionName=`myAction, handler=myHandler, msgAsTable=true)
```

### Common SELECT patterns

```dolphindb
// Time-range filter
select * from t where date between 2024.01.01 : 2024.03.31

// Group by with aggregation
select sym, avg(price), sum(volume) from t group by sym

// Context by (per-group time-series calculation)
select sym, date, price, mavg(price, 5) as ma5 from t context by sym

// Window function
select sym, date, price, mmax(price, 10) as rolling_max from t context by sym
```

### Type quick-reference

| DolphinDB type | Python equivalent | Example literal |
|----------------|------------------|-----------------|
| INT | int | `42i` |
| LONG | int | `42l` |
| DOUBLE | float | `3.14` |
| BOOL | bool | `true` / `false` |
| STRING | str | `"hello"` |
| SYMBOL | str (categorical) | `\`AAPL` |
| DATE | datetime.date | `2024.01.01` |
| DATETIME | datetime.datetime | `2024.01.01T12:00:00` |
| TIMESTAMP | datetime + ms | `2024.01.01T12:00:00.000` |
